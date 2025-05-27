import numpy as np

from rayopt import system_from_text, Analysis, GeometricTrace
#from rayopt.geometric_trace import GeometricTrace
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import time
from lens import *
from scipy.ndimage import gaussian_filter
def main():
    theta =0

    (lens, hD, dD) = (ACL1815U(), 2.8, 5.33) # Baseline Lens, Baseline Detector (hd = 2.8 nominal)
    (lens, hD, dD) = (EO_15889(), 2, 5.33) # Baseline Lens, Baseline Detector (hd = 2.8 nominal)
    #(lens, hD, dD) = (ACL1815U(), 5.3, 14.1) # Baseline lens, Big Detector (set hD=-0.2 to be at focal point and hD=5.3 nominal)
    #(lens, hD, dD) = (ACL2520U(), 6.0, 14.1) # Big Thor lens, Big Detector (set hD=-0.2 to be at focal point and hD=5.0 nominal)
    #(lens, hD, dD) = (EO_16982(), 2.0, 14.1) # Big EO lens, Big Detector
    (b,db) = (6,2)
    if (dD > 10):
        (b, db) = (12,3)
    FigName = f"Tracing_{theta}_{lens.name}_{dD}_{hD}.jpg"
    s = get_system(lens,hD)

    fig, ax = plt.subplots()
    if False:
        geo_trace(s,ax)
        single_ray(s,ax)
    else:
        
        N=500
        start = time.time()
        
        
        direction = np.array([np.sin(np.deg2rad(theta)), 0.0, np.cos(np.deg2rad(theta))])     # Pointing along +z
        #direction = np.array([0.2, 0.0, 1]) 
        if True:
            points = ray_bundle(s,direction,N)
        else: # This is actually slower....
            points = parallel_ray_bundle(s,direction,N)
        end = time.time()
        print(f"Took {end - start:.2f} seconds")    
        (az,el) = calc_ratios(points,dD/2)
        print(f"(rho_az,rho_el) = ({az},{el})")


        
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
        ax.plot((dD/2)*np.cos(psi),(dD/2)*np.sin(psi),color='white',linewidth=5)
        fig.colorbar(image, label='Hit count per bin')
        ax.set_xlabel('x (mm)')
        ax.set_ylabel('y (mm)')
        ax.set_xticks(np.arange(-b, b+1, db))  # Ticks at 0, 2, 4, 6, 8
        ax.set_xticks(np.arange(-b, b+1, db))  # Ticks at 0, 2, 4, 6, 8
        plt.savefig(FigName,dpi=400) # 14.1 

    plt.show()
    


def calc_ratios(points,rD,b=0):
    (A,B,C,D) = (b,b,b,b)
    T = A+B+C+D
    for point in points:
        x = point[0]
        y = point[1]
        r = np.sqrt(x**2+y**2)
        if r<rD:
            T=T+1
            if x < 0:
                if y < 0:
                    B = B+1
                else:
                    A = A+1
            else:
                if y < 0:
                    C = C+1
                else:
                    D = D+1
        az = 0
        el = 0
        if T>0:
            az = ((C+D)-(A+B))/(A+B+C+D)
            el = ((A+D)-(B+D))/(A+B+C+D)
    return (az,el)



def geo_trace(s,ax):
    print(s)
    s.plot(ax)
    t = GeometricTrace(s)
    h=0.0
    t.rays_clipping((0, h))
    t.plot(ax)

def single_ray(s,ax):
    ray_positions = three_d_ray(s)
    ray_paths = ray_positions.squeeze()
    distance = np.array([s[0]._distance, s[0]._distance + s[1]._distance, s[0]._distance + s[1]._distance+s[2]._distance, s[0]._distance+ s[1]._distance+s[2]._distance+s[3]._distance] )
    ax.plot(ray_paths[:, 2]+distance, ray_paths[:, 0], '-o', label='Ray path (x–z)')
    

