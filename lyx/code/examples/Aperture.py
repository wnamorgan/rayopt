# This module simulates an aperture, and is used to see what a colimated light source produces when evaluated below the aperture stop
# Variation in surface count histocgram is entirely due to input ray distribution, histogram parameters and filtering effects.  
# This should be considered when examining more complicated optical systems.  Different input distributions can be experimented with
# using the options available in grid.py


import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter

# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from raytracer.plane import PlaneElement
from raytracer.ray import Ray  
from raytracer.surface import * 
from raytracer.system import OpticalSystem
from raytracer.grid import *
D = 20.0

def make_system():
    plane_termination = PlaneElement(center=[0, 0, 0],       orientation = [0.0,0.0,0], material=Absorbing(),  name="Base Plane")
    system = OpticalSystem()
    system.add_elements(plane_termination)
    return system


def ray_bundle(s,direction,N):

    #(x,y) = generate_uniform_grid(N, xlim=(-D/2.0, D/2.0), ylim=(-D/2.0, D/2.0))
    #(x,y) = generate_hex_grid(N, xlim=(-D/2.0, D/2.0), ylim=(-D/2.0, D/2.0))
    (x,y) = generate_jittered_grid(N, xlim=(-D/2.0, D/2.0), ylim=(-D/2.0, D/2.0))
    #(x,y) = generate_random_grid(N, xlim=(-D/2.0, D/2.0), ylim=(-D/2.0, D/2.0))


    # Normalize direction
    direction = direction / np.linalg.norm(direction)

    pts = np.zeros(shape=(N**2,2))
    mask = np.zeros(shape=(N**2,1),dtype=bool)
    k=0
    points = []
    all_points = []
    
    for i in range(len(x)):
        ray = Ray(origin=[x[i], y[i], 10], direction=direction)
        history = s.propagate(ray)
        ray_final = history[-1][1].origin
        r_l = np.sqrt(ray_final[0]**2 + ray_final[1]**2)
        all_points.append(ray_final.copy())
        if ( (r_l <= D/2) ): 
            points.append(ray_final.copy())
    points = np.array(points)
    return points

def RayBundleSim(N=100,theta=np.deg2rad(180)):
        
        b=15
        M=11
        s = make_system()
        start = time.time()
        direction = np.array([0.0, 0.0, -1.0])     # Pointing along -z
        points = ray_bundle(s,direction,N)
        end = time.time()
        print(f"Took {end - start:.2f} seconds")    

        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/8))
    
        # Plot the heatmap
        plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect='equal')
        plt.colorbar(label='Hit count per bin')    


        fig, ax = plt.subplots()
        xedges = np.linspace(-1,1,int(N/8))*b
        yedges = xedges
        #hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/4))
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=[xedges,yedges])
    
        xtnt = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #xtnt = [-b, b, -b, b]
        # Plot the heatmap
        
        hist_smoothed = gaussian_filter(hist, sigma=2)
        image = ax.imshow(hist_smoothed.T, origin='lower', extent=xtnt, aspect='equal',vmin=0, vmax=np.ceil(hist_smoothed.max()/20.0)*20)
        psi = np.linspace(0,2*np.pi,500)
        ax.plot((D/2)*np.cos(psi),(D/2)*np.sin(psi),color='white',linewidth=5)
        fig.colorbar(image, label='Hit count per bin')



def main():
    RayBundleSim(1000,theta=np.deg2rad(180))
    plt.show()

if __name__ == "__main__":
    main()
