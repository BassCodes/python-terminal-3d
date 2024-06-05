# Alexander Bass
# Created 4/10/24
# Last Edited 6/5/24
import time
from math import sin
from point import Point, Rotator
from grass_donut import DonutEntity
from real_donut import RealDonutEntity
from entity import PointBlobEntity
from util import to_rad

WIDTH = 150
HEIGHT = 100
DEPTH = WIDTH
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT // 2
HALF_DEPTH = DEPTH // 2

NEGATIVE_DEPTH = -DEPTH


# Convert the world coordinate system to the screen coordinate system
def world_to_screen(p_x, p_y, p_z):
    s_x = round(p_x + HALF_WIDTH)
    s_y = round(p_y + HALF_HEIGHT)
    s_z = (p_z + HALF_DEPTH) / DEPTH
    return s_x, s_y, s_z


def format_grid(entities, screen):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            screen[y][x] = None

    for entity in entities:
        for p in entity.get_points():
            p_x, p_y, p_z = p.get_xyz()
            s_x, s_y, s_z = world_to_screen(p_x, p_y, p_z)
            if s_x in range(WIDTH) and s_y in range(HEIGHT):
                val = screen[s_y][s_x]
                if val is None:
                    red, green, blue = p.get_rgb()
                    screen[s_y][s_x] = (red, green, blue, s_z)
                elif val[3] < s_z:
                    red, green, blue = p.get_rgb()
                    screen[s_y][s_x] = (red, green, blue, s_z)

    s = ""
    last_color = (0, 0, 0)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            cell = screen[y][x]
            if cell is None or 0 > cell[3] > 255:
                s += "  "
                continue

            red, green, blue, depth = cell
            scale = depth
            red *= scale
            green *= scale
            blue *= scale
            if (red, green, blue) != last_color:
                s += f"\033[38;2;{round(red)};{round(green)};{round(blue)}m"
                last_color = (red, green, blue)
            s += "██"
        s += "\n"
    return s


def update_entities(entities, t):
    for e in entities:
        e.update(t)


class AxisEntity(PointBlobEntity):
    def __init__(self):
        self.points = []
        for x in range(WIDTH // 2 + 1):
            tx = x - WIDTH / 4
            for y in range(WIDTH // 2 + 1):
                ty = y - WIDTH / 4
                self.add_point(Point().set_xyz(0, tx, ty).set_color(1, 1, 0))

        r = (
            Rotator()
            .rotate_z(to_rad(80))
            .rotate_y(to_rad(30))
            .rotate_x(to_rad(30))
            .build()
        )

        self.rotate(r)

        self.rotor = Rotator().rotate_z(to_rad(0.6)).rotate_y(to_rad(0.06)).build()

    def update(self, t):
        t = t + 6 * 30

        self.rotate(self.rotor)
        for p in self.points:
            x, y, z = p.get_xyz()
            x, y = abs(x), abs(y)
            p.set_color(255 * abs(sin(x * t / 99)), 255 * abs(sin(y * t / 100)), 0)


class Origin(PointBlobEntity):
    def __init__(self):
        super().__init__()
        self.points = [Point().set_xyz(0, 0, 0).set_color(255, 0, 0)]


def main():
    entities = []
    # entities.append(AxisEntity())
    # entities.append(Origin())
    donut = RealDonutEntity()
    cube_donut = DonutEntity()

    for p in donut.points:
        p.translate_x(30)
    for p in cube_donut.points:
        p.translate_x(-30)
    entities.append(donut)
    entities.append(cube_donut)
    t = 1
    last_time = time.time()
    dt = 0

    grid = [[None for x in range(WIDTH)] for y in range(HEIGHT)]
    while True:
        print("\033c", end="")
        print(format_grid(entities, grid))

        update_entities(entities, t)
        current_time = time.time()
        dt = current_time - last_time
        wait = 1 / 45 - dt
        last_time = current_time
        time.sleep(max(wait, 0))

        t += 1 + 1 / 45 - dt


main()