def ray_bundle(s,direction,N):
    R_l = s[1].radius
    # Create a meshgrid 1"x1"
    x = np.linspace(-1, 1, N)*R_l*1.4 
    y = np.linspace(-1, 1, N)*R_l*1.4

    #x = np.linspace(-1, 1, N)*25.4/2.0
    #y = np.linspace(-1, 1, N)*25.4/2.0

    # Initialize the geometric tracer
    tracer = GeometricTrace(s)

    # Normalize direction
    direction = direction / np.linalg.norm(direction)

    pts = np.zeros(shape=(N**2,2))
    mask = np.zeros(shape=(N**2,1),dtype=bool)
    k=0
    points = []
    for i in range(N):
        for j in range(N):
            r = np.sqrt(x[i]**2 + y[j]**2)
            if True:# (r < R_l): - No, you can't limit this or you will miss rays that come in from the side of the lens at angle
                ray_positions = evaluate_point(((x[i],y[j]),direction,tracer))
    
                if (np.any(np.isnan(ray_positions))==False):
                    r_l = np.sqrt(ray_positions[1,0]**2 + ray_positions[1,1]**2)
                    r_d = np.sqrt(ray_positions[-1,0]**2 + ray_positions[-1,1]**2)
                    if ( (r_l <= R_l) ): # Later, I will check (r_d <= R_d) 
                        points.append(ray_positions[-1,0:2].copy())
    points = np.array(points)
    return points


def parallel_ray_bundle(s,direction,N):
    R_l = 18/2.0 
    # Generate a grid of points
    x = np.linspace(-1, 1, N)*25.4/2.0
    y = np.linspace(-1, 1, N)*25.4/2.0
    xg, yg = np.meshgrid(x, y)
    points = list(zip(xg.ravel(), yg.ravel()))
    tracer = GeometricTrace(s)

    # Package points and parameters for each job
    tasks = [((x, y), direction, tracer) for x, y in points]
    
    # Run in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(evaluate_point, tasks))



    # Convert result back into a 2D array (bool mask)
    #hit_mask = np.array(results).reshape(xg.shape)
    points = []
    for ray_positions in results:
        if (np.any(np.isnan(ray_positions))==False):
            r_l = np.sqrt(ray_positions[1,0]**2 + ray_positions[1,1]**2)
            r_d = np.sqrt(ray_positions[-1,0]**2 + ray_positions[-1,1]**2)
            if ( (r_l <= R_l) ): # Later, I will check (r_d <= R_d) 
                points.append(ray_positions[-1,0:2].copy())
    points = np.array(points)
    return points

def evaluate_point(args):
    (x, y), direction, tracer = args
    origin = np.array([x, y, -1.0])
    
    # Provide the ray to the tracer
    tracer.rays_given(origin, direction)
    # Propagate the ray through the system
    tracer.propagate()
    ray_positions = tracer.y.squeeze()
    return ray_positions 

def three_d_ray(system):
    # Create a ray origin0 0and direction (in 3D)
    origin = np.array([-10.5, 0.0, -1.0])      # 1qmm in front of lens, off-axis in x/y
    direction = np.array([0.2, 0.0, 1.0])     # Pointing along +z
    direction = np.array([0.0, 0.0, 1.0])     # Pointing along +z
    origin = np.array([9.0, 0.0, 0.0])      # 1qmm in front of lens, off-axis in x/y
    
    # Initialize the geometric tracer
    tracer = GeometricTrace(system)

    # Normalize direction
    direction = direction / np.linalg.norm(direction)
    
    # Provide the ray to the tracer
    tracer.rays_given(origin, direction)
    
    # Propagate the ray through the system
    tracer.propagate()
    
    # Access the ray positions at each surface
    ray_positions = tracer.y  # Shape: (number_of_surfaces, number_of_rays, 3)
    
    # Print the ray positions
    for i, pos in enumerate(ray_positions):
        print(f"Surface {i}: {pos[0]}")
    return ray_positions

def get_system(lens=ACL1815U(), hd = 2.8):
    
    text = f"""
        S       0      0      15 AIR
        S       {lens.roc}  1       {lens.D/2} 1.52
        S       {lens.s2_roc}      {lens.tc}     {lens.D/2} AIR
        S       0      {lens.BFL-hd}    12.0 AIR
        """
    
    columns = "type roc distance radius material"
    s = system_from_text(text, columns.split(),
    description="four element double gauss, intermediate optical design")

    s[1].conic = lens.conic
    s[1].aspherics = lens.aspherics


    s.object.angle = 20
    s.object.pupil.update_radius = True
    s.fields = 0, .7, 1.
    s.wavelengths=[1064e-9]
    s.update()
    print(s)
    return s

if __name__=='__main__':
    main()