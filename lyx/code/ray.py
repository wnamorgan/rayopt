import numpy as np

class Ray:
    def __init__(self, origin, direction, n=1.0):
        self.origin = np.array(origin, dtype=float)
        self.direction = np.array(direction, dtype=float)
        self.direction /= np.linalg.norm(self.direction)
        self.n = n  # current refractive index

    def point(self, t):
        return self.origin + t * self.direction

    def offset(self, epsilon=1e-6):
        return Ray(self.point(epsilon), self.direction)
    