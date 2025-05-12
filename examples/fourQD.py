import numpy as np

from rayopt import system_from_text, Analysis, GeometricTrace
#from rayopt.geometric_trace import GeometricTrace
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import time

def main():
    s = get_system()

    fig, ax = plt.subplots()
    if True:
        geo_trace(s,ax)
        single_ray(s,ax)
    else:
        N=400
        start = time.time()
        direction = np.array([0.2, 0.0, 1.0])     # Pointing along +z
        if True:
            points = ray_bundle(s,direction,N)
        else: # This is actually slower....
            points = parallel_ray_bundle(s,direction,N)
        end = time.time()
        print(f"Took {end - start:.2f} seconds")    
        (az,el) = calc_ratios(points,5.3/2)
        R = 1.0/s[1].curvature
        n = s.refractive_index(1064e-9,1)
        f = R/(n-1)
        D = 18
        hd = 10 - s[-1]._distance # assumes no field stop, i.e., s[-1] is relative to back of lens
        rs = D*hd/(2*f)
        eps_max = rs/(f-hd)
        print(f"rs = {rs} mm")
        print(f"(rho_az,rho_el) = ({az},{el})")
        print(np.arctan(eps_max)*57.1)
        hist, xedges, yedges = np.histogram2d(points[:,0], points[:,1], bins=int(N/2))
    
        # Plot the heatmap
        plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect='equal')
        plt.colorbar(label='Hit count per bin')

    plt.show()


def calc_ratios(points,rD):
    (A,B,C,D,T) = (0,0,0,0,0)
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
    R_l = 18/2.0
    R_d = 5.3/2.0
    # Create a meshgrid 1"x1"
    x = np.linspace(-1, 1, N)*25.4/2.0
    y = np.linspace(-1, 1, N)*25.4/2.0

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
    R_d = 5.3/2.0    
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
    origin = np.array([7.0, 0.0, -1.0])      # 1qmm in front of lens, off-axis in x/y
    
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

def get_system():
 

    # Last element is detector and is 2.65mm.  Left at 5.6 (arbirary) to evaluate hits post processing
    text = """
        S       0      0      15 AIR
        S       7.818  1       9 1.52
        S       0      8.2     9 AIR
        S       0      7.22    12.0 AIR
        """
    columns = "type roc distance radius material"
    s = system_from_text(text, columns.split(),
    description="four element double gauss, intermediate optical design")
    #s.object.angle = 20
    #s.object.pupil.update_radius = True
    #s.fields = 0, .7, 1.

    s[1].conic = -1.81700
    s[1].aspherics = [0,2.93e-04, 0.0, 0.0, 0.0]
    s.object.angle = 20
    s.object.pupil.update_radius = True
    s.fields = 0, .7, 1.
    s.wavelengths=[1064e-9]
    s.update()
    
    return s

if __name__=='__main__':
    main()