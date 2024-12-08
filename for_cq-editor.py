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
tray_gap = 0.1 #mm
chamfer_bottom = 0.6 #mm
dsg_01 = dsg(x = cell_size, y = cell_size, z = 75, chamfer_bottom=chamfer_bottom, tray_gap = tray_gap)

tray_x = 3
tray_y = 3

thickness = 0.8

# Generate standard tray
standard = dsg_01.label_tray(tray_x, tray_y, wall_thickness=thickness)

# Add a brim to help belt printing get started
tray_w = tray_x*cell_size
tray_h = tray_y*cell_size
brim = (
    cq.Workplane("XY")
    .lineTo(tray_w*3/2 ,tray_h/2, forConstruction=True)
    .lineTo(tray_w/2 , tray_h*3/2)
    .lineTo(0,tray_h-tray_gap-chamfer_bottom)
    .lineTo(tray_w-tray_gap-chamfer_bottom,tray_h-tray_gap-chamfer_bottom)
    .lineTo(tray_w-tray_gap-chamfer_bottom,0)
    .close()
    .extrude(0.6)
    )
support = brim

# Due to dovetail orientation I think the back right corner is the best
# starting point for belt printer
unit = brim + standard
unit = unit.rotate((0,0,0),(0,0,1),45)

show_object(unit)
