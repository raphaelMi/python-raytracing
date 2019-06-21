# This module is responsible for structuring the geometry and texture of a scene in a manageable way

import numpy as np


class Primitive:
    # stores a single triangle or sphere, along with texture and color data
    def __init__(self, point_a, radius=0.0, point_b=np.array([0, 0, 0]), point_c=np.array([0, 0, 0])):
        # initializer for triangle primitives
        if radius > 0:
            self.kind = "SPHERE"
            self.points = [np.array(point_a)]
            self.radius = radius
        elif radius == 0:
            self.kind = "TRIANGLE"
            self.points = [np.array(point_a), np.array(point_b), np.array(point_c)]
            n = np.cross(self.points[1] - self.points[0], self.points[2] - self.points[0])
            self.normal = n*(1/np.linalg.norm(n))

        self.color = [255, 255, 255]
        self.shininess = 0
        self.is_transparent = False
        self.refractive_index = 1
        self.is_light_source = False


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
        self.lights = {prim for prim in self.primitives if prim.is_light_source}
        self.camera = Camera()

    def add_primitive(self,prim):
        self.primitives.add(prim)
        if prim.is_light_source:
            self.lights.add(prim)


def read_scene_from_file(file):
    # reads scene from .obj file

    scene = 0

    return scene
