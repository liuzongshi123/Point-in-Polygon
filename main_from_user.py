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

    def define_category(self, name):
        self.__category = name


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
                point.define_category("outside")
                pointlist_aftertest.append(point)
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
                    point.define_category("boundary")
                    break
                if p1_y == p_y == p2_y:
                    if (p1_x < p_x < p2_x) or (p2_x < p_x < p1_x):
                        point.define_category("boundary")
                        break
                if (p1_y < p_y <= p2_y) or (p2_y < p_y <= p1_y):
                    x = p2_x - (p2_y - p_y) * \
                        (p2_x - p1_x) / (p2_y - p1_y)
                    if x == p_x:
                        point.define_category("boundary")
                        break
                    if x > p_x:
                        counting += 1
            if point.get_category() != "boundary":
                if counting % 2 == 0:
                    point.define_category("outside")
                else:
                    point.define_category("inside")
            pointlist_aftertest.append(point)
        return pointlist_aftertest


class File:
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

    def print_on_screen(self, pointlist, polylist):
        points_aftertest = Judgement().pip_test(pointlist, polylist)
        for i in points_aftertest:
            point = (i.get_x(), i.get_y())
            category = i.get_category()
            if category == "outside":
                print("point" + str(point) + ": outside the polygon" + "\n")
            if category == "inside":
                print("point" + str(point) + ": inside the polygon" + "\n")
            if category == "boundary":
                print("point" + str(point) + ": on the boundary" + "\n")


class Extractor:
    def extract_polygon(self, polylist, name):
        x_polygon = []
        y_polygon = []
        for point in polylist:
            x_polygon.append(point.get_x())
            y_polygon.append(point.get_y())
        if name == "xs":
            return x_polygon
        if name == "ys":
            return y_polygon

    def extract_point(self, point_set, polygon_set, category, name):
        points_aftertest = Judgement().pip_test(point_set, polygon_set)
        x_outside_list = []
        y_outside_list = []
        x_inside_list = []
        y_inside_list = []
        x_boundary_list = []
        y_boundary_list = []
        for i in points_aftertest:
            if i.get_category() == "outside":
                x_outside_list.append(i.get_x())
                y_outside_list.append(i.get_y())
            if i.get_category() == "inside":
                x_inside_list.append(i.get_x())
                y_inside_list.append(i.get_y())
            if i.get_category() == "boundary":
                x_boundary_list.append(i.get_x())
                y_boundary_list.append(i.get_y())
        if category == "outside" and name == "xs":
            return x_outside_list
        if category == "outside" and name == "ys":
            return y_outside_list
        if category == "inside" and name == "xs":
            return x_inside_list
        if category == "inside" and name == "ys":
            return y_inside_list
        if category == "boundary" and name == "xs":
            return x_boundary_list
        if category == "boundary" and name == "ys":
            return y_boundary_list


def main(tuple_pairs):
    plotter = Plotter()

    print("read polygon.csv")
    file = File()
    polygon_set = file.read_file("polygon.csv")
    print("Insert point information")
    tuple_pairs
    print("categorize points")
    file.print_on_screen(tuple_pairs, polygon_set)
    print("plot polygon and points")
    x_polygon = Extractor().extract_polygon(polygon_set, "xs")
    y_polygon = Extractor().extract_polygon(polygon_set, "ys")
    plotter.add_polygon(x_polygon, y_polygon)

    x_outside_list = Extractor().extract_point(tuple_pairs, polygon_set, "outside", "xs")
    y_outside_list = Extractor().extract_point(tuple_pairs, polygon_set, "outside", "ys")
    plotter.add_point(x_outside_list, y_outside_list, "outside")

    x_inside_list = Extractor().extract_point(tuple_pairs, polygon_set, "inside", "xs")
    y_inside_list = Extractor().extract_point(tuple_pairs, polygon_set, "inside", "ys")
    plotter.add_point(x_inside_list, y_inside_list, "inside")

    x_boundary_list = Extractor().extract_point(tuple_pairs, polygon_set, "boundary", "xs")
    y_boundary_list = Extractor().extract_point(tuple_pairs, polygon_set, "boundary", "ys")
    plotter.add_point(x_boundary_list, y_boundary_list, "boundary")

    plotter.show()


if __name__ == "__main__":
    print("Welcome to Zongshi's Point-in-Polygon Test! \n"
          "Remember! The coordinates you given should follow the structure:\n"
          "(x1,y1), (x2,y2), (x3,y3), (x4,y4).......\n"
          "The result will be shown by following structure: \n"
          "point(x1, y1): outside the polygon.\n"
          "point(x2, y2): inside the polygon.\n"
          "point(x3, y3): on the boundary.\n")
    points = eval(input("Please enter the points: "))
    while isinstance(points, tuple) is False:
        print("Type in wrong way! Please try again!")
        points = eval(input("Please enter the points: "))
    pointslist = []
    if isinstance(points[0], tuple):
        for i in range(len(points)):
            id_num = i
            x = float(points[i][0])
            y = float(points[i][1])
            point = Point(id_num, x, y)
            pointslist.append(point)
    else:
        id_num = 0
        x = float(points[0])
        y = float(points[1])
        point = Point(id_num, x, y)
        pointslist.append(point)
    tuple_pairs = pointslist

    main(tuple_pairs)
