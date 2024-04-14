# Alexander Bass
# Created 4/13/24
# Last Edited 4/13/24
from math import sin, cos, atan2, acos, sqrt
import math


def to_rad(deg):
    return math.pi * deg / 180.0


def sign(f):
    if f == 0:
        return f

    return f / math.fabs(f)


def to_cart(r, theta, phi):
    y = r * sin(theta) * cos(phi)
    x = r * cos(theta)
    z = r * sin(theta) * sin(phi)
    return x, y, z


def to_spherical(x, y, z):
    r = sqrt(x**2 + y**2 + z**2)
    theta = acos(z / r)
    x = x if x != 0 else 1
    phi = math.atan(y / x)
    return r, theta, phi
