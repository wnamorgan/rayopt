

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Circle
# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raytracer.ray import Ray
from raytracer.plane import PlaneElement
from raytracer.cylinder import CylinderElement
from raytracer.system import OpticalSystem
from raytracer.surface import Reflective

(origin, radius) = ((0,0),1.0)

def make_system():
    system = OpticalSystem()
    # Reflective plane at z = 0
    system.add_elements(PlaneElement(center=[0, 0, 0], orientation=[0, 0, 0], material=Reflective(), name = 'base'))

    # Reflective cylinder centered on z-axis, radius = 1, infinite height
    system.add_elements(CylinderElement(center=[origin[0], origin[1], 0], orientation=[0, 0, 0], radius=radius, 
                                        height = 5.0, material=Reflective(), name = 'cylinder'))

    return system

def main():
    start_time = time.perf_counter()
    
    system = make_system()
    
    psi = np.deg2rad(111)
    psi = np.deg2rad(100)
    theta = np.deg2rad(150)
    # Launch a ray from above at an angle toward the cylinder
    ray = Ray(origin=[0.5, 0, 2], direction=[-0.2, 0.5, -1.0])
    ray = Ray(origin=[0.5, .1, 2], direction=[np.sin(theta)*np.cos(psi), np.sin(theta)*np.sin(psi), np.cos(theta)])

    history = system.propagate(ray)

    # Print each step
    points = []
    for i, ray_int in enumerate(history):        
        (name,ray) = ray_int    
        points.append(ray.origin)
        print(f"Step {i}: Surface={name}, Origin={ray.origin}, Direction={ray.direction}")    
    points = np.array(points)
    # 2D plot (x–z plane)

    end_time = time.perf_counter()
    print(f"Elapsed time: {(end_time-start_time)*1000:.1f} ms")

    fig, ax = plt.subplots(1,2,figsize=(8,4),sharex=True)
    
    ax[0].plot(points[:, 1], points[:, 0], 'o-')
    ax[0].grid(True)
    ax[0].set_xlabel('y (mm)')
    ax[0].set_ylabel('x (mm)')
    ax[0].axis('equal')
    circle = Circle(origin, radius, edgecolor='black', facecolor='none', linewidth=2)
    ax[0].add_patch(circle)
    ax[0].set_xlim(-1.5,1.5)
    ax[0].set_ylim(-1.5,1.5)

    ax[1].plot(points[:, 1], points[:, 2], 'o-')
    ax[1].grid(True)
    ax[1].set_xlabel('y (mm)')
    ax[1].set_ylabel('z (mm)')

    plt.show()

if __name__ == "__main__":
    main()

