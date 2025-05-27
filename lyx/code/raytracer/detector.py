
import numpy as np

def calc_ratios(points,rD):
    (A,B,C,D,T) = (0,0,0,0,0)
    for point in points:
        x = point[0]
        y = point[1]
        r = np.sqrt(x**2+y**2)
        if r<rD:
            T=T+1
            if x < 0:
                if y < 0:
                    B = B+1
                else:
                    A = A+1
            else:
                if y < 0:
                    C = C+1
                else:
                    D = D+1
        az = 0
        el = 0
        if T>0:
            az = ((C+D)-(A+B))/(A+B+C+D)
            el = ((A+D)-(B+D))/(A+B+C+D)
    return (az,el)