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





def make_system(lens,offset,sigma_dif_deg):
    
    eps = 1e-4
    # Create refractive materials
    air_to_glass    = Refractive(n_top=1.0, n_bottom=lens.n)
    glass_to_air    = Refractive(n_top=lens.n, n_bottom=1.0)
    air_to_diffuser = Diffuse(n_top=1.0, n_bottom=1.5, sigma_deg=sigma_dif_deg) # will only scatter upon exit from diffuser
    diffuser_to_air = Diffuse(n_top=1.5, n_bottom=1.0, sigma_deg=sigma_dif_deg) # will only scatter upon exit from diffuser
    air_to_filter   = Refractive(n_top=1.0, n_bottom=1.5)
    filter_to_air   = Refractive(n_top=1.5, n_bottom=1.0)
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
    diffuser_front = PlaneElement(center=[0, 0, apex-lens.tc - eps],       orientation = [0.0,0.0,0], material=air_to_diffuser, name="Diffuser Front Surface")
    diffuser_back  = PlaneElement(center=[0, 0, apex-lens.tc - eps - 1.6], orientation = [0.0,0.0,0], material=diffuser_to_air, name="Diffuser Back Surface")

    filter_front = PlaneElement(center=[0, 0, apex-lens.tc - 1.6 - 5.84],           orientation = [0.0,0.0,0], material=air_to_filter, name="Filter Front Surface")
    filter_back  = PlaneElement(center=[0, 0, apex-lens.tc - eps - 1.6 - 5.84 - 3], orientation = [0.0,0.0,0], material=filter_to_air, name="Filiter Back Surface")

    system = OpticalSystem()
    system.add_elements(lens_front)
    system.add_elements(lens_back)
    if True:
        system.add_elements(diffuser_front)
        system.add_elements(diffuser_back)
        system.add_elements(filter_front)
        system.add_elements(filter_back)    
    system.add_elements(plane_termination)
    system.apex = apex
    return system

def RayBundle(s,angle=10,N=100,dD=14.1):
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
        
        return points

def SpotSim(lens, offset=5, sigma_dif_deg=10, dD=14.1, N=100,theta=180):

        b=12

        s = make_system(lens,offset,sigma_dif_deg)

        points = RayBundle(s,angle=0,N=N,dD=dD)


        (az,el) = calc_ratios(points,dD/2)
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




def Plot_Single_Scurve(lens,hD,sigma_dif_deg,dD,Amax=20):

    (az,angles) = Single_Scurve(lens,hD,sigma_dif_deg,dD,Amax)

    FigName = f"Scurve_{lens.name}_{dD}_{hD}.jpg"
    fig, ax = plt.subplots()
    az = np.append(-az[:0:-1], az)
    angles = np.append(-angles[:0:-1], angles)

    if False:
        ax.plot(angles,az,color = 'blue', label='Raytrace')
        ax.plot(ami_ang, 2*(ami_4qd.mean(axis=1)-0.5), color='red', label='Experimental')
    else:
        ax.plot(angles,az/2+0.5,color = 'blue', label='Raytrace')
        ax.plot(ami_ang, ami_4qd.mean(axis=1), color='red', label='Experimental')

    ax.legend()
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('4QD Response')
    ax.set_xlim([-Amax,Amax])
    ax.grid(True)
    #plt.savefig(FigName,dpi=400) # 14.1 

def Single_Scurve(lens,hD,sigma_dif_deg,dD,Amax=15):
    s = make_system(lens,hD,sigma_dif_deg)

    N_ang=10
    N_rays=200
    start = time.time()
    az = np.zeros(N_ang)
    el = np.zeros(N_ang)
    angles = np.linspace(0,Amax,N_ang)
    
    for k, ang in enumerate(angles):
        points        = RayBundle(s,angle=ang,N=N_rays,dD=dD)
        (az[k],el[k]) = calc_ratios(points,dD/2,scatter_perc=10)
        print(f"(rho_az,rho_el) = ({az[k]},{el[k]})")
    end = time.time()
    print(f"Took {end - start:.2f} seconds")   
    return (az, angles)

