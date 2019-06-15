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
            if point_b == point_c:
                self.kind = "POINT"
                self.points = [point_a]
            else:
                self.kind = "TRIANGLE"
                self.points = [point_a, point_b, point_c]

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
        self.width_angle = 110
        self.height_angle = 80

    def set_position(self, coords):
        self.point = coords

    def set_fov(self, width_angle, height_angle):
        self.width_angle = width_angle
        self.height_angle = height_angle


class Scene:
    # container for all primitives and camera
    def ___init___(self):
        pass


def read_scene_from_file(file):
    # reads scene from .obj file

    scene = 0

    return scene
