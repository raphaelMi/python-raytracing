#This module is responsible for structuring the geometry and texture of a scene in a manageable way

import numpy as np

class Primitive:
    #stores a single triangle or sphere, along with texture and color data
    pass

class Camera:
    def ___init___(self):
        pass

    def set_position(self,x,y,z):
        self.x0 = x
        self.y0 = y
        self.z0 = z

    def set_FOV(self,width_angle,height_angle):
        self.width_angle = width_angle
        self.height_angle = height_angle