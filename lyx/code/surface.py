
import numpy as np
from abc import ABC, abstractmethod
from ray import Ray
from hit import Hit

# === SURFACE BEHAVIOR CLASSES ===
class SurfaceBehavior(ABC):
    @abstractmethod
    def redirect(self, ray: Ray, hit: Hit):
        pass

class Reflective(SurfaceBehavior):
    def redirect(self, ray: Ray, hit: Hit):
        d = ray.direction
        n = hit.normal
        reflected = d - 2 * np.dot(d, n) * n
        new_ray = Ray(hit.point + 1e-6 * reflected, reflected)
        return new_ray, True

class Absorbing(SurfaceBehavior):
    def redirect(self, ray: Ray, hit: Hit):
        return None, False