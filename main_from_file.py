# Read polygon.csv file and extract the coordinates of each point
import csv
with open("polygon.csv", "r") as f:
    x_polygon = []
    y_polygon = []
    polygonlist = []
    reader = csv.DictReader(f)  # The CSV file would be analyzed by using "DictReader" function
    for row in reader:
        polygon = [0, 0]
        polygon[0] = float(row["x"])
        polygon[1] = float(row["y"])
        polygonlist.append(polygon)
        x_polygon.append(float(row['x']))
        y_polygon.append(float(row["y"]))

# Read input.csv file and extract the coordinates of each point
with open("input.csv", "r") as f:
    x_point = []
    y_point = []
    poi = []
    reader = csv.DictReader(f)  # The CSV file would be analyzed by using "DictReader" function
    for row in reader:
        point = [0, 0, 0]
        point[0] = float(row["x"])
        point[1] = float(row["y"])
        point[2] = int(row["id"])
        poi.append(point)
        x_point.append(float(row["x"]))
        y_point.append(float(row["y"]))


point_outside = []
point_boundary = []
point_inside = []


max_x = max(x_polygon)
min_x = min(x_polygon)
max_y = max(y_polygon)
min_y = min(y_polygon)
for point in poi:
    if point[0] > max_x or point[0] < min_x or point[1] > max_y or point[1] < min_y:
        point_outside.append(point)
    else:
        counting = 0
        point1 = polygonlist[0]
        for i in range(1, len(polygonlist)):
            point2 = polygonlist[i]
            if (point[0] == point1[0] and point[1] == point1[1]) or (point[0] == point2[0] and point[1] == point2[1]):
                point_boundary.append(point)
                break
            if point1[1] == point[1] == point2[1]:
                if point1[0] < point[0] < point2[0] or point2[0] < point[0] < point1[0]:
                    point_boundary.append(point)
                    break
            if (point1[1] < point[1] <= point2[1]) or (point2[1] < point[1] <= point1[1]):
                point12lng = point2[0] - (point2[1] - point[1]) * (point2[0] - point1[0]) / (point2[1] - point1[1])
                if point12lng == point[0]:
                    point_boundary.append(point)
                    break
                if point12lng > point[0]:
                    counting += 1
            point1 = point2
        if point not in point_boundary:
            if counting % 2 == 0:
                point_outside.append(point)
            else:
                point_inside.append(point)

with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "category"])
    for point in poi:
        if point in point_boundary:
            writer.writerow([str(point[2], "boundary")])
        if point in point_outside:
            writer.writerow([str(point[2], "outside")])
        if point in point_inside:
            writer.writerow([str(point[2], "inside")])







x_outside_list = []
y_outside_list = []
for i in range(len(point_outside)):
    x_outside_list.append(point_outside[i][0])
    y_outside_list.append(point_outside[i][1])
x_boundary_list = []
y_boundary_list = []
for i in range(len(point_boundary)):
    x_boundary_list.append(point_boundary[i][0])
    y_boundary_list.append(point_boundary[i][1])
x_inside_list = []
y_inside_list = []
for i in range(len(point_inside)):
    x_inside_list.append(point_inside[i][0])
    y_inside_list.append(point_inside[i][1])






from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None):
        if kind == "outside":
            plt.plot(x, y, "ro", label='Outside')
        elif kind == "boundary":
            plt.plot(x, y, "bo", label='Boundary')
        elif kind == "inside":
            plt.plot(x, y, "go", label='Inside')
        else:
            plt.plot(x, y, "ko", label='Unclassified')

    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()

plotter = Plotter()
plotter.add_polygon(x_polygon, y_polygon)
plotter.add_point(x_outside_list, y_outside_list, "outside")
plotter.add_point(x_boundary_list, y_boundary_list, "boundary")
plotter.add_point(x_inside_list, y_inside_list, "inside")
plotter.show()