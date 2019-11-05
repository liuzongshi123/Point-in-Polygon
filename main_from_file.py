from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import csv
matplotlib.use('TkAgg')


class Geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(Geometry):
    x = ""
    y = ""
    id_unm = ""

    def __init__(self, name, x, y, id_num):
        super().__init__(name)
        self.__x = x
        self.__y = y
        self.__id_num = id_num

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_id_num(self):
        return self.__id_num


class Pointset(Point):
    pointlist = []
    polylist = []
    point_outside = []
    point_boundary = []
    point_inside = []

    def __init__(self, name, pointlist, polylist, point_outside, point_inside, point_boundary):
        super().__init__(name)
        self.__pointlist = pointlist
        self.__polylist = polylist
        self.__point_outside = point_outside
        self.__point_inside = point_inside
        self.__point_boundary = point_boundary

    def get_pointlist(self):
        return self.__pointlist

    def get_polylist(self):
        return self.__polylist

    def get_point_outside(self):
        return self.__point_outside

    def get_point_inside(self):
        return self.__point_inside

    def get_point_boundary(self):
        return self.__point_boundary

    def read_input(self):
        with open("input.csv", "r") as f:  # Read input.csv file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                id_num = row["id"]
                point = Point(x, y, id_num)
                self.__pointlist.append(point)
        return self.get_pointlist()

    def read_polygon(self):
        with open("polygon.csv", "r") as f:  # Read polygon.csv file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                point = Point(x, y)
                self.__polylist.append(point)
            return self.get_polylist()


class Classification(Pointset):
    def __init__(self, name, points):
        super().__init__(name)

    def get_mbr(points):
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

    def is_point_in_mbr(point, mbr):
        if mbr[3].x <= point.x <= mbr[0].x and mbr[3].y <= point.y <= mbr[2].y:
            return True
        else:
            return False

    def is_point_in_polygon(pointlist, polylist):
        point_outside = []
        point_boundary = []
        point_inside = []
        for points in polylist:
            mbr = get_mbr(points)
            for point in pointlist:
                if not is_point_in_mbr(point, mbr):
                    point_outside.append(point)
                    continue

                length = len(points)
                p = point
                p1 = points[0]
                counting = 0
                for i in range(1, length):
                    p2 = points[i]
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
        return point_outside, point_boundary, point_inside


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
    Pointset.read_polygon()
    print("read polygon.csv")
    Pointset.read_input()
    print("read input.csv")
    Classification.is_point_in_polygon(pointlist, polylist)
    print("categorize points")

    print("write output.csv")
    x_polygon = []
    y_polygon = []
    for point in Pointset.polylist:
        x_polygon.append(point.x)
        y_polygon.append(point.y)
    plotter.add_polygon(x_polygon, y_polygon)

    x_outside_list = []
    y_outside_list = []
    for point in Pointset.point_outside:
        x_outside_list.append(point.x)
        y_outside_list.append(point.y)
    plotter.add_point(x_outside_list, y_outside_list, "outside")

    x_inside_list = []
    y_inside_list = []
    for point in Pointset.point_inside:
        x_inside_list.append(point.x)
        y_inside_list.append(point.y)
    plotter.add_point(x_inside_list, y_inside_list, "inside")

    x_boundary_list = []
    y_boundary_list = []
    for point in Pointset.point_boundary:
        x_boundary_list.append(point.x)
        y_boundary_list.append(point.y)
    plotter.add_point(x_boundary_list, y_boundary_list, "boundary")
    print("plot polygon and points")
    plotter.show()


if __name__ == "__main__":
    main()
