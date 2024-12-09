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

"""
Using CQ-Editor to generate dovetail storage grid trays.

This file is intended to be opened in CQ-Editor for interactive visualization
while experimenting with different parameters. See dovetailstoragegrid.py for
documentation on what each parameter means.
"""

"""
This specific example generates a tray with small support element designed
for a Creality CR-30 a.k.a. CrealityBelt a.k.a. Naomi Wu's 3DPrintMill
"""

import math
import cadquery as cq

from dovetailstoragegrid import DovetailStorageGrid as dsg

cell_size = 15 #mm
dsg_01 = dsg(x = cell_size, y = cell_size, z = 75)

tray_x = 3
tray_y = 3

thickness = 0.7

# Generate standard tray
tray = dsg_01.label_tray(tray_x, tray_y, wall_thickness=thickness)

# Generate a support object with custom fit by subtracting the tray
support_center = tray_y*cell_size
support_size = 2
support_gap = 0.4
support = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, 0, -support_size))
    .lineTo(support_center - support_size, 0, forConstruction = True)
    .lineTo(support_center               , support_size)
    .lineTo(support_center + support_size, 0)
    .close()
    .extrude(tray_x*cell_size+support_size*2)
    )
exterior = dsg_01._grow_xy_by(dsg_01.bounding_volume(tray_x, tray_y), support_gap)
support = support - exterior

# Generate a brim that connects the first line to the support
brim_height = 0.6
brim = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, 0, -support_size))
    .lineTo(support_center - support_size, 0, forConstruction = True)
    .lineTo(support_center - support_size+ brim_height, brim_height)
    .lineTo(support_center               , brim_height)
    .lineTo(support_center               , 0)
    .close()
    .extrude(tray_x*cell_size+support_size*2)
    )

#show_object(brim)
#show_object(support, options = {"alpha":0.5, "color":"aquamarine"})
#show_object(tray, options = {"alpha":0.5, "color":"red"})

assembly = tray + support + brim

show_object(assembly)