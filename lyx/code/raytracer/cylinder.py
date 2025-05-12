import numpy as np
from raytracer.element import Element
from raytracer.hit import Hit

class CylinderElement(Element):
    def __init__(self, center, axis, radius, height, material, name):
        super().__init__(material, name)
        self.center = np.array(center, dtype=float) # Bottom Center
        self.axis = np.array(axis, dtype=float)
        self.axis /= np.linalg.norm(self.axis)
        self.radius = radius
        self.height = height
        #self.material = material

    def intersect(self, ray):
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
        if t is None:
            return None

        hit_point = ray.origin + t * ray.direction
        # Check if the hit point is within the height of the cylinder
        projection = self.center + np.dot(hit_point - self.center, self.axis) * self.axis
        height_check = np.dot(hit_point - self.center, self.axis)

        if height_check < 0 or height_check > self.height:
            return None  # Hit point is outside the cylinder bounds


        return Hit(t, ray.point(t), self.normal(hit_point), self)


    def normal(self, point):
        x, y, _ = point
        cx, cy, _ = self.center
        n = np.array([2 * (x - cx), 2 * (y - cy), 0.0])
        self._normal = np.linalg.norm(n)
        return n / np.linalg.norm(self._normal)