import numpy as np
from abc import ABC, abstractmethod
from ray import Ray
from hit import Hit

# === ABSTRACT ELEMENT CLASS ===
class Element(ABC):
    @abstractmethod
    def intersect(self, ray: Ray):
        pass

    @abstractmethod
    def redirect(self, ray: Ray, hit: Hit):
        pass
