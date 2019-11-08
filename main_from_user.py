import argparse
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
    # The Minimum Bounding Rectangle Algorithm.
    def __init__(self, name, polylist):
        length = len(polylist)
        top = down = left = right = polylist[0]
        # Get four vertices of the MBR.
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


# The Point-in-Polygon Algorithm.
class Judgement:
    # Determine whether the point is inside the MBR.
    def is_point_in_mbr(self, point, mbr):
        if mbr[3].get_x() <= point.get_x() <= mbr[0].get_x() and \
                mbr[3].get_y() <= point.get_y() <= mbr[2].get_y():
            return True
        else:
            return False

    # Determine whether the point set is inside the polygon.
    # Return a point set that each point have "category" attribute.
    def pip_test(self, pointlist, polylist):
        mbr = MBR("polygon", polylist).get_mbr()
        pointlist_aftertest = []
        for point in pointlist:
            # Determine whether the point is inside the MBR.
            if not self.is_point_in_mbr(point, mbr):
                point.define_category("outside")
                pointlist_aftertest.append(point)
                continue
            # The Ray Casting Algorithm.
            lines = Polygon("polygonlines", polylist).lines()
            p_x = point.get_x()
            p_y = point.get_y()
            counting = 0
            for line in lines:
                p1_x = line.point_1.get_x()
                p1_y = line.point_1.get_y()
                p2_x = line.point_2.get_x()
                p2_y = line.point_2.get_y()
                # Point coincides with the vertices of the polygon.
                if (p_x == p1_x and p_y == p1_y) or (p_x == p2_x and p_y == p2_y):
                    point.define_category("boundary")
                    break
                # Point is on the boundaries that are parallel with X axis.
                if p1_y == p_y == p2_y:
                    if (p1_x < p_x < p2_x) or (p2_x < p_x < p1_x):
                        point.define_category("boundary")
                        break
                # Determine whether the end points of the line segment are on either side of the ray.
                if (p1_y < p_y <= p2_y) or (p2_y < p_y <= p1_y):
                    # The x-coordinate of a point on a line segment that has same y-coordinate with the ray.
                    x = p2_x - (p2_y - p_y) * (p2_x - p1_x) / (p2_y - p1_y)
                    # Point is on the boundary of the polygon.
                    if x == p_x:
                        point.define_category("boundary")
                        break
                    # The ray pass through the boundary of the polygon.
                    if x > p_x:
                        counting += 1
            # Determine whether the number of intersections is even.
            if point.get_category() != "boundary":
                if counting % 2 == 0:
                    point.define_category("outside")
                else:
                    point.define_category("inside")
            pointlist_aftertest.append(point)
        return pointlist_aftertest


class File:
    # Read file by using "DictReader" function, return point set.
    def read_file(self, filename=""):
        with open(filename, "r") as f:
            pointlist = []
            for i in f.readlines()[1:]:
                point = i.split(",")
                id = point[0]
                x = float(point[1])
                y = float(point[2])
                point1 = Point(id, x, y)
                pointlist.append(point1)
        return pointlist

    # Read tuple_pairs given by user, return point set.
    def read_from_user(self, tuple_pairs):
        points = tuple_pairs.split("(")
        pointslist = []
        for i in points[1:]:
            id_num = i
            x = float(i[0])
            y = float(i[2])
            point = Point(id_num, x, y)
            pointslist.append(point)
        return pointslist

    # Print result on screen.
    def print_on_screen(self, point_aftertest):
        for i in point_aftertest:
            point = (i.get_x(), i.get_y())
            category = i.get_category()
            if category == "outside":
                print("point" + str(point) + ": outside the polygon" + "\n")
            if category == "inside":
                print("point" + str(point) + ": inside the polygon" + "\n")
            if category == "boundary":
                print("point" + str(point) + ": on the boundary" + "\n")


class PlotterAssistant:
    # Extract x-coordinates and y-coordinates of the polygon.
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

    # Extract x-coordinates and y-coordinates of points after PiP test.
    # Return coordinates based on category of each point.
    def extract_point(self, point_aftertest, category, name):
        x_outside_list = []
        y_outside_list = []
        x_inside_list = []
        y_inside_list = []
        x_boundary_list = []
        y_boundary_list = []
        for i in point_aftertest:
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


# Run the Point-in-Polygon Test and plot polygon and points.
# Pass a tuple pairs given by user as an argument to the function.
def main(tuple_pairs):
    plotter = Plotter()

    print("read polygon.csv")
    file = File()
    polygon_set = file.read_file("polygon.csv")

    print("Insert point information")
    point_set = file.read_from_user(tuple_pairs)

    print("categorize points")
    judge = Judgement()
    point_aftertest = judge.pip_test(point_set, polygon_set)
    file.print_on_screen(point_aftertest)

    print("plot polygon and points")
    x_polygon = PlotterAssistant().extract_polygon(polygon_set, "xs")
    y_polygon = PlotterAssistant().extract_polygon(polygon_set, "ys")
    plotter.add_polygon(x_polygon, y_polygon)

    # Plot points based on category of each point
    x_outside_list = PlotterAssistant().extract_point(point_aftertest, "outside", "xs")
    y_outside_list = PlotterAssistant().extract_point(point_aftertest, "outside", "ys")
    plotter.add_point(x_outside_list, y_outside_list, "outside")

    x_inside_list = PlotterAssistant().extract_point(point_aftertest, "inside", "xs")
    y_inside_list = PlotterAssistant().extract_point(point_aftertest, "inside", "ys")
    plotter.add_point(x_inside_list, y_inside_list, "inside")

    x_boundary_list = PlotterAssistant().extract_point(point_aftertest, "boundary", "xs")
    y_boundary_list = PlotterAssistant().extract_point(point_aftertest, "boundary", "ys")
    plotter.add_point(x_boundary_list, y_boundary_list, "boundary")

    plotter.show()


# Use "argparse" library to get argument.
# (Source: Codelog. 2019. https://codeday.me/bug/20190429/1003501.html)
parser = argparse.ArgumentParser(description="Welcome to Zongshi's Point-in-Polygon Test! \n"
                                             "Please enter the points as tuple pairs as argument\n"
                                             "Remember! The coordinates you given should follow the structure:\n"
                                             "(x1,y1)(x2,y2)(x3,y3)(x4,y4).......\n"
                                             "The result will be shown by following structure: \n"
                                             "point(x1, y1): outside the polygon.\n"
                                             "point(x2, y2): inside the polygon.\n"
                                             "point(x3, y3): on the boundary.\n")
# Get "tuple_pairs" argument.
parser.add_argument("tuple_pairs",
                    help="tuple_pairs, required arguments")
args = parser.parse_args()


if __name__ == "__main__":
    # Run program, print wrong message when program do not work.
    try:
        main(args.tuple_pairs)
    except Exception as e:
        print(e)



