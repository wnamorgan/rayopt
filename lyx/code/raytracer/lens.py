
from scipy.interpolate import interp1d
import numpy as np

class refractive_material():
    def __init__(self):
        pass
    def compute_n(self, λ_um):
        (B, C) = (self.B,self.C)
        λ2 = λ_um ** 2
        n2 = 1 + (B[0] * λ2) / (λ2 - C[0]) + (B[1] * λ2) / (λ2 - C[1]) + (B[2] * λ2) / (λ2 - C[2])
        return n2 ** 0.5
    def focal_shift(self, f0, n0, n_lambda):
        return (n0 - 1) / (n_lambda - 1) * f0
    
class BK7(refractive_material):
    def __init__(self):
        super().__init__()        
        self.B = [1.03961212, 0.231792344, 1.01046945]
        self.C = [0.00600069867, 0.0200179144, 103.560653]

class BAL35(refractive_material):
    def __init__(self):
        super().__init__()      
        self.B = [0.92873, 0.49620, 1.09463]
        self.C = [0.0089160, 0.0466400, 112.40597]

class SLAH64(refractive_material):
    def __init__(self):
        super().__init__()        
        self.B = [1.79918241, 0.234902303, 1.00946241]
        self.C = [0.014537134, 0.0591563786, 127.000152]

class B270(refractive_material): # B270 lens haqve a manufacturing tolerance that allows for pm8% deviation of specified focal length!
    def __init__(self):
        super().__init__()
        # Manufacture (Thor) provides focal deviations as a function of frequency.  I converted this into equivalent Sellmeier parameters       
        self.B = [1.360,  0.004348,  1.683]
        self.C = [0.01544, -0.2422, 127.1]
    

class ACL2520(B270):
    def __init__(self,λ_um=None):
        super().__init__()        
        self.B = [4.687e-03,  1.281e+00,  1.053e+00]
        self.C = [-2.709e-01,  1.016e-02, 1.272e+02]
        self.name     = 'ACL2520'
        self.D        = 25.0
        self.fb       = 12 + .35 # This fudge factor was likely needed because these B270 lense only have pm8% accuracy, and the data used to construct B and C was from testing of a specific lens
        self.λ_um_des = 590e-3
        self.n        = self.compute_n(self.λ_um_des)#1.52        
        self.roc      = 10.462
        self.tc       = 12.0
        self.conic    = -0.6265
        self.aspheric = [1.5e-05]  # A_4

class ACL1815(B270):
    def __init__(self,λ_um=None):
        super().__init__()        
        self.name     = 'ACL1815'
        self.B = [3.868e-03,  1.283e+00,  8.543e-01]
        self.C = [-3.100e-01,  8.168e-03, 1.270e+02]
        self.D        = 18.0
        self.fb       = 10 #- 0.23 # This fudge factor was likely needed because these B270 lense only have pm8% accuracy, and the data used to construct B and C was from testing of a specific lens
        self.λ_um_des = 587.6e-3
        self.n        = self.compute_n(self.λ_um_des)        
        #self.n        = 1.52
        self.roc      = 7.818
        self.tc       = 8.2
        self.conic    = -1.817
        self.aspheric = [0.0, 2.93e-04]  # A_4

class AL1815(SLAH64):
    def __init__(self,λ_um=None):
        super().__init__()        
        self.name     = 'AL1815'
        self.D        = 18.0
        self.fb       = 11.5
        self.λ_um_des = 590e-3
        self.n        = self.compute_n(self.λ_um_des)#1.7880                
        self.roc      = 11.65
        self.tc       = 6.2
        self.conic    = -1.1
        self.aspheric = [0.0, 3.6906721e-5, -1.2854612e-8, -1.4001677e-10, -2.5131166e-13, 5.0178988e-16, 5.8558715e-18, -1.1277944e-20]

class AL1512(SLAH64):
    def __init__(self,λ_um=None):
        super().__init__()
        self.name     = 'AL1512'
        self.D        = 15.0
        self.fb       = 9.0
        self.λ_um_des = 587.6e-3
        self.n        = self.compute_n(self.λ_um_des)#1.7880
        self.roc      = 9.32
        self.tc       = 5.3
        self.conic    = -1.0
        self.aspheric = [0.0, 5.7598697e-05, -2.503422e-08, -6.7519988e-10, -2.0018474e-12, 3.8684828e-15, 1.2447477e-16, -3.659331e-19]


class AL75150(BK7):
    # Actual focal distand 8s at 140.1-2.45 per this ray tracer (could be other things like index 
    # of refraction difference; main point is the user will need to tune lens separation if this is 
    # used in a beam expander)
    def __init__(self,λ_um=None): # EFL = 150.0
        super().__init__()    
        self.name     = 'AL75150'
        self.D        = 75.0
        self.fb       = 140.1
        self.λ_um_des = 780e-3
        self.n        = self.compute_n(self.λ_um_des)#1.52
        self.roc      = 76.68
        self.tc       = 15.0
        self.conic    = -0.675
        self.aspheric = [0.0, 2.7709219e-08, 6.418186e-13, -1.5724014e-17, -2.7768768e-21, -2.590162e-25]

class EO22714(BK7):
    def __init__(self,λ_um=None): # EFL = 112.5
        super().__init__()
        self.name = 'EO22714'
        self.D        = 75.0
        self.fb       = 101.42
        self.n        = 1.5168
        self.roc      = 58.14
        self.tc       = 16.81
        self.conic    = -0.952
        self.aspheric = [0.0, 2.425e-07, 1.252e-11, 5.21e-16]


class EO49109(BAL35):
    def __init__(self,λ_um=None): # EFL = 112.5
        super().__init__()
        self.name = 'EO49109'
        self.D        = 15.0
        self.fb       = 6.85
        self.λ_um_des = 587.6e-3
        self.n        = self.compute_n(self.λ_um_des)    
        self.roc      = 6.628
        self.tc       = 7.00
        self.conic    = -1.076527
        self.aspheric = [0.0, 2.396040E-04, 6.414674E-07, 7.685840E-09]