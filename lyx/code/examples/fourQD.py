import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter

# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raytracer.asphere import AsphericElement
from raytracer.plane import PlaneElement
from raytracer.ray import Ray  
from raytracer.surface import * 
from raytracer.lens import *
from raytracer.system import OpticalSystem
from raytracer.detector import calc_ratios

# Select Lens
(lens,offset,dD) = (ACL2520(),0.0,5.33)
(lens,offset,dD) = (ACL1815(),0.0,5.33)
(lens,offset,dD) = (AL1815(),0.0,5.33)
(lens,offset,dD) = (AL75150(),0.0,5.33) 
(lens,offset,dD) = (AL1512(),0.0,5.33)
(lens,offset,dD) = (EO22714(),0.0,5.33)
#(lens,offset,dD) = (EO49109(),3.0,5.33)


(lens,offset,dD) = (ACL1815(),2.8,5.33)
(lens,offset,dD) = (EO15731(),0.0,5.33)


def make_system(lens,offset):
    
    # Create refractive materials
    air_to_glass = Refractive(n_top=1.0, n_bottom=lens.n)
    glass_to_air = Refractive(n_top=lens.n, n_bottom=1.0)
    
    # Surfaces: plane at z=0 (termination), lens back (z=10), asphere front (z=22)
    apex=lens.tc + lens.fb
    plane_termination = PlaneElement(center=[0, 0, offset],       orientation = [0.0,0.0,0], material=Absorbing(),  name="Base Plane")
    lens_back         = PlaneElement(center=[0, 0, apex-lens.tc], orientation = [0.0,0.0,0], material=glass_to_air, name="Lens Back Surface")
    lens_front = AsphericElement(
        center=[0, 0, apex],  # Apex at z=22 (lens is 12mm thick)
        orientation=np.array([0.0,0.0,0.0]),
        lens=lens,
        material=air_to_glass,
        name="Aspheric Front Surface"
    )
    
    system = OpticalSystem()
    system.add_elements(lens_front)
    system.add_elements(lens_back)
    system.add_elements(plane_termination)
    system.apex = apex
    return system

def RayBundle(s,angle=10,N=100,dD=5.3):
        theta = 180-angle
        (b,db) = (6,2)
        if (dD > 10):
            (b, db) = (12,3)
        start = time.time()
        D = s.elements[0].aperture_radius*2.0
        bundle_path = s.ray_bundle(center=(0,0,s.apex+1.0),psi=0,theta=theta,W=D*1.4, N=N)
        points = []
        for k,ray_path in enumerate(bundle_path):
            if (s.elements[0].name==ray_path[1][0]): # assumes first element in system is only entry point
                ray_final = ray_path[-1][1]
                points.append(ray_final.origin)
                if ray_final.origin[0]<-0.1:
                    pass
        points = np.array(points)
        
        end = time.time()
        print(f"Took {end - start:.2f} seconds")    
        (az,el) = calc_ratios(points,dD/2)
        return (az,el)