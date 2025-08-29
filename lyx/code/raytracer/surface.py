
import numpy as np
from abc import ABC, abstractmethod
from raytracer.ray import Ray
from raytracer.hit import Hit

# === SURFACE BEHAVIOR CLASSES ===
class Material(ABC):
    @abstractmethod
    def redirect(self, ray: Ray, hit: Hit):
        pass

    @staticmethod
    def CPM(v):
        v = v.reshape(3)
        return np.array([[  0.0, -v[2],  v[1]],
                         [ v[2],   0.0, -v[0]],
                         [-v[1],  v[0],   0.0]])

class Reflective(Material):
    def redirect(self, ray: Ray, hit: Hit):
        d = ray.direction
        un = hit.normal
        reflected = d - 2 * np.dot(d, un) * un
        new_ray = Ray(hit.point + 1e-6 * reflected, reflected)
        return new_ray, True

class Absorbing(Material):
    def redirect(self, ray, hit):
        new_ray = Ray(hit.point,ray.direction)
        return new_ray, False


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
    
class Diffuse(Refractive):
    def __init__(self, n_top=1.0, n_bottom=1.0, sigma_deg = 10.0):
        self.sigma_deg = sigma_deg
        super().__init__(n_top, n_bottom)
    
    @staticmethod
    def Rodriguez(v_in,u,theta):
        K = Material.CPM(u)
        R = np.eye(3) + np.sin(theta)*K + (1.0 - np.cos(theta))*(K @ K)
        v_out = R @ v_in
        return v_out
    

    
    def redirect(self,ray,hit):
        refracted_ray, _ = super().redirect(ray,hit)
        d = refracted_ray.direction
        raw_normal = hit.normal

        dir = np.dot(d, raw_normal)
        leaving = (dir>0 and self.n_top<self.n_bottom) or (dir<0 and self.n_top>self.n_bottom)
        if leaving: # Leaving material => apply scatter
            if raw_normal[0] < 0.9:
                temp = np.array([1.0, 0.0, 0.0]).reshape(3,1)
            else:
                temp = np.array([0.0, 1.0, 0.0]).reshape(3,1)

            u1 = Material.CPM(raw_normal) @ temp
            u1 = u1/np.linalg.norm(u1)
            u2 = Material.CPM(raw_normal) @ u1

            d1 = Diffuse.Rodriguez(d, u1, np.deg2rad(self.sigma_deg*np.random.normal(scale=1))) # Rotate about u1
            d2 = Diffuse.Rodriguez(d1,u2, np.deg2rad(self.sigma_deg*np.random.normal(scale=1))) # Rotate about u2

            return Ray(hit.point, d2), True
        else: 
            return refracted_ray, True


