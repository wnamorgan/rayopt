class ACL1815U():
    def __init__(self):
        self.name      = 'ACL1815U'
        self.tc        = 8.2
        self.D         = 18
        self.EFL       = 15
        self.BFL       = 10
        self.roc       = 7.818
        self.conic     = -1.81700
        self.aspherics = [0, 2.93e-04, 0.0, 0.0, 0.0]
        self.s2_roc    = 0.0

class ACL2520U():
    def __init__(self):
        self.name      = 'ACL2520U'
        self.tc        = 12.0
        self.D         = 25
        self.EFL       = 20.1
        self.BFL       = 12
        self.roc       = 10.462
        self.conic     = -0.6265
        self.aspherics = [0, 1.5e-05, 0.0, 0.0, 0.0]
        self.s2_roc    = 0.0

class EO_16982():
    def __init__(self):
        self.name      = '16-982'
        self.tc        = 10.40
        self.D         = 25
        self.EFL       = 15
        self.BFL       = 9.24
        self.roc       = 12.078
        self.conic     = -0.6243706
        self.aspherics = [0, 2.562558e-06, -2.3980870e-08, -2.9296510e-10, 0.0]        
        self.s2_roc    = 0.0


# This Lens doesn't work
class EO_15888():
    def __init__(self):
        self.name      = '15-888'
        self.tc        = 7.40
        self.D         = 18
        self.EFL       = 13.5
        self.BFL       = 8.64+4.27
        self.roc       = 1/0.141633
        self.conic     = -1.131
        self.aspherics = [0, 2.10e-04, -6.35e-06, 4.60e-8, 0.0]        
        self.conic     = 1.131
        self.aspherics = [0, -2.10e-04, 6.35e-06, -4.60e-8, 0.0]   
        self.s2_roc    = 0.0       


# This Lens doesn't work
class EO_15889():
    def __init__(self):
        self.name      = '15-889'
        self.tc        = 10.90
        self.D         = 20
        self.EFL       = 11
        self.BFL       = 4.86
        self.roc       = 1/0.146826
        self.conic     = -3.014
        self.aspherics = [0, 3.0e-04, -1.97e-6, 0.0, 0.0]        
        self.s2_roc    = -17.7

