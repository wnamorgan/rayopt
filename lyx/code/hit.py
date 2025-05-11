import numpy as np

# === HIT CLASS ===
class Hit:
    def __init__(self, t, point, normal, element):
        self.t = t
        self.point = point
        self.normal = normal
        self.element = element