import numpy as np
from abc import ABC, abstractmethod
from raytracer.ray import Ray
from raytracer.hit import Hit

# === ABSTRACT ELEMENT CLASS ===
class Element(ABC):
    @abstractmethod
    def intersect(self, ray: Ray):
        pass

    @abstractmethod
    def redirect(self, ray: Ray, hit: Hit):
        pass

class Element(ABC):
    def __init__(self, material, name='element'):
        self.material = material
        self.name = name

    @abstractmethod
    def intersect(self, ray):
        pass

    @abstractmethod
    def normal(self, point):
        pass

    def redirect(self, ray, hit):
        return self.material.redirect(ray, hit)