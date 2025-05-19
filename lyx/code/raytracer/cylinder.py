import numpy as np
from raytracer.element import Element
from raytracer.hit import Hit
from scipy.optimize import bisect

class CylinderElement(Element):
    def __init__(self, center, axis, radius, height, material, name):
        super().__init__(material, name)
        self.center = np.array(center, dtype=float) # Bottom Center
        self.axis = np.array(axis, dtype=float)
        self.axis /= np.linalg.norm(self.axis)
        self.radius = radius
        self.height = height
        self.bounds = (1e-9,100)
        #self.material = material

    def surface_function(self,x, y, z):
        r2 = x**2 + y**2
        return self.radius**2-r2

    def intersect(self, ray):
        
        if True:
            t=self.intersect_analytical(ray)
        else:
            t=self.intersect_numerical(ray)

        if t is None:
            return None

        hit_point = ray.origin + t * ray.direction
        # Check if the hit point is within the height of the cylinder
        projection = self.center + np.dot(hit_point - self.center, self.axis) * self.axis
        height_check = np.dot(hit_point - self.center, self.axis)

        if height_check < 0 or height_check > self.height:
            return None  # Hit point is outside the cylinder bounds


        return Hit(t, ray.point(t), self.normal(hit_point), self)


    def intersect_numerical(self, ray):
        def f(t):
            point = ray.point(t)
            return self.surface_function(*point)

        try:
            t_hit = bisect(f, *self.bounds, xtol=1e-6)
            if t_hit < 0:
                return None
            else:
                return t_hit
        except ValueError:
            return None  # No root found in bounds


    def intersect_analytical(self, ray):
        # Compute ray-cylinder intersection (finite cylinder)
        ro = ray.origin - self.center
        rd = ray.direction

        # Projection of ray onto plane perpendicular to the cylinder axis
        a = rd - np.dot(rd, self.axis) * self.axis
        a_dot = np.dot(a, a)
        if a_dot == 0:
            return None  # Ray is parallel to cylinder axis

        b = ro - np.dot(ro, self.axis) * self.axis
        b_dot = np.dot(a, b)

        c = np.dot(b, b) - self.radius**2

        discriminant = b_dot**2 - a_dot * c
        if discriminant < 0:
            return None  # No real intersection

        sqrt_disc = np.sqrt(discriminant)
        t0 = (-b_dot - sqrt_disc) / a_dot
        t1 = (-b_dot + sqrt_disc) / a_dot

        t = t0 if t0 > 1e-6 else (t1 if t1 > 1e-6 else None)
        return t

    def normal(self, point):
        x, y, _ = point
        cx, cy, _ = self.center
        n = np.array([2 * (x - cx), 2 * (y - cy), 0.0])
        self._normal = n/np.linalg.norm(n)
        return self._normal