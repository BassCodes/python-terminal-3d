# Alexander Bass
# Created 4/13/24
# Last Edited 4/13/24
class Entity:
    def update(self, t):
        pass


class PointBlobEntity(Entity):
    def __init__(self):
        super().__init__()
        self.points = []

    def get_points(self):
        return self.points

    def add_point(self, point):
        self.points.append(point)

    def rotate(self, transform):
        for p in self.points:
            p.rotate(transform)

    def set_points(self, points):
        self.points = points
