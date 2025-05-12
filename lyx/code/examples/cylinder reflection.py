

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raytracer.ray import Ray
from raytracer.plane import PlaneElement
from raytracer.cylinder import CylinderElement
from raytracer.system import OpticalSystem
from raytracer.surface import Reflective

def make_system():
    system = OpticalSystem()
    # Reflective plane at z = 0
    system.add_elements(PlaneElement(point=[0, 0, 0], normal=[0, 0, 1], material=Reflective(), name = 'base'))

    # Reflective cylinder centered on z-axis, radius = 1, infinite height
    system.add_elements(CylinderElement(center=[0, 0, 0], axis=[0, 0, 1], radius=1.0, height = 5.0, material=Reflective(), name = 'cylinder'))

    return system

def main():
    system = make_system()

    # Launch a ray from above at an angle toward the cylinder
    ray = Ray(origin=[0.5, 0, 2], direction=[-0.2, 0.5, -1.0])

    history = system.propagate(ray)

    # Print each step
    points = []
    for i, ray_int in enumerate(history):        
        (name,ray) = ray_int    
        points.append(ray.origin)
        print(f"Step {i}: Surface={name}, Origin={ray.origin}, Direction={ray.direction}")    
    points = np.array(points)
    # 2D plot (x–z plane)

    plt.figure()
    plt.plot(points[:, 1], points[:, 2], 'o-')
    circle = plt.Circle((0, 0), 1.0, color='gray', fill=False, linestyle='--', label='Cylinder Wall')
    plt.gca().add_patch(circle)
    plt.axhline(0, color='k', linestyle='--', label='Reflective Plane')
    plt.gca().set_aspect('equal')
    plt.xlabel('x')
    plt.ylabel('z')
    plt.legend()
    plt.title('Ray Reflection in Cylinder Over Plane')
    plt.show()

if __name__ == "__main__":
    main()
