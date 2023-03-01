"""
This script contains common utility functions used in the project.
"""

from loadPoints import Point


def getDistance(point1: Point, point2: Point):
    """
        This method calculates the distance between two points.
        It takes two points as arguments and returns the distance between them.
    """
    return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)**.5
