import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import cumulative_trapezoid

# Using loadtxt
data = np.loadtxt('./examples/N-BK7_Ground_Glass_Diffusers.csv', delimiter=',', dtype=float, skiprows=1)
#PDF = cumulative_trapezoid(data[:,1], initial=0)
theta = np.deg2rad(data[:,0])
PDF = cumulative_trapezoid(data[:,-1]*np.abs(np.sin(theta))*np.abs(np.cos(theta)),theta, initial=0)
fig,ax = plt.subplots(2,1)
ax[0].plot(data[:,0],data[:,-1])
ax[1].plot(data[:,0],PDF)

idx0 = np.where(theta>0)[0][0]
fig, ax = plt.subplots()
ax.plot(np.rad2deg(theta[idx0:]),data[idx0:,1],label='120 Grid')
ax.plot(np.rad2deg(theta[idx0:]),data[idx0:,2],label='220 Grit')
ax.plot(np.rad2deg(theta[idx0:]),data[idx0:,3],label='600 Grit')
ax.plot(np.rad2deg(theta[idx0:]),data[idx0:,4],label='1500 Grit')
ax.grid(True)
ax.legend()
ax.set_xlabel('Angle (deg)')
ax.set_ylabel('BSDF (1/Sr)')
ax.set_xscale('log')
ax.set_yscale('log')
plt.savefig("GlassDiffuser",dpi=400) # 14.1 
plt.show()
