# This module is responsible for rendering a scene.


import numpy as np
import geometry


MAX_RECURSION_DEPTH = 4
BACKGROUND_COLOR = [0, 0, 0]


class Ray:
    # ray has information about
    def __init__(self, point, vector):
        self.point = point
        self.vector = vector

    def intersect(self, scene):
        # calculate the earliest intersection with a primitive of the scene
        if np.linalg.norm(self.vector) == 0:
            print("Rays must have valid direction")
            return
        return geometry.Primitive(), (0, 0, 0), 1.0
        # TODO
        # return primitive,coordinates,length

    def evaluate(self, scene, recursion_depth):
        # evaluates chromaticity and brightness of a given ray recursively for a set depth of recursion
        try:
            prim, coord, length = self.intersect(scene)
        except ValueError:
            # if ray did not make any intersection, return
            return BACKGROUND_COLOR, 0

        if prim.is_light_source:
            # if the ray hits a light source we can stop iterating
            return prim.color, prim.light_intensity/length**2

        if recursion_depth > MAX_RECURSION_DEPTH:
            # rays die after exceeding depth of recursion
            return [0, 0, 0], 0.0

        if prim.shininess == 0.0:
            pass

        # TODO
        # depending on the texture of the primitive, calculate more rays and combine result
        # light_reflection = Ray(coords, self.vector - 2*np.dot(self.vector,prim.normal)*prim.normal)
        #                       .evaluate(scene,recursion_depth+1)
        # light_source = Ray(coords, scene.light.coords - coords).eval...
        # light_diffuse = ...
        # light_refraction...
        # return np.quick_maffs(light...)


def ray_iterator(camera, block_number, total_blocks):
    yield Ray((0, 0, 0), (1, 0, 0)), (0, 0)
    # this function enables iteration through every pixel on the FOV
    # yield ray,(x,y)...


def render_scene(scene, config):
    # iterates through all pixels in viewport, traces rays and draws to bitmap

    for ray, pixel in ray_iterator(scene.get_camera, 0, 1):
        color, intensity = ray.evaluate(ray, scene, 0)






