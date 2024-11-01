import math
import cadquery as cq

from dovetailstoragegrid import DovetailStorageGrid as dsg

cell_size = 15 #mm

dsg_01 = dsg(x = cell_size, y = cell_size, z = 75, dovetail_angle=60, dovetail_protrusion = 2.5, dovetail_gap=0.2)

show_object(dsg_01.label_tray(2,1), options = {"alpha":0.5, "color":"blue"})

show_object(dsg_01.label_tray(2,1).translate((cell_size*2,0,0)), options = {"alpha":0.5, "color":"yellow"})

show_object(dsg_01.label_tray(2,1).translate((0,cell_size,0)), options = {"alpha":0.5, "color":"red"})
