from collections import OrderedDict
import matplotlib.pyplot as plt
import csv
from plotter import Plotter


class Geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(Geometry):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


class Line(Geometry):
    def __init__(self, name, point_1, point_2):
        super().__init__(name)
        self.point_1 = point_1
        self.point_2 = point_2


class Polygon(Geometry):
    def __init__(self, name, points):
        super().__init__(name)
        self.__points = points

    def get_points(self):
        return self.__points

    def lines(self):
        res = []
        points = self.get_points()
        point_a = points[0]
        for point_b in points[1:]:
            res.append(Line(point_a.get_name() + "-" + point_b.get_name(), point_a, point_b))
            point_a = point_b
        res.append(Line(point_a.get_name() + "-" + points[0].get_name(), point_a, points[0]))
        return res


class MBR(Polygon):
    def get_mbr(self):
        points = self.get_points()
        length = len(points)
        top = down = left = right = points[0]
        for i in range(1, length):
            if points[i].x > top.x:
                top = points[i]
            elif points[i].x < down.x:
                down = points[i]
            if points[i].y > right.y:
                right = points[i]
            elif points[i].y < left.y:
                left = points[i]
        point0 = Point("topright", top.x, left.y)
        point1 = Point("bottomright", top.x, right.y)
        point2 = Point("bottomleft", down.x, right.y)
        point3 = Point("topleft", down.x, left.y)
        mbr = [point0, point1, point2, point3]
        return mbr


class Judgement:
    def is_point_in_mbr(self, point, mbr):
        if mbr[3].x <= point.x <= mbr[0].x and mbr[3].get_y() <= point.y <= mbr[2].y:
            return True
        else:
            return False

    def piptest(self, pointlist, polylist, category=None):
        point_outside = []
        point_inside = []
        point_boundary = []
        mbr = MBR("polygon", polylist).get_mbr()
        for point in pointlist:
            if not self.is_point_in_mbr(point, mbr):
                point_outside.append(point)
                continue
            lines = Polygon("polygonlines", polylist).lines()
            p_x = point.get_x()
            p_y = point.get_y()
            counting = 0
            for line in lines:
                if (p_x == line.point_1.x and p_y == line.point_1.y) or \
                        (p_x == line.point_2.x and p_y == line.point_2.y):
                    point_boundary.append(p)
                    break
                if line.point_1.y == p_y == line.point_2.y:
                    if line.point_1.x < p_x < line.point_2.y or \
                            line.point_2.x < p_x() < line.point_1.x:
                        point_boundary.append(p)
                        break
                if (line.point_1.y < p_y <= line.point_2.y) or \
                        (line.point_2.y < p_y <= line.point_1.y):
                    x = line.point_2.x - (line.point_2.y - p_y) * \
                        (line.point_2.x - line.point_1.x) / (line.point_2.y - line.point_1.y)
                    if x == p_x:
                        point_boundary.append(p)
                        break
                    if x > p_x:
                        counting += 1
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


class Data:
    def __init__(self, name=None):
        self.name = name

    def read_input(self, filename=""):
        pointlist = []
        with open(filename, "r") as f:  # Read input.csv file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                id_num = row["id"]
                point = Point(id_num, x, y)
                pointlist.append(point)
        return pointlist

    def read_polygon(self, filename=""):
        polylist = []
        with open(filename, "r") as f:  # Read polygon.csv file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                id_num = row["id"]
                point = Point(id_num, x, y)
                polylist.append(point)
            return polylist

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
    categorize_points = Judgement()
    polygonset = data.read_polygon("polygon.csv")
    pointset = data.read_input("input.csv")
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