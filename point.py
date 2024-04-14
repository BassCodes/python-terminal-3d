# Alexander Bass
# Created 4/13/24
# Last Edited 4/13/24
from math import cos, sin


class Point:
    def __init__(self):
        self.__color = (1, 1, 1)
        self.__x, self.__y, self.__z = 0, 0, 0

    def set_xyz(self, x, y, z):
        self.__x, self.__y, self.__z = x, y, z
        return self

    def rotate_x(self, angle):
        cos_a = cos(angle)
        sin_a = sin(angle)
        y_1 = self.__y * cos_a - self.__z * sin_a
        z_1 = self.__y * sin_a + self.__z * cos_a
        self.set_xyz(self.__x, y_1, z_1)
        return self

    def rotate_z(self, angle):
        cos_a = cos(angle)
        sin_a = sin(angle)

        x_1 = self.__x * cos_a - self.__y * sin_a
        y_1 = self.__x * sin_a + self.__y * cos_a
        self.set_xyz(x_1, y_1, self.__z)
        return self

    def rotate_y(self, angle):
        cos_a = cos(angle)
        sin_a = sin(angle)

        x_1 = self.__x * cos_a + self.__z * sin_a
        z_1 = self.__z * cos_a - self.__x * sin_a
        self.set_xyz(x_1, self.__y, z_1)
        return self

    def translate(self, x, y, z):
        self.__x += x
        self.__y += y
        self.__z += z

    def translate_x(self, x):
        self.__x += x

    def translate_y(self, y):
        self.__y += y

    def translate_z(self, z):
        self.__z += z

    def get_xyz(self):
        return (self.__x, self.__y, self.__z)

    def rotate(self, transform):
        x_n, y_n, z_n = transform.run(*self.get_xyz())
        self.set_xyz(x_n, y_n, z_n)

    def get_rgb(self):
        return self.__color

    def set_color(self, r, g, b):
        if r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b < 0:
            raise ValueError("Color is greater than 255 or less than 0")
        self.__color = (r, g, b)
        return self


class Rotator:
    def __init__(self):
        self.__alpha = 0.0
        self.__beta = 0.0
        self.__gamma = 0.0

        self.__sin_alpha = 0.0
        self.__cos_alpha = 0.0
        self.__sin_beta = 0.0
        self.__cos_beta = 0.0
        self.__sin_gamma = 0.0
        self.__cos_gamma = 0.0

    def rotate_x(self, angle):
        self.__alpha += angle
        return self

    def rotate_y(self, angle):
        self.__beta += angle
        return self

    def rotate_z(self, angle):
        self.__gamma += angle
        return self

    def build(self):
        self.__sin_alpha = sin(self.__alpha)
        self.__cos_alpha = cos(self.__alpha)
        self.__sin_beta = sin(self.__beta)
        self.__cos_beta = cos(self.__beta)
        self.__sin_gamma = sin(self.__gamma)
        self.__cos_gamma = cos(self.__gamma)
        return self

    def run(self, xI, yI, zI):
        x_0 = xI
        y_0 = yI
        z_0 = zI

        x_1, y_1 = 0, 0

        # if self.__alpha != 0.0:
        y_1 = y_0 * self.__cos_alpha - z_0 * self.__sin_alpha
        z_0 = y_0 * self.__sin_alpha + z_0 * self.__cos_alpha
        y_0 = y_1

        # if self.__beta != 0.0:
        x_1 = x_0 * self.__cos_beta + z_0 * self.__sin_beta
        z_0 = z_0 * self.__cos_beta - x_0 * self.__sin_beta
        x_0 = x_1

        # if self.__gamma != 0.0:
        x_1 = x_0 * self.__cos_gamma - y_0 * self.__sin_gamma
        y_0 = x_0 * self.__sin_gamma + y_0 * self.__cos_gamma
        x_0 = x_1

        return x_0, y_0, z_0
