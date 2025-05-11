

# === SYSTEM CLASS ===
class OpticalSystem:
    def __init__(self, elements, max_bounces=10, epsilon=1e-6):
        self.elements = elements
        self.max_bounces = max_bounces
        self.epsilon = epsilon

    def propagate(self, initial_ray):
        history = [initial_ray]
        continue_propagation = True
        bounce_count = 0
        while continue_propagation:
            ray = history[-1]
            hit = self.find_next_intersection(ray)
            
            if not hit:
                break  # ray left the system
            
            new_ray, continue_flag = hit.element.redirect(ray, hit)
            history.append(new_ray)
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
