from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import csv

matplotlib.use('TkAgg')


class Point:
    def __init__(self, x, y, id_num=""):
        self.x = x
        self.y = y
        self.id_num = id_num


class Data:
    def __init__(self, name=""):
        self.__name = name

    def read_input(self, filename=""):
        pointlist = []
        with open(filename, "r") as f:  # Read input.csv file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                id_num = row["id"]
                point = Point(x, y, id_num)
                pointlist.append(point)
        return pointlist

    def read_polygon(self, filename=""):
        polylist = []
        with open(filename, "r") as f:  # Read polygon.csv file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                point = Point(x, y)
                polylist.append(point)
            return polylist


class Classification:
    def get_mbr(self, points):
        points = Data().read_polygon("polygon.csv")
        length = len(points)
        top = down = left = right = points[0]
        for i in range(1, length):
            if points[i].x > top.x:
                top = points[i]
            elif points[i].x < down.x:
                down = points[i]
            else:
                pass
            if points[i].y > right.y:
                right = points[i]
            elif points[i].y < left.y:
                left = points[i]
            else:
                pass
        point0 = Point(top.x, left.y)
        point1 = Point(top.x, right.y)
        point2 = Point(down.x, right.y)
        point3 = Point(down.x, left.y)
        mbr = [point0, point1, point2, point3]
        return mbr

    def is_point_in_mbr(self, point, mbr):
        if mbr[3].x <= point.x <= mbr[0].x and mbr[3].y <= point.y <= mbr[2].y:
            return True
        else:
            return False

    def piptest(self, pointlist, polylist, category=None):
        point_outside = []
        point_inside = []
        point_boundary = []
        for points in polylist:
            mbr = Classification().get_mbr(points)
            for point in pointlist:
                if not Classification().is_point_in_mbr(point, mbr):
                    point_outside.append(point)
                    continue

                length = len(polylist)
                p = point
                p1 = polylist[0]
                counting = 0
                for i in range(1, length):
                    p2 = polylist[i]
                    if (p.x == p1.x and p.y == p1.y) or (p.x == p2.x and p.y == p2.y):
                        point_boundary.append(p)
                        break
                    if p1.y == p.y == p2.y:
                        if p1.x < p.x < p2.x or p2.x < p.x < p1.x:
                            point_boundary.append(p)
                            break
                    if (p1.y < p.y <= p2.y) or (p2.y < p.y <= p1.y):
                        x = p2.x - (p2.y - p.y) * (p2.x - p1.x) / (p2.y - p1.y)
                        if x == p.x:
                            point_boundary.append(p)
                            break
                        if x > p.x:
                            counting += 1
                    p1 = p2
                if p not in point_boundary:
                    if counting % 2 == 0:
                        point_outside.append(p)
                    else:
                        point_inside.append(p)
        if category == "outside":
            return point_outside
        if category == "inside":
            return point_inside
        if category == "boundary":
            return point_boundary


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


def main():
    plotter = Plotter()
    data = Data()
    polygonset = data.read_polygon("polygon.csv")
    pointset = data.read_input("input.csv")
    categorize_points = Classification()
    piptest = categorize_points.piptest(pointset, polygonset)
    outside = categorize_points.piptest(pointset, polygonset, "outside")
    inside = categorize_points.piptest(pointset, polygonset, "inside")
    boundary = categorize_points.piptest(pointset, polygonset, "boundary")
    polygonset
    print("read polygon.csv")
    pointset
    print("read input.csv")
    piptest
    print("categorize points")

    print("write output.csv")
    x_polygon = []
    y_polygon = []
    for point in polygonset:
        x_polygon.append(point.x)
        y_polygon.append(point.y)
    plotter.add_polygon(x_polygon, y_polygon)

    x_outside_list = []
    y_outside_list = []
    for point in outside:
        x_outside_list.append(point.x)
        y_outside_list.append(point.y)
    plotter.add_point(x_outside_list, y_outside_list, "outside")

    x_inside_list = []
    y_inside_list = []
    for point in inside:
        x_inside_list.append(point.x)
        y_inside_list.append(point.y)
    plotter.add_point(x_inside_list, y_inside_list, "inside")

    x_boundary_list = []
    y_boundary_list = []
    for point in boundary:
        x_boundary_list.append(point.x)
        y_boundary_list.append(point.y)
    plotter.add_point(x_boundary_list, y_boundary_list, "boundary")
    print("plot polygon and points")
    plotter.show()


if __name__ == "__main__":
    main()