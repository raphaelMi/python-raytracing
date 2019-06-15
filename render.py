#This module is responsible for rendering a scene.


import numpy as np

class Ray:
    def ___init___(self, x0, y0, z0, xdir, ydir, zdir):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.xdir = xdir
        self.ydir = ydir
        self.zdir = zdir


def ray_iterator():
    pass
    #this function enables smart iteration through every pixel on the FOV
    #yield ray...
