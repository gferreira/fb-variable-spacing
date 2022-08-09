from __future__ import division
import random
from math import sin, cos, radians, degrees, sqrt, atan, acos

'''
This is the `progvis.modules.vector` module.

The module supplies functions for calculations with vectors.

>>> getVector((0, 0), (500, 500))
    (707.1067811865476, 45.0)

'''

def getVector(p1, p2):
    '''
    Get the distance and angle between two `x,y` points.

    >>> getVector((0, 0), (500, 500))
    (707.1067811865476, 45.0)

    >>> getVector((0, 0), (200, 500))
    (538.5164807134504, 68.19859051364818)

    '''

    # unpack x,y tuples
    x1, y1 = p1
    x2, y2 = p2

    # get catheti (aka legs)
    w = x2 - x1
    h = y2 - y1

    # get hypotenuse
    distance = sqrt(w ** 2 + h ** 2)

    # get angle (in degrees)
    if w != 0:
        angleRadians = atan(float(h) / w)
        angleDegrees = degrees(angleRadians)
    else:
        angleDegrees = 0

    # done!
    return distance, angleDegrees

def vector(pos, distance, angle):
    '''
    Calculate a new `x,y` position based on a given distance and angle (in degrees).

    >>> vector((0, 0), 125, 45)
    (88.38834764831844, 88.38834764831843)

    >>> p1 = (200, 500)
    >>> distance, angle = getVector((0, 0), p1)
    >>> p2 = vector((0, 0), distance, angle)

    >>> p1
    (200, 500)

    >>> p2
    (200.00000000000003, 500.0)

    '''
    x, y = pos
    x += cos(radians(angle)) * distance
    y += sin(radians(angle)) * distance
    return x, y

def getAngle(a, b, c):
    '''
    Get the angle between three sides of a triangle.

    '''
    angleRadians = acos((c ** 2 - b ** 2 - a ** 2) / (-2.0 * a * b))
    angleDegrees = degrees(angleRadians)
    return angleDegrees

def constrain(value, minValue, maxValue):
    '''
    Constrain a value between two values.

    '''
    if value < minValue:
        return minValue
    elif value > maxValue:
        return maxValue
    else:
        return value

def mapValue(value, start1, stop1, start2, stop2):
    range1 = stop1 - start1
    range2 = stop2 - start2
    factor = range2 / range1
    return start2 + (value * factor)

if __name__ == '__main__':

    import sys
    print(sys.version)

    import doctest
    doctest.testmod()
