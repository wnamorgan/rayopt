from raytracer.hit import Hit
from raytracer.plane import PlaneElement
from raytracer.ray import Ray  
from raytracer.grid import *
class OpticalSystem:
    def __init__(self, elements=[], max_bounces=10, epsilon=1e-6):
        self.elements = elements
        self.max_bounces = max_bounces
        self.epsilon = epsilon

    def add_elements(self, elements):
        self.elements.append(elements)

    def propagate(self, initial_ray):


        history = [('source', initial_ray)]

        continue_propagation = True
        bounce_count = 0
        ray = initial_ray
        while continue_propagation:
            hit = self.find_next_intersection(ray)
            
            if not hit:
                break  # ray left the system
            
            new_ray, continue_flag = hit.element.redirect(ray, hit)
            history.append((hit.element.name,new_ray))
            ray = new_ray
            continue_propagation = continue_flag
    
            bounce_count += 1
            if bounce_count > self.max_bounces:
                continue_propagation = False


        return history

    def find_next_intersection(self, ray):
        closest_hit = None
        for element in self.elements:
            hit = element.intersect(ray)
            if hit and (closest_hit is None or hit.t < closest_hit.t):
                closest_hit = hit
        return closest_hit


    def ray_bundle(self,center=(0,0,10),psi=0.0,theta=180.0,W=20, N=400):
        # center = origin or ray bundle
        # direction is direction of ray bundle
        # W = with of input bundle

        (x,y) = generate_uniform_grid(N, xlim=(-W/2.0, W/2.0), ylim=(-W/2.0, W/2.0))
        #(x,y) = generate_hex_grid(N, xlim=(-W/2.0, W/2.0), ylim=(-W/2.0, W/2.0))
        #(x,y) = generate_jittered_grid(N, xlim=(-W/2.0, W/2.0), ylim=(-W/2.0, W/2.0))
        #(x,y) = generate_random_grid(N, xlim=(-W/2.0, W/2.0), ylim=(-W/2.0, W/2.0))
    
        # Normalize direction
        psi    = np.deg2rad(psi)
        theta  = np.deg2rad(theta)
        direction=[np.sin(theta)*np.cos(psi), np.sin(theta)*np.sin(psi), np.cos(theta)] 
        bundle_path = []

        for i in range(len(x)):
            if True:#(np.sqrt(x[i]**2 + y[i]**2) <= W/2): 
                ray = Ray(origin=[x[i]+center[0], y[i]+center[1], center[2]], direction=direction)
                history = self.propagate(ray)
                bundle_path.append(history)
        return bundle_path
