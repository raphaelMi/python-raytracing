# This module is responsible for rendering a scene.


import numpy as np


class Ray:
    # ray has information about
    def ___init___(self, x0, y0, z0, xdir, ydir, zdir):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.xdir = xdir
        self.ydir = ydir
        self.zdir = zdir

    def intersect(self, scene):
        # calculate the earliest intersection with a primitive of the scene
        pass
        # TODO
        # return primitive,coordinate,length

    def evaluate(self, scene, recursion_depth):
        # evaluates chromaticity and brightness of given ray recursively for a set depth of recursion
        prim,coord,length = self.intersect(scene)
        # TODO
        # depending on the texture of the primitive, calculate more rays and combine result
        # light_reflection = self.mirror(prim.normal).evaluate(scene,recursion_depth+1)
        # light_source = ray(coord,scene.light.coord).eval...
        # light_diffuse = ...
        # light_refraction...
        # return np.quick_maffs(light...)


def ray_iterator(self, camera):
    pass
    # this function enables iteration through every pixel on the FOV
    # yield ray,(x,y)...


def render_scene(scene, config):
    # iterates through all pixels in viewport, traces rays and draws to bitmap

    for ray,pixel in ray_iterator(scene.get_camera):
        (r, g, b) = ray.evaluate(ray, scene, 0)






