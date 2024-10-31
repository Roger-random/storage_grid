from cadquery import exporters
from dovetailstoragegrid import DovetailStorageGrid as dsg

cell_size_x = 32 # mm
cell_size_y = 32 # mm
cell_size_z = 63 # mm

dovetail_gap = 0.1 # mm

d = dsg(x = cell_size_x, y = cell_size_y, z = cell_size_z,
        dovetail_gap = dovetail_gap)

for x_size in range(1, 4, 1):
    for y_size in range(1, 4, 1):
        filename = "./dsg_x{:d}y{:d}.stl".format(x_size, y_size)
        print("Generating: {:s}".format(filename))

        tray = d.label_tray(x_size, y_size)
        exporters.export(tray, filename)
