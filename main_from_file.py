import csv
from plotter import Plotter


class Geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(Geometry):
    def __init__(self, name, x, y, category=None):
        super().__init__(name)
        self.__x = x
        self.__y = y
        self.__category = category

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_category(self):
        return self.__category


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

    def pip_test(self, pointlist, polylist):
        mbr = MBR("polygon", polylist).get_mbr()
        pointlist_aftertest = []
        for point in pointlist:
            if not self.is_point_in_mbr(point, mbr):
                point.category = "outside"
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
                    point.category = "boundary"
                    break
                if p1_y == p_y == p2_y:
                    if (p1_x < p_x < p2_x) or (p2_x < p_x < p1_x):
                        point.category = "boundary"
                        break
                if (p1_y < p_y <= p2_y) or (p2_y < p_y <= p1_y):
                    x = p2_x - (p2_y - p_y) * \
                        (p2_x - p1_x) / (p2_y - p1_y)
                    if x == p_x:
                        point.category = "boundary"
                        break
                    if x > p_x:
                        counting += 1
            if point.get_category() != "boundary":
                if counting % 2 == 0:
                    point.category = "outside"
                else:
                    point.category = "inside"
            pointlist_aftertest.append(point)
        return pointlist_aftertest


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
        point_set = self.read_file("input.csv")
        polygon_set = self.read_file("polygon.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "category"])
            for point in Judgement().pip_test(point_set, polygon_set):
                if point.get_category() == "outside":
                    writer.writerow([point.get_name(), "outside"])
                if point.get_category() == "inside":
                    writer.writerow([point.get_name(), "inside"])
                if point.get_category() == "boundary":
                    writer.writerow([point.get_name(), "boundary"])


def main():
    plotter = Plotter()
    file = File()
    judgement = Judgement()
    polygon_set = file.read_file("polygon.csv")
    point_set = file.read_file("input.csv")
    write_file = file.write_file("output.csv")
    print("read polygon.csv")
    print("read input.csv")
    sb = judgement.pip_test(point_set, polygon_set)
    print("categorize points")
    write_file
    print("write output.csv")
    x_polygon = []
    y_polygon = []
    for point in polygon_set:
        x_polygon.append(point.get_x())
        y_polygon.append(point.get_y())
    plotter.add_polygon(x_polygon, y_polygon)
    x_outside_list = []
    y_outside_list = []
    x_inside_list = []
    y_inside_list = []
    x_boundary_list = []
    y_boundary_list = []
    for point in sb:
        if point.get_category() == "outside":
            x_outside_list.append(point.get_x())
            y_outside_list.append(point.get_y())
        if point.get_category() == "inside":
            x_inside_list.append(point.get_x())
            y_inside_list.append(point.get_y())
        if point.get_category() == "boundary":
            x_inside_list.append(point.get_x())
            y_inside_list.append(point.get_y())
    plotter.add_point(x_outside_list, y_outside_list, "outside")
    plotter.add_point(x_inside_list, y_inside_list, "inside")
    plotter.add_point(x_boundary_list, y_boundary_list, "boundary")
    print("plot polygon and points")
    plotter.show()
    sb[0].category = "123"
    print(sb[0].get_category())


if __name__ == "__main__":
    main()