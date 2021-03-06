# This module is responsible for structuring the geometry and texture of a scene in a manageable way

import numpy as np
from itertools import chain

KIND_TRIANGLE = 1
KIND_SPHERE = 2

COLOR_RED = np.array([1, 0, 0])
COLOR_GREEN = np.array([0, 1, 0])
COLOR_BLUE = np.array([0, 0, 1])


class Primitive:
    # stores a single triangle or sphere, along with texture and color data
    def __init__(self, point_a, radius=0.0, point_b=np.array([0, 0, 0]), point_c=np.array([0, 0, 0])):
        # initializer for triangle primitives
        if radius > 0:
            self.kind = KIND_SPHERE
            self.points = [np.array(point_a)]
            self.radius = radius
        elif radius == 0:
            self.kind = KIND_TRIANGLE
            point_a = np.array(point_a)
            point_b = np.array(point_b)
            point_c = np.array(point_c)
            v0v1 = np.array(point_b - point_a)
            v0v2 = np.array(point_c - point_a)
            self.points = [point_a, point_b, point_c, sum(np.array([point_a, point_b, point_c])) / 3, v0v1, v0v2,
                           np.cross(v0v1, v0v2)]
            n = np.cross(self.points[1] - self.points[0], self.points[2] - self.points[0])
            self.normal = n * (1 / np.linalg.norm(n))

        self.color = np.array([1, 1, 1])
        self.specular = 1
        self.shininess = 0
        self.is_transparent = False
        self.refractive_index = 1
        self.is_light_source = False
        self.is_reflective = False


class Camera:
    # stores information about viewport and FOV
    # position does not currently determine viewport

    def __init__(self):
        self.point = np.array([0, 0, 0])
        self.fov_width_angle = 70
        self.view_vector = np.array([1, 0, 0])


class Scene:
    # container for all primitives and camera
    def __init__(self, primitives):
        self.primitives = primitives
        self.lights = {prim for prim in chain.from_iterable([frozenset(s) for s in primitives.values()]) if prim.is_light_source}
        self.camera = Camera()

    def add_primitive(self, prim):
        self.primitives.update()
        if prim.is_light_source:
            self.lights.add(prim)

