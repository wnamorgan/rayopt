import numpy as np

from rayopt import system_from_text, Analysis, GeometricTrace
#from rayopt.geometric_trace import GeometricTrace
import matplotlib.pyplot as plt

def main():
    s = get_system()
    print(s)
    fig, ax = plt.subplots()
    s.plot(ax)
    t = GeometricTrace(s)
    h=0.0
    t.rays_clipping((0, h))
    t.plot(ax)
    ray_positions = three_d_ray(s)
    ray_paths = ray_positions.squeeze()
    ax.plot(ray_paths[:, 2], ray_paths[:, 0], '-o', label='Ray path (x–z)')
    #ro.Analysis(s,plot_transverse=False,plot_spots=False,plot_opds=False,plot_longitudinal=False)
    plt.show()

def three_d_ray(system):
    # Create a ray origin and direction (in 3D)
    origin = np.array([0.2, 0.1, -1.0])      # 1qmm in front of lens, off-axis in x/y
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
        S       0      0     2 AIR
        S       1.25      1     1 SCHOTT-BK|N-BK7
        S       0    1.0     1 AIR
        S       0    2.0     2 AIR
        """
    columns = "type roc distance radius material"
    s = system_from_text(text, columns.split(),
        description="four element double gauss, intermediate optical design")
    s.object.angle = .36
    s.object.pupil.update_radius = True
    s.fields = 0, .7, 1.
    s.update()
    return s

if __name__=='__main__':
    main()