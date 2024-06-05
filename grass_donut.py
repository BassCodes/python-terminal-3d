# Alexander Bass
# Created 4/13/24
# Last Edited 6/5/24
from point import Point, Rotator
from util import to_rad
import ppm
from itertools import product
from entity import PointBlobEntity
import math


DIRT = ppm.load_ppm(open("dirt.ppm", "r"))
GRASS_TOP = ppm.load_ppm(open("grass_side.ppm", "r"))
GRASS_SIDE = ppm.load_ppm(open("grass_top.ppm", "r"))


def mix_color_transparency(left, right):
    for a in left:
        if a > 0:
            return left
    return right


def mul_color(a, b):
    return (a[0] * b[0], a[1] * b[1], a[2] * b[2])


def mul_color_scalar(a, b):
    return (a[0] * b, a[1] * b, a[2] * b)


def cube(dirt, g_sides, g_top, face_x, face_y):
    GRASS_COLOR_MUL = (0.4, 1, 0.4)
    out = []
    image_size = 16
    point_count = 20
    world_width = 16
    for x, y in product(range(point_count), range(point_count)):
        # Scale x and y to be from 0 to 1 to be later scaled back for any respective coordinate system
        x /= point_count
        y /= point_count

        dirt_color = dirt[round(y * image_size)][round(x * image_size)]
        top_col = g_top[round(y * image_size)][round(x * image_size)]
        grass_side_color = g_sides[int(y * image_size)][int(x * image_size)]
        grass_side_color = mul_color(grass_side_color, GRASS_COLOR_MUL)
        top_col = mul_color(top_col, GRASS_COLOR_MUL)

        side_color = mix_color_transparency(grass_side_color, dirt_color)

        b_red, b_green, b_blue = dirt_color

        t_red, t_green, t_blue = top_col

        s_red, s_green, s_blue = side_color

        x_w = x * world_width
        y_w = y * world_width
        w_w = world_width

        if face_x == -1 or face_x == 1 and face_y == 0:
            out.append(Point().set_xyz(0, x_w, y_w).set_color(s_red, s_green, s_blue))
        if face_x == 1 or face_x == -1 and face_y == 0:
            out.append(Point().set_xyz(w_w, x_w, y_w).set_color(s_red, s_green, s_blue))

        if face_y == -1 or face_y == 1 and face_x == 0:
            out.append(Point().set_xyz(x_w, 0, y_w).set_color(s_red, s_green, s_blue))
        if face_y == 1 or face_y == -1 and face_x == 0:
            out.append(Point().set_xyz(x_w, w_w, y_w).set_color(s_red, s_green, s_blue))

        # Top and bottom faces
        out.append(Point().set_xyz(x_w, y_w, w_w).set_color(b_red, b_green, b_blue))
        out.append(Point().set_xyz(x_w, y_w, 0).set_color(t_red, t_green, t_blue))

    for p in out:
        p.translate_x(face_x * world_width - world_width / 2)
        p.translate_y(face_y * world_width - world_width / 2)
        p.translate_z(-world_width / 2)
        p.rotate_z(to_rad(90))
        p.rotate_y(45 * 3)
        pass
    return out


class DonutEntity(PointBlobEntity):
    def __init__(self):
        super().__init__()
        points = []
        for x, y in product((-1, 0, 1), (-1, 0, 1)):
            if x == y == 0:
                continue
            points.extend(cube(DIRT, GRASS_TOP, GRASS_SIDE, x, y))
        self.set_points(points)

    def update(self, t):
        tf = Rotator()
        tf.rotate_y(math.cos(t / 25) * 0.05)
        tf.rotate_x(math.sin(t / 20) * 0.05 + 0.002)
        tf.build()
        for p in self.points:
            p.rotate(tf)
        pass

    def shift(self, x, y, z):
        for p in self.points:
            p.translate(x, y, z)
