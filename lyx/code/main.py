# Core vector math can be done using NumPy
import numpy as np
from raytracer.ray import Ray
from raytracer.hit import Hit
from raytracer.plane import PlaneElement
from raytracer.system import OpticalSystem
from raytracer.surface import Reflective

def make_system():
    plane = PlaneElement(point=[0, 0, 0], normal=[0, 0, 1], material=Reflective(),name='Base')
    system = OpticalSystem(elements=[plane])
    return system

def main():
    system = make_system()
    ray = Ray(origin=[0, 0, 1], direction=[0, 0, -1])
    path = system.propagate(ray)
    for i, (o, d) in enumerate(path):
        print(f"Step {i}: Origin={o}, Direction={d}")    

if __name__ == "__main__":
    main()
