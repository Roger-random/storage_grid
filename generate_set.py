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
Programmatically generate dovetail storage grid trays.

This file is an example of how to programmatically generate a set of trays
with specified combination of parameters. Must be executed in an environment
with CadQuery installed, usually at a command line.

Modify as needed to generate trays to suit your needs.

See dovetailstoragegrid.py for documentation on what each parameter means.

Alternatively see for_cq-editor.py for an example using CQ-Editor GUI tool.

See CadQuery documentation on file export formats to see options other than
STL files. For example, you can export STEP for further customization in
CAD tool of your choice.
"""

from cadquery import exporters
from dovetailstoragegrid import DovetailStorageGrid as dsg

# Create an instance of the generator with common parameters
d = dsg(x = 15, y = 15, z = 63,
        dovetail_angle=60, dovetail_protrusion=2.5, dovetail_gap = 0.15)

# Create a range of tray sizes and export to STL for vase mode 3D printing
for x_size in range(2, 5, 2):
    for y_size in range(2, 5, 1):
        filename = "./dsg_x{:d}y{:d}.stl".format(x_size, y_size)
        print("Generating: {:s}".format(filename))

        tray = d.label_tray(x_size, y_size)
        exporters.export(tray, filename)
