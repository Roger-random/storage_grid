import math
import cadquery as cq

from dovetailstoragegrid import DovetailStorageGrid as dsg

cell_size = 15 #mm

dsg_01 = dsg(x = cell_size, y = cell_size, z = 75)

tray_x = 2
tray_y = 1

tray = dsg_01.label_tray(tray_x, tray_y)

show_object(tray, options = {"alpha":0.5, "color":"blue"})

show_object(tray.translate((cell_size*tray_x,0,0)), options = {"alpha":0.5, "color":"yellow"})

show_object(tray.translate((0,cell_size*tray_y,0)), options = {"alpha":0.5, "color":"red"})
