"""
MIT License

Copyright (c) 2024 Roger Cheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math
import cadquery as cq

class DovetailStorageGrid:
    """
    Dove-tail storage grid

    Python class using CadQuery to describe storage trays that are sized to
    conform to a specified grid and interlock with each other via dovetail
    features on their sides.
    """

    """
    The array of storage trays are axis aligned as follows when viewing the
    storage grid from above:

    X-axis: -X is left, +X is right.
    Y-axis: -Y is front, +Y is rear.
    Z-axis: -Z is the bottom, +Z is the top of an individual tray.

    Optional ledge for labeling is tilted towards -Y and +Z because user is
    expected to view the array from above and in front.
    """

    def __init__(self,
                 x = 15,
                 y = 15,
                 z = 75,
                 tray_gap = 0.1,
                 corner_fillet = 2,
                 chamfer_top = 1, chamfer_bottom=1.5,
                 dovetail_protrusion = 2.5,
                 dovetail_length_fraction = 0.5,
                 dovetail_angle = 60,
                 dovetail_gap = 0.2):
        """
        Configure parameters common to all generated trays.

        X, Y, and Z are fundamental to a storage grid. Defaults are provided
        but usually overridden by user to fit specific usage scenario.

        Remainder of parameters are available for fine-tuning but beware of
        invalid combinations.

        :param x: Size (in mm) of each grid cell along the X (left/right) axis.
        :param y: Size (in mm) of each grid cell along the Y (front/back) axis.
        :param z: Height (in mm) of a tray.
        :param tray_gap: Gap (in mm) to leave on X/Y sides of a tray to allow
            easier assembly/removal. Zero generates tight-fitting trays.
        :param corner_fillet: Round off vertical edges, in mm.
        :param chamfer_top: Chamfer top (>Z) edges, in mm.
        :param chamfer_buttom: Chamfer bottom (<Z) edges, in mm.
        :param dovetail_protrusion: How far (in mm) a dovetail protrudes from
            the left and front side of each tray, and how deep to cut the
            match slot on the right and rear sides of the tray.
        :param dovetail_length_fraction: Fraction (between 0.0 and 1.0) of
            a grid cell's size to devote to dovetail. Weird things happen when
            too far away from 0.5.
        :param dovetail_angle: Dovetail angle in degrees, usually 45 or 60.
        :param dovetail_gap: Gap (in mm) to leave on sides of a dovetail to
            allow easier assembly/removal. Zero generates tight-fitting
            dovetails.
        """
        if tray_gap < 0:
            raise ValueError("Trays with negative gaps will not fit together.")

        self.grid_x = x
        self.grid_y = y
        self.grid_z = z
        self.tray_gap = tray_gap
        self.corner_fillet = corner_fillet
        self.chamfer_top = chamfer_top
        self.chamfer_bottom = chamfer_bottom
        self.dovetail_protrusion = dovetail_protrusion
        self.dovetail_length_fraction = dovetail_length_fraction
        self.dovetail_angle = dovetail_angle
        self.dovetail_gap = dovetail_gap

    def nominal_volume(self, x=1, y=1):
        """
        Returns the nominal volume for specified number of grid cells.

        Actual tray will extend beyond this volume for dovetail.
        Useful for visualization in tools like CQ-editor.
        Also used internally as starting point to build a tray.

        :param x: Number of grid cells along X (left/right) axis.
        :param y: Number of grid cells along Y (front/back) axis.
        """
        return (
            cq.Workplane("XY")
            .lineTo(0,               self.grid_y * y)
            .lineTo(self.grid_x * x, self.grid_y * y)
            .lineTo(self.grid_x * x, 0)
            .close()
            .extrude(self.grid_z)
        )

    def _grow_xy_by(self, shape, amount):
        """
        Grow the given shape along X and Y axis by the given size in mm.

        Feels like there should be an existing CadQuery operator for growing/
        shrinking a shape, since the math already exists for .shell(). But
        I haven't found it yet. In the meantime, call shell() then using the
        result to modify original shape.
        """
        if amount < 0:
            shape = shape - shape.faces("+Z or -Z").shell(amount)
        elif amount > 0:
            shape = shape + shape.faces("+Z or -Z").shell(amount)

        return shape

    def bounding_volume(self, x=1, y=1):
        """
        Returns the maximum volume for specified number of grid cells.

        Actual tray will not exceed this volume.
        Useful for visualization in tools like CQ-editor.
        Also used internally in a finishing step to cut off extraneous parts.

        :param x: Number of grid cells along X (left/right) axis.
        :param y: Number of grid cells along Y (front/back) axis.
        """
        bounds = self._grow_xy_by(self.nominal_volume(x, y), self.dovetail_protrusion)
        p = self.dovetail_protrusion
        bounds = (
            cq.Workplane("XY")
            .lineTo(-p,                   -p, forConstruction = True)
            .lineTo(-p,                    p + self.grid_y * y)
            .lineTo( p + self.grid_x * x,  p + self.grid_y * y)
            .lineTo( p + self.grid_x * x, -p)
            .close()
            .extrude(self.grid_z)
        )

        bounds = bounds.faces("+Z").chamfer(self.dovetail_protrusion + self.chamfer_top)
        bounds = bounds.faces("-Z").chamfer(self.dovetail_protrusion + self.chamfer_bottom)
        bounds = bounds.edges("not (>Z or <Z)").fillet(self.corner_fillet)
        return bounds

    def _dovetail(self, width):
        """
        Return a trapezoidal volume for use as interlink dovetail. Usually not
        called directly, use _dovetail_x or _dovetail_y to build a dovetail
        aligned with the proper axis.
        """
        return (
            cq.Workplane("XY").sketch()
            .trapezoid(
                w = width,
                h = self.dovetail_protrusion+self.tray_gap+self.dovetail_gap*2,
                a1 = self.dovetail_angle)
            .finalize()
            .extrude(self.grid_z)
            .translate((0, -(self.dovetail_protrusion-self.tray_gap)/2,0))
            )

    def _dovetail_y(self):
        """
        Create a trapezoidal volume for use as interlink dovetails on front
        and back (+Y and -Y) faces.
        """
        return self._dovetail(width = self.grid_x * self.dovetail_length_fraction)

    def _dovetail_x(self):
        """
        Create a trapezoidal volume for use as interlink dovetails on left
        and right (+X and -X) faces.
        """
        return (
            self._dovetail(width = self.grid_y * self.dovetail_length_fraction)
            .rotate((0, 0, 0), (0, 0, 1), -90))

    def _tray(self, x=1, y=1):
        """
        Create a dovetail tray solid with given size specified in number of grid cells.
        """
        tray = self.nominal_volume(x, y)
        tray = tray.edges("|Z").fillet(self.corner_fillet)
        if self.tray_gap > 0:
            tray = self._grow_xy_by(tray,-self.tray_gap)

        tray_x = x * self.grid_x
        tray_y = y * self.grid_y

        dovetail_y = self._dovetail_y()
        for x_index in range(x):
            x_position = self.grid_x/2 + x_index*self.grid_x
            tray = tray + self._grow_xy_by(dovetail_y,-self.dovetail_gap).translate((x_position, 0,      0))
            tray = tray - self._grow_xy_by(dovetail_y, self.dovetail_gap).translate((x_position, tray_y, 0))

        dovetail_x = self._dovetail_x()
        for y_index in range(y):
            y_position = self.grid_y/2 + y_index*self.grid_y
            tray = tray + self._grow_xy_by(dovetail_x,-self.dovetail_gap).translate((0,      y_position, 0))
            tray = tray - self._grow_xy_by(dovetail_x, self.dovetail_gap).translate((tray_x, y_position, 0))

        tray = tray.intersect(self.bounding_volume(x,y))

        return tray

    def basic_tray(self, x=1, y=1, wall_thickness=0):
        """
        Return a basic (no additional feature) tray

        :param x: Number of grid cells along X (left/right) axis.
        :param y: Number of grid cells along Y (front/back) axis.
        :param wall_thickness: Default 0 generates a solid for vase mode print.
            Nonzero generates wall of specified thickness (in mm) to be printed
            normally. Recommend a multiple of nozzle diameter: 0.8, 1.2, etc.
        """
        tray = self._tray(x,y)

        # If a nonzero wall thickness was specified, use the .shell() operator
        # to generate a tray to be printed normally (vs. vase mode solid)
        if wall_thickness > 0:
            tray = tray.faces(">Z").shell(-wall_thickness)

        return tray

    def label_tray(self, x=1, y=1, wall_thickness=0, label_height=10):
        """
        Return a tray with a top front label area of specified size.

        :param x: Number of grid cells along X (left/right) axis.
        :param y: Number of grid cells along Y (front/back) axis.
        :param wall_thickness: Default 0 generates a solid for vase mode print.
            Nonzero generates wall of specified thickness (in mm) to be printed
            normally. Recommend a multiple of nozzle diameter: 0.8, 1.2, etc.
        :param label_height: Height of label area, in mm.
        """
        label_size = label_height/math.sqrt(2)

        # Cut out a wedge for the label area.
        tray = self._tray(x,y) - (
            cq.Workplane("YZ")
            .lineTo(  label_size,               self.grid_z, forConstruction = True)
            .lineTo( -self.dovetail_protrusion, self.grid_z)
            .lineTo( -self.dovetail_protrusion, self.grid_z - self.dovetail_protrusion - label_size)
            .close()
            .extrude(x*self.grid_x)
        )

        # Cutting out a wedge for the label may leave a tiny peak at the front-
        # most dovetail slot. This must be removed for printing in vase mode.
        # Feels like this can be done more elegantly but in the meantime this
        # will suffice for avoiding the problem.
        tray = tray - (
            cq.Workplane("YZ").workplane(offset = x * self.grid_x)
            .lineTo(  label_size,               self.grid_z, forConstruction = True)
            .lineTo( -self.dovetail_protrusion, self.grid_z)
            .lineTo( -self.dovetail_protrusion, self.grid_z - self.dovetail_protrusion * 2 - label_size)
            .lineTo(  label_size,               self.grid_z - self.dovetail_protrusion * 2 - label_size)
            .close()
            .workplane(offset = -self.dovetail_protrusion - self.dovetail_gap - self.tray_gap)
            .lineTo(  label_size,               self.grid_z, forConstruction = True)
            .lineTo( -self.dovetail_protrusion, self.grid_z)
            .lineTo( -self.dovetail_protrusion, self.grid_z - self.dovetail_protrusion - label_size)
            .lineTo(  label_size,               self.grid_z - self.dovetail_protrusion - label_size)
            .close()
            .loft()
        )

        # If a nonzero wall thickness was specified, use the .shell() operator
        # to generate a tray to be printed normally (vs. vase mode solid)
        if wall_thickness > 0:
            tray = tray.faces(">Z").shell(-wall_thickness)

        return tray
