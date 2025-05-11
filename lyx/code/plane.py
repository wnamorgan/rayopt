import numpy as np
from ray import Ray
from element import Element
from hit import Hit

class PlaneElement(Element):
    def __init__(self, point, normal, behavior):
        self.point = np.array(point)
        self.normal = np.array(normal) / np.linalg.norm(normal)
        self.behavior = behavior

    def intersect(self, ray: Ray):
        denom = np.dot(self.normal, ray.direction)
        if np.abs(denom) < 1e-6:
            return None
        t = np.dot(self.point - ray.origin, self.normal) / denom
        if t > 1e-6:
            return Hit(t, ray.point(t), self.normal, self)
        return None

    def redirect(self, ray: Ray, hit: Hit):
        return self.behavior.redirect(ray, hit)