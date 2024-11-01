from cadquery import exporters
from dovetailstoragegrid import DovetailStorageGrid as dsg

d = dsg(x = 15, y = 15, z = 63,
        dovetail_angle=60, dovetail_protrusion=2.5, dovetail_gap = 0.15)

for x_size in range(2, 7, 2):
    for y_size in range(2, 7, 2):
        filename = "./dsg_x{:d}y{:d}.stl".format(x_size, y_size)
        print("Generating: {:s}".format(filename))

        tray = d.label_tray(x_size, y_size)
        exporters.export(tray, filename)
