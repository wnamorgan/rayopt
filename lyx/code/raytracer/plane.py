import numpy as np
from raytracer.ray import Ray
from raytracer.element import Element
from raytracer.hit import Hit

class PlaneElement(Element):
    def __init__(self, point, normal, material, name):
        super().__init__(material, name)
        self.point = np.array(point)
        self._normal = np.array(normal) / np.linalg.norm(normal)
        #self.material = material

    def intersect(self, ray: Ray):
        un = self.normal(ray.origin)
        denom = np.dot(un, ray.direction)
        if np.abs(denom) < 1e-6:
            return None
        t = np.dot(self.point - ray.origin, un) / denom
        if t > 1e-6:
            return Hit(t, ray.point(t), un, self)
        return None
    
    def normal(self, point):
        return self._normal