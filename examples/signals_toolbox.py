"""
MIT License

Copyright (c) 2026 Roger Cheng

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
import cadquery.selectors as sel
from cadquery import exporters

import sys

sys.path.append("../")  # Fragile, depends on directory structure
import dovetailstoragegrid


# When not running in CQ-Editor, turn log into print
if "log" not in globals():

    def log(*args):
        print(args)


# When not running in CQ-Editor, turn show_object into no-op
if "show_object" not in globals():

    def show_object(*args, **kwargs):
        pass


def inch_to_mm(length_inch: float):
    return length_inch * 25.4


class signals_toolbox:
    """
    Using the storage grid system to organize my LALS signals tool box
    """

    def __init__(
        self,
        cell_size=15,
        dovetail_gap=0.2,
    ):
        self.cell_size = cell_size
        self.dovetail_gap = dovetail_gap
        self.height = 140

        # Create instance of tray generator
        self.generator = dovetailstoragegrid.DovetailStorageGrid(
            x=self.cell_size, y=self.cell_size, z=self.height, dovetail_gap=dovetail_gap
        )

    def generic_tray(self, width, depth):
        return self.generator.basic_tray(
            math.ceil(width / self.cell_size),
            math.ceil(depth / self.cell_size),
            wall_thickness=0,
        )

    def dual_jewel_box(self):
        """
        Holds two small multi-compartment plastic containers ("jewel boxes")
        vertically
        """
        return self.generic_tray(width=23 * 2, depth=102)

    def wire_stripper_knipex(self):
        """
        One of the most frequently used tools: Knipex wire stripper 12 62 180
        for 10-24 AWG wire
        """
        return self.generic_tray(width=28, depth=100)

    def ferrule_crimper(self):
        """
        Kangora HC-8893 ferrule crimper
        """
        return self.generic_tray(width=22, depth=74)

    def meter_scope(self):
        """
        Fnirsi 2C53T portable meter scope
        """
        return self.generic_tray(width=60, depth=90)

    def magnet_wire_organizer(self):
        """
        Magnetic wire organizer base and supply of zip ties
        """
        return self.generic_tray(width=35, depth=100)


st = signals_toolbox()

show_object(st.magnet_wire_organizer(), options={"color": "green", "alpha": 0.5})
