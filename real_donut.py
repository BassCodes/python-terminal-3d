# Alexander Bass
# Created 4/13/24
# Last Edited 4/13/24
from point import Point, Rotator
from util import to_rad
from entity import PointBlobEntity
from math import sin, cos

RADIUS = 10
DISTANCE = 15
POINTS_PER_CIRCLE = 70
NUMBER_CIRCLES = 360


class RealDonutEntity(PointBlobEntity):
    def __init__(self):
        super().__init__()
        points = []
        rot = Rotator().rotate_x(to_rad(-30))
        rot.build()
        for phi_t in range(NUMBER_CIRCLES):
            phi_percent = phi_t / NUMBER_CIRCLES
            phi = phi_percent * 360
            temp_points = []
            for theta in range(POINTS_PER_CIRCLE):
                percent_theta = theta / POINTS_PER_CIRCLE
                theta = percent_theta * 360
                x = DISTANCE + RADIUS * cos(to_rad(theta))
                y = RADIUS * sin(to_rad(theta))
                new_point = Point().set_xyz(x, y, 0).set_color(255, 255, 0)
                # temp_points
                new_point.rotate_y(to_rad(phi))
                temp_points.append(new_point)
            points.extend(temp_points)
            temp_points.clear()
        for p in points:
            p.rotate(rot)
        self.set_points(points)

    def update(self, t):
        tf = Rotator()
        tf.rotate_y(0.03)
        tf.rotate_x(0.02 * cos(t / 120))
        tf.build()
        for p in self.points:
            p.rotate(tf)

    def shift(self, x, y, z):
        for p in self.points:
            p.translate(x, y, z)
