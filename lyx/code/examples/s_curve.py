import time
import numpy as np
import matplotlib.pyplot as plt
import sys, os
# Add the parent directory of raytracer/ to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from raytracer.lens import *
from examples.fourQD import make_system, RayBundle

def Single_Point(lens,hD,dD,ang=10):
    s = make_system(lens,hD)
    N_rays=200
    start = time.time()    
    (az,el) = RayBundle(s,angle=ang,N=N_rays,dD=dD)
    print(f"(rho_az,rho_el) = ({az},{el})")
    end = time.time()
    print(f"Took {end - start:.2f} seconds")   


def Single_Scurve(lens,hD,dD,Amax=15):
    s = make_system(lens,hD)

    N_ang=10
    N_rays=200
    start = time.time()
    az = np.zeros(N_ang)
    el = np.zeros(N_ang)
    angles = np.linspace(0,Amax,N_ang)
    
    for k, ang in enumerate(angles):
        (az[k],el[k]) = RayBundle(s,angle=ang,N=N_rays,dD=dD)
        print(f"(rho_az,rho_el) = ({az[k]},{el[k]})")
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
    #plt.savefig(FigName,dpi=400) # 14.1 

def Sweep(lens,hD,dD,Amax=20):

    hDvals = [3.0, 4.0, 5.0, 6.0, 7.0]
    #hDvals = [2.5, 3.0, 3.5, 4.0, 4.5]
    #hDvals = [-2.0, 2.0]
    #hDvals = [14,16,18,20]
    hDvals = [2.4,2.6,2.8,3.0,3.2]
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
    (lens,offset,dD) = (ACL2520(),4.0,14.1)
    (lens,offset,dD) = (EO15731(),2.5,5.33)
    #(lens,offset,dD) = (EO48769(),20.0,14.1)
    #Single_Point(lens,offset,dD,ang=10)
    #Plot_Single_Scurve(lens,offset,dD,Amax=Amax)
    Sweep(lens,offset,dD,Amax)
    #PosVsNeg(lens,hD,dD,Amax)
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