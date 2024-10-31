import math
import cadquery as cq

from dovetailstoragegrid import DovetailStorageGrid as dsg

cell_size = 32 #mm

dsg_01 = dsg(x = cell_size, y = cell_size, z = 62, dovetail_gap=0.1)

show_object(dsg_01.label_tray(1,1), options = {"alpha":0.5, "color":"blue"})

show_object(dsg_01.label_tray(1,1).translate((cell_size,0,0)), options = {"alpha":0.5, "color":"yellow"})

show_object(dsg_01.label_tray(1,1).translate((0,cell_size,0)), options = {"alpha":0.5, "color":"red"})
