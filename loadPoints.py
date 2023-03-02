"""
This script loads all the points from the points.csv file and converts them to objects of the Point class.
Usage:
    ```python
        from loadPoints import points
        # get the point with name "point1"
        point1 = points["point1"] # returns the Point object
    ```
"""
import csv



class Point:
    def __init__(self, name, x, y, z, rx, ry, rz):
        self.name = name

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.rx = float(rx)
        self.ry = float(ry)
        self.rz = float(rz)

    def __str__(self):
        return f"{self.name}: ({self.x}, {self.y}, {self.z}, {self.rx}, {self.ry}, {self.rz})"

    __repr__ = __str__

    def pose(self):
        return [self.x, self.y, self.z, self.rx, self.ry, self.rz]


# load the points from the csv file into dictionary
print("Loading points...")
points = {point[0]: Point(point[0], point[1], point[2], point[3], point[4],
                          point[5], point[6]) for point in csv.reader(open("points.csv")) if point[0] != "name"}

print(*points.values(), sep='\n')

