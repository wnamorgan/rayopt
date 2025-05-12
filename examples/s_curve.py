import time
from examples.fourQD import get_system, ray_bundle, calc_ratios
import numpy as np
import matplotlib.pyplot as plt

def main():
    s = get_system()

    N_ang=20
    N_rays=100
    start = time.time()
    
    az = np.zeros(N_ang)
    el = np.zeros(N_ang)
    angles = np.linspace(0,12,N_ang)
    
    for k, angle in enumerate(angles):
        direction = np.array([np.sin(np.deg2rad(angle)), 0.0, np.cos(np.deg2rad(angle))])     # Pointing along +z
        points = ray_bundle(s,direction,N_rays)
        (az[k],el[k]) = calc_ratios(points,5.3/2)
        print(f"(rho_az,rho_el) = ({az},{el})")
    end = time.time()
    print(f"Took {end - start:.2f} seconds")   
    fig, ax = plt.subplots()
    ax.plot(angles,az)
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('4QD Response')
    ax.grid(True)
    plt.show()
if __name__=='__main__':
    main()