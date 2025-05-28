

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raytracer.ray import Ray
from raytracer.plane import PlaneElement
from raytracer.system import OpticalSystem
from raytracer.surface import Reflective

def make_system():
    plane = PlaneElement(center=[0, 0, 0], orientation=[0, 0, 0], material=Reflective(),name='base')
    system = OpticalSystem(elements=[plane])
    return system

def main():
    system = make_system()
    ray = Ray(origin=[0, 0, 1], direction=[0, 1, -1])
    ray_ints = system.propagate(ray)
    pts = []
    for i, ray_int in enumerate(ray_ints):        
        (name,ray) = ray_int    
        pts.append(ray.origin)
        print(f"Step {i}: Surface={name}, Origin={ray.origin}, Direction={ray.direction}")    
    pts = np.array(pts)
    fig,ax = plt.subplots()
    ax.plot(pts[:,1],pts[:,2])
    ax.set_xlabel('y (mm)')
    ax.set_ylabel('z (mm)')
    ax.grid(True)
    plt.show()
if __name__ == "__main__":
    main()