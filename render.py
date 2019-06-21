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

        nearest_dist = -1
        nearest_prim = 0
        nearest_point = (0, 0, 0)

        for prim in scene.primitives:
            # we use intersection testing algorithms from
            # http://www.iquilezles.org/www/articles/intersectors/intersectors.htm

            if prim.kind == "SPHERE":

                origin_center = self.point - prim.points[0]
                b = np.dot(origin_center, self.vector)
                c = np.linalg.norm(origin_center)**2 - prim.radius**2
                h = b**2 - c
                if h >= 0.0: # TODO check if this algorithm fails when ray origin is inside sphere
                    h = np.sqrt(h)
                    if nearest_dist > -b - h >= 0:
                        nearest_dist = -b - h
                        nearest_prim = prim

            elif prim.kind == "TRIANGLE":

                v0v1 = prim.points[1] - prim.points[0]
                v0v2 = prim.points[2] - prim.points[0]
                rov0 = self.point - prim.points[0]

                n = np.cross(v0v1, v0v2)

                q = np.cross(rov0, self.vector)

                d = 1.0 / np.dot(self.vector, n)

                u = d * np.dot(-q, v0v2)
                v = d * np.dot(q, v0v1)
                t = d * np.dot(-n, rov0)

                if 1.0 >= u >= 0.0 and 1.0 >= v >= 0.0 and (u + v) <= 1.0 :
                    if nearest_dist > t >= 0:
                        nearest_dist = t
                        nearest_prim = prim
            # TODO calculate intersection point based on nearest prim
        return
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






