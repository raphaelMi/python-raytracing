# This module is responsible for rendering a scene.


import numpy as np
from geometry import *


MAX_RECURSION_DEPTH = 0
BACKGROUND_COLOR = np.array([0, 0, 0])


class Ray:
    # ray has information about
    def __init__(self, point, vector):
        self.point = point
        self.vector = vector*(1/np.linalg.norm(vector))

    def intersect(self, scene):
        # calculate the earliest intersection with a primitive of the scene

        nearest_dist = -1
        nearest_prim = 0
        nearest_point = np.array([0, 0, 0])

        for prim in scene.primitives:
            # we use intersection testing algorithms from
            # http://www.iquilezles.org/www/articles/intersectors/intersectors.htm

            if prim.kind == "SPHERE":

                origin_center = self.point - prim.points[0]
                b = np.dot(origin_center, self.vector)
                c = np.linalg.norm(origin_center)**2 - prim.radius**2
                h = b**2 - c
                if h >= 0.0:  # TODO check if this algorithm fails when ray origin is inside sphere
                    h = np.sqrt(h)
                    if nearest_dist > -b - h > 0:  # TODO check if isClose is needed
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

                if 1.0 >= u >= 0.0 and 1.0 >= v >= 0.0 and (u + v) <= 1.0:
                    if nearest_dist > t > 0:
                        nearest_dist = t
                        nearest_prim = prim
        if nearest_dist < 0:  # no intersection
            return

        nearest_point = nearest_dist*self.vector + self.point
        normal = np.array([0, 0, 0])
        if nearest_prim.kind == "SPHERE":
            normal = nearest_point - nearest_prim.points[0]
            normal = normal * (1/np.linalg.norm(normal))
        elif nearest_prim.kind == "TRIANGLE":
            normal = nearest_prim.normal

        return nearest_prim, nearest_point, nearest_dist, normal

    def evaluate(self, scene, recursion_depth):
        # evaluates chromaticity and brightness of a given ray recursively for a set depth of recursion
        # [1.0, 1.0, 1.0] is white
        try:
            prim, coord, length, normal = self.intersect(scene)
        except ValueError:
            # if ray did not make any intersection, return
            return BACKGROUND_COLOR, 0

        if prim.is_light_source:
            # if the ray hits a light source we can stop iterating
            return prim.color/length**2

        if recursion_depth > MAX_RECURSION_DEPTH:
            # rays die after exceeding depth of recursion
            return np.array([0.0, 0.0, 0.0])

        lights_source = []

        for light_prim in scene.lights:
            light_point = np.array([0, 0, 0])
            if light_prim.kind == "SPHERE":
                light_point = light_prim.points[0]
            elif light_prim.kind == "TRIANGLE":
                light_point = sum(light_prim.points)/3
            else:
                continue

            light_vector = light_point - coord
            c = Ray(coord, light_vector).evaluate(scene, 1)
            c = c*np.dot(normal, light_vector)/(np.linalg.norm(light_vector)*np.linalg.norm(normal))
            # intensity has to be scaled down relative to the angle

            lights_source.append(c)

        result_lights = [sum(lights_source)[k]*prim.color[k] for k in range(3)]

        return result_lights
        # if prim.shininess == 0.0:
        #    pass

        # TODO:
        # depending on the texture of the primitive, calculate more rays and combine result
        # light_reflection = Ray(coords, self.vector - 2*np.dot(self.vector,normal)*normal)
        #                       .evaluate(scene,recursion_depth+1)
        # light_source = Ray(coords, scene.light.coords - coords).eval...
        # light_diffuse = ...
        # light_refraction...
        # return np.quick_maffs(light...)


def ray_iterator(camera, resolution, block_number, total_blocks):
    # this function enables iteration through every pixel on the FOV
    # yield ray,(x,y)...

    half_fov_width = np.tan(camera.fov_width_angle/2)
    ratio = resolution[1]/resolution[0]
    half_fov_height = half_fov_width*ratio
    top_left = np.array([1, -half_fov_width, half_fov_height])
    down = np.array([0, 0, -2*half_fov_height])
    right = np.array([0, 2*half_fov_width, 0])

    for y in range(resolution[1]):
        for x in range(resolution[0]):

            yield Ray(camera.point, top_left + x/resolution[0]*right + y/resolution[1] * down), (x, y)


def render_scene(scene, **config):
    # iterates through all pixels in viewport, traces rays and draws to bitmap

    w = config["width"]
    h = config["height"]

    pixels = [[0, 0, 0]]*(w*h)

    for ray, pixel in ray_iterator(scene.camera, [w, h], 0, 1):
        color = ray.evaluate(scene, 0)
        color = np.clip(np.uint8(color*255), a_min=0, a_max=255)