def Single_trace(lens,offset,sigma_dif_deg):
    start_time = time.perf_counter()
    
    system = make_system(lens,offset,sigma_dif_deg)
    
    psi = np.deg2rad(0.0)
    theta = np.deg2rad(180)
    ray = Ray(origin=[0.0, 12.0, 30.0], direction=[np.sin(theta)*np.cos(psi), np.sin(theta)*np.sin(psi), np.cos(theta)])

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
    #ax[0].axis('equal')
    #ax[0].set_xlim(-1.5,1.5)
    #ax[0].set_ylim(-1.5,1.5)

    ax[1].plot(points[:, 1], points[:, 2], 'o-')
    ax[1].grid(True)
    ax[1].set_xlabel('y (mm)')
    ax[1].set_ylabel('z (mm)')

def Sweep_offset(lens, sigma_dif_deg, dD,Amax=20):

    hDvals = [-2, -4, -6, -8] #[5,6,7,8]
    FigName = f"ScurveSweep_{lens.name}_{dD}.jpg"
    fig, ax = plt.subplots()
    for k,hD in enumerate(hDvals):
        print(f"Evaluating offset: {hD} mm")
        (az,angles) = Single_Scurve(lens,hD,sigma_dif_deg,dD,Amax)
        az = np.append(-az[:0:-1], az)
        angles = np.append(-angles[:0:-1], angles)
        ax.plot(angles,az,label=f"{hD} mm")
  
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('4QD Response')
    ax.set_xlim([-Amax,Amax])
    ax.grid(True)
    ax.legend()
    #plt.savefig(FigName,dpi=400) # 14.1     

def Sweep_sigmaDiffuser(lens, hD, dD,Amax=20):

    sigma_dif_deg_vals = [6,8,10,12]
    FigName = f"ScurveSweep_{lens.name}_{dD}.jpg"
    fig, ax = plt.subplots()
    for k,sigma_dif_deg in enumerate(sigma_dif_deg_vals):
        (az,angles) = Single_Scurve(lens,hD,sigma_dif_deg,dD,Amax)
        az = np.append(-az[:0:-1], az)
        angles = np.append(-angles[:0:-1], angles)
        ax.plot(angles,az,label=f"{sigma_dif_deg} deg")
  
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('4QD Response')
    ax.set_xlim([-Amax,Amax])
    ax.grid(True)
    ax.legend()
    #plt.savefig(FigName,dpi=400) # 14.1    

def main():
# Select Lens
# (lens,offset,dD) = (ACL2520(),0.0,14.1)
    lens=ACL2520()
    dD=14.1
    Amax = 20
    offset=-7 # offset = -1.54
    sigma_dif_deg = 10 # Expect real value is 10, datasheet indicates 7.4
    #Single_trace(lens,offset,sigma_dif_deg)
    #Plot_Single_Scurve(lens,offset,sigma_dif_deg,dD,Amax=Amax)
    SpotSim(lens,offset, sigma_dif_deg , dD, 400)
    #Sweep_offset(lens,sigma_dif_deg, dD,Amax=Amax)
    #Sweep_sigmaDiffuser(lens,offset, dD,Amax=20)
    plt.show()
  


ami_ang = np.arange(-20, 20.1, 2.5)
ami_4qd = np.array([[0.065431730,   0.039233303,	0.054582604,	0.045399516],
                     [0.060776064,	0.038721717,	0.054508290,	0.044193700],
                     [0.061283050,   0.050105586,	0.064858491,	0.050548589],
                     [0.079545455,	0.065426997,	0.077645359,	0.064095792],
                     [0.111319788,	0.095910184,	0.112102340,	0.093477904],
                     [0.163639339,	0.144413751,	0.166100049,	0.141237600],
                     [0.252108716,	0.231223255,	0.249960797,	0.228860989],
                     [0.367078825,	0.346503244,	0.373525356,	0.349777117],
                     [0.508391822,	0.503046620,	0.504483964,	0.504403993],
                     [0.655879180,   0.640045636,	0.657918969,	0.637451966],
                     [0.765290283,	0.754172109,	0.771281572,	0.756679676],
                     [0.844734694,	0.834836189,	0.852631579,	0.835423440],
                     [0.885413125,	0.885570575,	0.894611593,	0.888601455],
                     [0.915664845,	0.913807673,	0.921772429,	0.919419682],
                     [0.930185223,	0.931980458,	0.937206932,	0.935047619],
                     [0.937236418,	0.940252268,	0.942454927,	0.944902967],
                     [0.937056165,	0.933565419,	0.937800577,	0.941279579],
                     ])


if __name__=='__main__':
    main()