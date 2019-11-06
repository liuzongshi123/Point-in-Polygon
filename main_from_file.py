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
    def __init__(self, name, polylist):
        length = len(polylist)
        top = down = left = right = polylist[0]
        for i in range(1, length):
            if polylist[i].get_x() > top.get_x():
                top = polylist[i]
            elif polylist[i].get_x() < down.get_x():
                down = polylist[i]
            if polylist[i].get_y() > right.get_y():
                right = polylist[i]
            elif polylist[i].get_y() < left.get_y():
                left = polylist[i]
        point0 = Point("topright", top.get_x(), left.get_y())
        point1 = Point("bottomright", top.get_x(), right.get_y())
        point2 = Point("bottomleft", down.get_x(), right.get_y())
        point3 = Point("topleft", down.get_x(), left.get_y())
        points = [point0, point1, point2, point3]
        super().__init__(name, points)

    def get_mbr(self):
        mbr = self.get_points()
        return mbr


class Judgement:
    def is_point_in_mbr(self, point, mbr):
        if mbr[3].get_x() <= point.get_x() <= mbr[0].get_x() and \
                mbr[3].get_y() <= point.get_y() <= mbr[2].get_y():
            return True
        else:
            return False

    def pip_test(self, pointlist, polylist, category=""):
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
                p1_x = line.point_1.get_x()
                p1_y = line.point_1.get_y()
                p2_x = line.point_2.get_x()
                p2_y = line.point_2.get_y()
                if (p_x == p1_x and p_y == p1_y) or (p_x == p2_x and p_y == p2_y):
                    point_boundary.append(point)
                    break
                if p1_y == p_y == p2_y:
                    if (p1_x < p_x < p2_x) or (p2_x < p_x < p1_x):
                        point_boundary.append(point)
                        break
                if (p1_y < p_y <= p2_y) or (p2_y < p_y <= p1_y):
                    x = p2_x - (p2_y - p_y) * \
                        (p2_x - p1_x) / (p2_y - p1_y)
                    if x == p_x:
                        point_boundary.append(point)
                        break
                    if x > p_x:
                        counting += 1
            if point not in point_boundary:
                if counting % 2 == 0:
                    point_outside.append(point)
                else:
                    point_inside.append(point)
        if category == "outside":
            return point_outside
        if category == "inside":
            return point_inside
        if category == "boundary":
            return point_boundary

    def classification(self, name=""):
        point_list = []
        point_set = File().read_file("input.csv")
        polygon_set = File().read_file("polygon.csv")
        points = self.pip_test(point_set, polygon_set, name)
        for point in points:
            point_list.append(point)
        return point_list


class File:
    def __init__(self, name=""):
        self.name = name

    def read_file(self, filename=""):
        pointlist = []
        with open(filename, "r") as f:  # Read file by using "DictReader" function
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                id_num = row["id"]
                point = Point(id_num, x, y)
                pointlist.append(point)
        return pointlist

    def write_file(self, filename=""):
        point_set = File().read_file("input.csv")
        outside = Judgement().classification("outside")
        inside = Judgement().classification("inside")
        boundary = Judgement().classification("boundary")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category"])
            for point in point_set:
                if point in outside:
                    writer.writerow([point.get_name(), "outside"])
                if point in inside:
                    writer.writerow([point.get_name(), "inside"])
                if point in boundary:
                    writer.writerow([point.get_name(), "boundary"])


def main():
    plotter = Plotter()
    outside = Judgement().classification("outside")
    inside = Judgement().classification("inside")
    boundary = Judgement().classification("boundary")
    print("read polygon.csv")

    print("read input.csv")

    print("categorize points")
    File().write_file("output.csv")
    print("write output.csv")
    x_polygon = []
    y_polygon = []
    for point in File().read_file("polygon.csv"):
        x_polygon.append(point.get_x())
        y_polygon.append(point.get_y())
    plotter.add_polygon(x_polygon, y_polygon)

    x_outside_list = []
    y_outside_list = []
    for point in outside:
        x_outside_list.append(point.get_x())
        y_outside_list.append(point.get_y())
    plotter.add_point(x_outside_list, y_outside_list, "outside")

    x_inside_list = []
    y_inside_list = []
    for point in inside:
        x_inside_list.append(point.get_x())
        y_inside_list.append(point.get_y())
    plotter.add_point(x_inside_list, y_inside_list, "inside")

    x_boundary_list = []
    y_boundary_list = []
    for point in boundary:
        x_boundary_list.append(point.get_x())
        y_boundary_list.append(point.get_y())
    plotter.add_point(x_boundary_list, y_boundary_list, "boundary")
    print("plot polygon and points")
    plotter.show()


if __name__ == "__main__":
    main()
