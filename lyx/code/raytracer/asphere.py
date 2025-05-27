import numpy as np
from raytracer.element import Element
from raytracer.hit import Hit
from scipy.optimize import bisect

class AsphericElement(Element):
    def __init__(self, center, lens, material, name):
        super().__init__(material, name)
        self.center = np.array(center, dtype=float)
        self.curvature = 1/lens.roc    # 1 / radius of curvature
        self.k = lens.conic            # Conic constant
        self.coeffs = lens.aspheric    # List of A4, A6, A8, ...
        self.aperture_radius = lens.D/2 
        self.bounds = (1e-5, 100)

    def cylinder_function(self,x, y, z):
        r2 = x**2 + y**2
        return self.aperture_radius**2-r2

    def surface_function(self, x, y, z):
        # Function assumes input coordinates are relative to asphere apex
        r2 = x**2 + y**2
        z_surf = self.sag(r2)
        return z - z_surf

    def sag(self, r2):
        # Standard sag equation for an asphere
        c = self.curvature
        k = self.k
        sqrt_term = np.sqrt(1 - (1 + k) * c**2 * r2)
        base = (c * r2) / (1 + sqrt_term)
        #poly = sum(a * r2**((i+2)//2) for i, a in enumerate(self.coeffs))
        poly = self.coeffs[0]*r2**2
        return -(base + poly)

    def intersect(self, ray):
        def f(t):
            point = ray.point(t) - self.center
            return self.surface_function(*point)
        def f_cylinder(t):
            point = ray.point(t) - self.center
            return self.cylinder_function(*point)
        
        try:
            rhb = self.bounds[1]
            if (f_cylinder(self.bounds[0])*f_cylinder(self.bounds[1])<0):
                rhb = bisect(f_cylinder, *self.bounds, xtol=1e-6)
            t_hit = bisect(f, self.bounds[0], rhb, xtol=1e-6)
            if t_hit < 0:
                return None
        except ValueError:
            return None  # No intersection

        hit_point = ray.point(t_hit)
        rel_hit = hit_point - self.center
        if np.linalg.norm(rel_hit[:2]) > self.aperture_radius:
            return None  # Outside aperture

        return Hit(t_hit, ray.point(t_hit), self.normal(hit_point), self)

    def normal(self, point):
        # Placeholder: Numerically compute gradient of the surface function
        x, y, z = point
        eps = 1e-6
        dx = (self.surface_function(x + eps, y, z) - self.surface_function(x - eps, y, z)) / (2 * eps)
        dy = (self.surface_function(x, y + eps, z) - self.surface_function(x, y - eps, z)) / (2 * eps)
        dz = 1  # dz/dz of surface function is always -1 in z-directional surface function form
        n = np.array([dx, dy, dz]) 
        self._normal = n/np.linalg.norm(n)
        return self._normal
