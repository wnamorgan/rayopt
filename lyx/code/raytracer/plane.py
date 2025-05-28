import numpy as np
from raytracer.ray import Ray
from raytracer.element import Element
from raytracer.hit import Hit

class PlaneElement(Element):
    def __init__(self, center, orientation, material, name):
        super().__init__(material, center, orientation, name)

    def intersect(self, ray_global: Ray):
        ray_local = self.ray_local_from_global(ray_global)
        un_local = self.normal()
        denom = np.dot(un_local, ray_local.direction)
        if np.abs(denom) < 1e-6:
            return None
        t = -np.dot(ray_local.origin, un_local) / denom
        if t > 1e-6:
            point_local = ray_local.point(t)
            point_global = self.center + np.dot(self.R_G_from_L,point_local)
            un_global = np.dot(self.R_G_from_L,un_local)
            return Hit(t, point_global, un_global, self)
        return None
    
    def normal(self, point=None):
        un_local = np.array([0,0,1])
        return un_local