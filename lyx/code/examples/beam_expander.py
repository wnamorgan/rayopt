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
(lens1, lens2, offset, dD) = (AL1815(), AL75150(), 0.0, 5.33) 



def make_system():
    


    # Create refractive materials
    air_to_lens1 = Refractive(n_top=1.0, n_bottom=lens1.n)
    lens1_to_air = Refractive(n_top=lens1.n, n_bottom=1.0)
    air_to_lens2 = Refractive(n_top=1.0, n_bottom=lens2.n)
    lens2_to_air = Refractive(n_top=lens2.n, n_bottom=1.0)


    apex=200.0
    lens1_front = AsphericElement(
        center=[0, 0, apex],  
        orientation=np.array([0.0,0.0,0.0]),
        lens=lens1,
        material=air_to_lens1,
        name="Lens 1 Front Surface"
    )
    lens1_back         = PlaneElement(center=lens1_front.center + np.array([0, 0, - lens1.tc]), orientation = [0.0,0.0,0], material=lens1_to_air, name="Lens 1 Back Surface")    

    lens2_back         = PlaneElement(center=lens1_back.center +  np.array([0, 0, - lens1.fb - lens2.fb]), orientation = [0.0,180.0,0], material=lens2_to_air, name="Lens 2 Back Surface")    
    
    lens2_front = AsphericElement(
        center=lens2_back.center + np.array([0, 0, - lens2.tc]),  
        orientation=np.array([0.0,180.0,0.0]),
        lens=lens2,
        material=air_to_lens2,
        name="Lens 2 Front Surface"
    )

    plane_termination = PlaneElement(center=[0, 0, offset],       orientation = [0.0,0.0,0], material=Absorbing(),  name="Base Plane")

    system = OpticalSystem()
    system.add_elements(lens1_front)
    system.add_elements(lens1_back)
    system.add_elements(lens2_back)
    system.add_elements(lens2_front)
    system.add_elements(plane_termination)
    return system

def single_ray():
    
    system = make_system()
    
    psi = np.deg2rad(0)
    theta = np.deg2rad(180)

    
    hR = 250.0

    ray = Ray(origin=[3.0, 0.0, hR], direction=[np.sin(theta)*np.cos(psi), np.sin(theta)*np.sin(psi), np.cos(theta)])

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
    ax[0].set_xlim(-75,75)
    ax[0].set_ylim(-75,75)

    ax[1].plot(points[:, 1], points[:, 2], 'o-')
    ax[1].grid(True)
    ax[1].set_xlabel('y (mm)')
    ax[1].set_ylabel('z (mm)')

def ray_bundle(s,direction,N):

    R_b = 6.0/2.0 # input beam size
    # Create a meshgrid 1"x1"
    x = np.linspace(-1, 1, N)*3.0
    y = np.linspace(-1, 1, N)*3.0

    hR = 250.0

    # Normalize direction
    direction = direction / np.linalg.norm(direction)

    pts = np.zeros(shape=(N**2,2))
    mask = np.zeros(shape=(N**2,1),dtype=bool)
    k=0
    points = []
    for i in range(N):
        for j in range(N):

            ray = Ray(origin=[x[i], y[j], hR], direction=direction)
            history = s.propagate(ray)
            ray_final = history[-1][1].origin
            r_l = np.sqrt(ray.origin[0]**2 + ray.origin[1]**2)
            if ( (r_l <= R_b) ): 
                points.append(ray_final.copy())
    points = np.array(points)
    return points

def RayBundleSim(N=100,theta=np.deg2rad(180)):
        
        b=40
        FigName = f"Tracing_{theta}_Expander.jpg"

        s = make_system()
        start = time.time()
        direction = np.array([0.0, 0.0, -1.0])     # Pointing along -z
        psi = np.deg2rad(0)
        points = ray_bundle(s,direction,N)
        end = time.time()
        print(f"Took {end - start:.2f} seconds")    

        #hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/2))
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=[int(N/2),int(N/2)], range=[[-40, 40],[-40, 40]])

        # Plot the heatmap
        fig, ax = plt.subplots()
        image = ax.imshow(hist.T, origin='lower', extent=[-40, 40, -40, 40], aspect='equal')
        fig.colorbar(image, label='Hit count per bin')  
        psi = np.linspace(0,2*np.pi,500)
        ax.plot((75/2)*np.cos(psi),(75/2)*np.sin(psi),color='white',linewidth=5)



        fig, ax = plt.subplots()
        xedges = np.linspace(-1,1,int(N/4))*b
        yedges = xedges
        #hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/4))
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=[xedges,yedges])
    
        xtnt = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #xtnt = [-b, b, -b, b]
        # Plot the heatmap
        
        hist_smoothed = gaussian_filter(hist, sigma=2)
        image = ax.imshow(hist_smoothed.T, origin='lower', extent=xtnt, aspect='equal',vmin=0, vmax=np.ceil(hist_smoothed.max()/20.0)*20)
        psi = np.linspace(0,2*np.pi,500)
        ax.plot((75/2)*np.cos(psi),(75/2)*np.sin(psi),color='white',linewidth=5)
        fig.colorbar(image, label='Hit count per bin')



def main():
    #single_ray()
    RayBundleSim(1000,theta=np.deg2rad(180))
    plt.show()

if __name__ == "__main__":
    main()
