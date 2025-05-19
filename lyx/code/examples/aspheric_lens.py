import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Circle

# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raytracer.asphere import AsphericElement
from raytracer.plane import PlaneElement
from raytracer.ray import Ray  
from raytracer.surface import * 
from raytracer.lens import *
from raytracer.system import OpticalSystem
from raytracer.detector import calc_ratios

def make_system():
    # Select Lens
    lens = ACL2520()
    lens = ACL1815()
    
    # Create refractive materials
    air_to_glass = Refractive(n_top=1.0, n_bottom=lens.n)
    glass_to_air = Refractive(n_top=lens.n, n_bottom=1.0)
    
    # Surfaces: plane at z=0 (termination), lens back (z=10), asphere front (z=22)
    apex=lens.tc + lens.fb
    plane_termination = PlaneElement(point=[0, 0, 2.8], normal=[0, 0, 1], material=Absorbing(), name="Base Plane")
    lens_back = PlaneElement(point=[0, 0, apex-lens.tc], normal=[0, 0, 1], material=glass_to_air, name="Lens Back Surface")
    lens_front = AsphericElement(
        center=[0, 0, apex],  # Apex at z=22 (lens is 12mm thick)
        lens=lens,
        material=air_to_glass,
        name="Aspheric Front Surface"
    )
    
    system = OpticalSystem()
    system.add_elements(lens_front)
    system.add_elements(lens_back)
    system.add_elements(plane_termination)
    return system

def single_ray():
    
    system = make_system()
    
    psi = np.deg2rad(0)
    theta = np.deg2rad(180)

    ray = Ray(origin=[0.0, -8, 30], direction=[np.sin(theta)*np.cos(psi), np.sin(theta)*np.sin(psi), np.cos(theta)])

    start_time = time.perf_counter()
    history = system.propagate(ray)
    end_time = time.perf_counter()
    print(f"Elapsed time: {(end_time-start_time)*1000:.1f} ms")
    # Print each step
    points = []
    for i, ray_int in enumerate(history):        
        (name,ray) = ray_int    
        points.append(ray.origin)
        print(f"Step {i}: Surface={name}, Origin={ray.origin}, Direction={ray.direction}")    
    points = np.array(points)
    # 2D plot (x–z plane)



    fig, ax = plt.subplots(1,2,figsize=(8,4),sharex=True)
    
    ax[0].plot(points[:, 1], points[:, 0], 'o-')
    ax[0].grid(True)
    ax[0].set_xlabel('y (mm)')
    ax[0].set_ylabel('x (mm)')
    #ax[0].axis('equal')
    circle = Circle((0,0), 25.0, edgecolor='black', facecolor='none', linewidth=2)
    ax[0].add_patch(circle)
    ax[0].set_xlim(-15,15)
    ax[0].set_ylim(-15,15)

    ax[1].plot(points[:, 1], points[:, 2], 'o-')
    ax[1].grid(True)
    ax[1].set_xlabel('y (mm)')
    ax[1].set_ylabel('z (mm)')

def ray_bundle(s,direction,N):

    R_l = 18/2.0
    R_d = 5.3/2.0
    # Create a meshgrid 1"x1"
    x = np.linspace(-1, 1, N)*25.4/2.0
    y = np.linspace(-1, 1, N)*25.4/2.0

    # Normalize direction
    direction = direction / np.linalg.norm(direction)

    pts = np.zeros(shape=(N**2,2))
    mask = np.zeros(shape=(N**2,1),dtype=bool)
    k=0
    points = []
    for i in range(N):
        for j in range(N):

            ray = Ray(origin=[x[i], y[j], 30], direction=direction)
            history = s.propagate(ray)
            ray_final = history[-1][1].origin
            r_l = np.sqrt(ray_final[0]**2 + ray_final[1]**2)
            if ( (r_l <= R_l) ): 
                points.append(ray_final.copy())
    points = np.array(points)
    return points

def RayBundleSim(N=100):
        s = make_system()
        start = time.time()
        direction = np.array([0.0, 0.0, -1.0])     # Pointing along -z
        psi = np.deg2rad(0)
        theta = np.deg2rad(180)
        points = ray_bundle(s,direction,N)
        end = time.time()
        print(f"Took {end - start:.2f} seconds")    
        (az,el) = calc_ratios(points,5.3/2)
        print(f"(rho_az,rho_el) = ({az},{el})")
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/2))
    
        # Plot the heatmap
        plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect='equal')
        plt.colorbar(label='Hit count per bin')    


def main():
    #single_ray()
    RayBundleSim(100)
    plt.show()

if __name__ == "__main__":
    main()
