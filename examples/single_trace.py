import numpy as np

from rayopt import system_from_text, Analysis, GeometricTrace
#from rayopt.geometric_trace import GeometricTrace
import matplotlib.pyplot as plt

def main():
    s = get_system()


    fig, ax = plt.subplots()
    geo_trace(s,ax)
    single_ray(s,ax)

    plt.show()

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
    

def three_d_ray(system):
    # Create a ray origin and direction (in 3D)
    origin = np.array([0.2, 0.1, -1.0])*10      # 1qmm in front of lens, off-axis in x/y
    direction = np.array([0.0, 0.0, 1.0])     # Pointing along +z
    
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
 


    text = """
        S       0      0      10 AIR
        S       7.818  1       9 1.52
        S       0      8.2     9 AIR
        S       0      7.22     2.6 AIR
        """
    columns = "type roc distance radius material"
    s = system_from_text(text, columns.split(),
    description="four element double gauss, intermediate optical design")
    #s.object.angle = 20
    #s.object.pupil.update_radius = True
    #s.fields = 0, .7, 1.

    s[1].conic = -1.81700
    s[1].aspherics = [0,2.93e-04, 0.0, 0.0, 0.0]
    s.update()
    
    return s

if __name__=='__main__':
    main()