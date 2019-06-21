# This module is responsible for structuring the geometry and texture of a scene in a manageable way

import numpy as np


class Primitive:
    # stores a single triangle or sphere, along with texture and color data
    def __init__(self, point_a, radius=0.0, point_b=(0, 0, 0), point_c=(0, 0, 0)):
        # initializer for triangle primitives
        if radius > 0:
            self.kind = "SPHERE"
            self.points = [point_a]
            self.radius = radius
        elif radius == 0:
            self.kind = "TRIANGLE"
            self.points = [point_a, point_b, point_c]
            n = np.cross(point_b - point_a, point_c - point_a)
            self.normal = n*(1/np.linalg.norm(n))

        self.color = [255, 255, 255]
        self.shininess = 0
        self.is_transparent = False
        self.refractive_index = 1
        self.is_light_source = False
        self.light_intensity = 0.0


class Camera:
    # stores information about viewport and FOV
    def __init__(self):
        self.point = (0, 0, 0)
        self.fov_width_angle = 110
        self.fov_height_angle = 80


class Scene:
    # container for all primitives and camera
    def ___init___(self):
        self.primitives = {}
        self.light = {prim for prim in self.primitives if prim.is_light_source}


def read_scene_from_file(file):
    # reads scene from .obj file

    scene = 0

    return scene
