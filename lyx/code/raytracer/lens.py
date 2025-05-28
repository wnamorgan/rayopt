
class ACL2520():
    def __init__(self):
        self.name     = 'ACL2520'
        self.D        = 25.0
        self.fb       = 12
        self.n        = 1.52
        self.roc      = 10.462
        self.tc       = 12.0
        self.conic    = -0.6265
        self.aspheric = [1.5e-05]  # A_4

class ACL1815():
    def __init__(self):
        self.name     = 'ACL1815'
        self.D        = 18.0
        self.fb       = 10
        self.n        = 1.52
        self.roc      = 7.818
        self.tc       = 8.2
        self.conic    = -1.817
        self.aspheric = [2.93e-04]  # A_4

class AL1815():
    def __init__(self):
        self.name     = 'AL1815'
        self.D        = 18.0
        self.fb       = 11.5
        self.n        = 1.79
        self.roc      = 11.65
        self.tc       = 6.2
        self.conic    = -1.1
        self.aspheric = [3.6906721e-5, -1.2854612e-8, -1.4001677e-10, -2.5131166e-13, 5.0178988e-16, 5.8558715e-18, -1.1277944e-20]

class AL75150():
    # Actual focal distand 8s at 140.1-2.45 per this ray tracer (could be other things like index 
    # of refraction difference; main point is the user will need to tune lens separation if this is 
    # used in a beam expander)
    def __init__(self):
        self.name     = 'AL75150'
        self.D        = 75.0
        self.fb       = 140.1-2.45 
        self.n        = 1.52
        self.roc      = 76.68
        self.tc       = 15.0
        self.conic    = -0.675
        self.aspheric = [2.7709219e-8, 6.418186e-13, -1.5724014e-17, -2.7768768e-21, -2.590162e-25]
