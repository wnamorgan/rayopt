
import numpy as np
from abc import ABC, abstractmethod
from raytracer.ray import Ray
from raytracer.hit import Hit

# === SURFACE BEHAVIOR CLASSES ===
class Material(ABC):
    @abstractmethod
    def redirect(self, ray: Ray, hit: Hit):
        pass

class Reflective(Material):
    def redirect(self, ray: Ray, hit: Hit):
        d = ray.direction
        un = hit.normal
        reflected = d - 2 * np.dot(d, un) * un
        new_ray = Ray(hit.point + 1e-6 * reflected, reflected)
        return new_ray, True

class Absorbing(Material):
    def redirect(self, ray: Ray, hit: Hit):
        return None, False


class Refractive(Material):
    def __init__(self, n_top=1.0, n_bottom=1.0):
        self.n_top    = n_top
        self.n_bottom = n_bottom

    def resolve_material_context(self, ray, hit):
        d = ray.direction
        raw_normal = hit.normal

        if np.dot(d, raw_normal) < 0:
            u_n = raw_normal / np.linalg.norm(raw_normal)
            n1, n2 = self.n_top, self.n_bottom
        else:
            u_n = -raw_normal / np.linalg.norm(raw_normal)
            n1, n2 = self.n_bottom, self.n_top

        return u_n, n1, n2

    def redirect(self, ray, hit):
        u_n, n1, n2 = self.resolve_material_context(ray, hit)
        d = ray.direction
        cos_theta_i = -np.dot(u_n, d)
        sin2_theta_t = (n1 / n2)**2 * (1 - cos_theta_i**2)

        if sin2_theta_t > 1.0:
            # Total internal reflection
            reflected_dir = d + 2 * cos_theta_i * u_n
            return Ray(hit.point, reflected_dir), True

        cos_theta_t = np.sqrt(1 - sin2_theta_t)
        refracted_dir = (n1 / n2) * d + ((n1 / n2) * cos_theta_i - cos_theta_t) * u_n
        return Ray(hit.point, refracted_dir), True