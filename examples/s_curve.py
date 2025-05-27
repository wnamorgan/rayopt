import time
from examples.fourQD import get_system, ray_bundle, calc_ratios
import numpy as np
import matplotlib.pyplot as plt
from lens import *

def Single_Scurve(lens,hD,dD,Amax=20):
    s = get_system(lens,hD)

    N_ang=50
    N_rays=400
    start = time.time()
    az = np.zeros(N_ang)
    el = np.zeros(N_ang)
    angles = np.linspace(0,Amax,N_ang)
    
    for k, angle in enumerate(angles):
        direction = np.array([np.sin(np.deg2rad(angle)), 0.0, np.cos(np.deg2rad(angle))])     # Pointing along +z
        points = ray_bundle(s,direction,N_rays)
        b = 0
        (az[k],el[k]) = calc_ratios(points,dD/2,0)
        print(f"(rho_az,rho_el) = ({az},{el})")
    end = time.time()
    print(f"Took {end - start:.2f} seconds")   
    return (az, angles)


def Plot_Single_Scurve(lens,hD,dD,Amax=20):

    (az,angles) = Single_Scurve(lens,hD,dD,Amax)

    FigName = f"Scurve_{lens.name}_{dD}_{hD}.jpg"
    fig, ax = plt.subplots()
    az = np.append(-az[:0:-1], az)
    angles = np.append(-angles[:0:-1], angles)

    ax.plot(angles,az,color = 'blue')
    #ax.plot(-angles,-az, color = 'blue')

    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('4QD Response')
    ax.set_xlim([-Amax,Amax])
    ax.grid(True)
    plt.savefig(FigName,dpi=400) # 14.1 

def Sweep(lens,hD,dD,Amax=20):

    hDvals = [3.0, 4.0, 5.0, 6.0, 7.0]
    #hDvals = [2.5, 3.0, 3.5, 4.0, 4.5]
    hDvals = [-2.0, 2.0]
    FigName = f"ScurveSweep_{lens.name}_{dD}.jpg"
    fig, ax = plt.subplots()
    for k,hD in enumerate(hDvals):
        (az,angles) = Single_Scurve(lens,hD,dD,Amax)
        az = np.append(-az[:0:-1], az)
        angles = np.append(-angles[:0:-1], angles)
        ax.plot(angles,az,label=f"{hD} mm")
  
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('4QD Response')
    ax.set_xlim([-Amax,Amax])
    ax.grid(True)
    ax.legend()
    plt.savefig(FigName,dpi=400) # 14.1     

def main():

    Amax = 15
    
    (lens, hD, dD) = (ACL1815U(), 2.8, 5.33) # Baseline Lens, Baseline Detector (2.8)
    #(lens, hD, dD) = (ACL1815U(), 5.0, 14.1) # Baseline lens, Big Detector (5.0)
    #(lens, hD, dD) = (ACL2520U(), 6.0, 14.1) # Big Thor lens, Big Detector (5.0)
    #(lens, hD, dD) = (ACL2520U(), 3.5, 5.33) # Big Thor Lens, Baseline Detector (2.8)
    #(lens, hD, dD) = (EO_15889(), 2, 5.33)

    hD=2.8
    #Plot_Single_Scurve(lens,hD,dD,Amax=20)
    #Sweep(lens,hD,dD,Amax)
    PosVsNeg(lens,hD,dD,Amax)
    plt.show()




def PosVsNeg(lens,hD,dD,Amax=20):

    roygbiv_colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF']
    colors =         ['#FF0000', '#0000FF', '#008000', '#FFFF00', '#00FFFF', '#FF00FF', '#FFA500']


    hDvals = [3.0, 4.0, 5.0, 6.0, 7.0]
    hDvals = [2.5, 3.0, 3.5, 4.0, 4.5]
    FigName = f"ScurveSweep_{lens.name}_{dD}_PM.jpg"
    fig, ax = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
    for k,hD in enumerate(hDvals):
        (az,angles) = Single_Scurve(lens,hD,dD,Amax)
        az = np.append(-az[:0:-1], az)
        angles = np.append(-angles[:0:-1], angles)
        ax[0].plot(angles,az,label=f"{hD} mm")

        (az,angles) = Single_Scurve(lens,-hD,dD,Amax)
        az = np.append(-az[:0:-1], az)
        angles = np.append(-angles[:0:-1], angles)
        ax[1].plot(angles,az,label=f"-{hD} mm")        
  
    ax[0].set_xlabel('Angle (deg)')
    ax[0].set_ylabel('4QD Response')
    ax[0].set_xlim([-Amax,Amax])
    ax[0].grid(True)
    ax[0].legend()
    ax[1].set_xlabel('Angle (deg)')
    ax[1].set_ylabel('4QD Response')
    ax[1].set_xlim([-Amax,Amax])
    ax[1].grid(True)
    ax[1].legend()    
    plt.savefig(FigName,dpi=400) # 14.1      

if __name__=='__main__':
    main()