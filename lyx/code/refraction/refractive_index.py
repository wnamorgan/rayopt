import numpy as np
from scipy.optimize import minimize

if False: # ACL1815U
    filename = 'refraction/ACL1815U'
    r0 = 7.818
    f0 = 15.0
else: # ACL2520
    filename = 'refraction/ACL2520U'
    r0 = 10.462
    f0 = 20.0


data = np.loadtxt(filename, delimiter='\t', dtype=float)
df   = np.array(data[:,1])
λ_um = data[:,0]/1000.0


λ0 = 590
n0 = 1+r0/f0

def compute_n2(B,C,λ_um):
    λ2 = λ_um ** 2
    n2 = 1 + (B[0] * λ2) / (λ2 - C[0]) + (B[1] * λ2) / (λ2 - C[1]) + (B[2] * λ2) / (λ2 - C[2])
    return n2

# Define the function to minimize
def objective_function(x):
    B = x[0:3]
    C = x[3:6]
    #n0 = np.sqrt(compute_n2(B,C,λ0/1e3)) # x[6]
    
    N    = len(df)
    df_comp = np.zeros(N)
    rms_err = 0
    for k,lam_um in enumerate(λ_um):
       n_lam = np.sqrt(compute_n2(B,C,lam_um))
       df_comp[k] = (n0-n_lam)/(n_lam-1)*f0
       rms_err += (df[k]-df_comp[k])**2 
    
    print(rms_err)
    return np.sqrt(rms_err)




import numpy as np


# Initial guess
x0 = np.array([1.79918241, 0.234902303, 1.00946241, 0.014537134, 0.0591563786, 127.000152, 1.5])

# Minimize the function
bounds = [(1,2), (None, None), (None, None), (None, None), (None, None), (None, None), (1.4, 1.6) ]
result = minimize(objective_function, x0, method='SLSQP')#, bounds=bounds)
print(result)