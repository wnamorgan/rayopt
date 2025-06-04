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

def make_system():
    


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

def single_ray():
    
    system = make_system()
    
    psi = np.deg2rad(0)
    theta = np.deg2rad(170)

    
    hR = np.ceil(lens.fb/10)*10*2.0

    ray = Ray(origin=[-6, -8.0, system.apex+1], direction=[np.sin(theta)*np.cos(psi), np.sin(theta)*np.sin(psi), np.cos(theta)])

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



def RayBundleSim(N=100,theta=np.deg2rad(180)):
        
        (b,db) = (6,2)
        if (dD > 10):
            (b, db) = (12,3)
        FigName = f"Tracing_{theta}_{lens.name}_{dD}_{offset}.jpg"

        s = make_system()
        start = time.time()

        bundle_path = s.ray_bundle(center=(0,0,s.apex+1.0),psi=0,theta=theta,W=lens.D*1.4, N=N)
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
        (az,el) = calc_ratios(points,5.3/2)
        print(f"(rho_az,rho_el) = ({az},{el})")
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/2))
    
        # Plot the heatmap
        plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect='equal')
        plt.colorbar(label='Hit count per bin')    


        fig, ax = plt.subplots()
        xedges = np.linspace(-1,1,int(N/4))*b
        yedges = xedges
        #hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/4))
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=[xedges,yedges])
    
        xtnt = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        hist_smoothed = gaussian_filter(hist, sigma=1)
        if False:
            image = ax.imshow(hist_smoothed.T, origin='lower', extent=xtnt, aspect='equal',vmin=0, vmax=np.ceil(hist_smoothed.max()/20.0)*20)
        else:
            image = ax.imshow(hist.T, origin='lower', extent=xtnt, aspect='equal',vmin=0, vmax=np.ceil(hist.max()/20.0)*20)
        psi = np.linspace(0,2*np.pi,500)
        ax.plot((dD/2)*np.cos(psi),(dD/2)*np.sin(psi),color='white',linewidth=5)
        fig.colorbar(image, label='Hit count per bin')



def main():
    #single_ray()
    RayBundleSim(200,theta=170)
    plt.show()

if __name__ == "__main__":
    main()
