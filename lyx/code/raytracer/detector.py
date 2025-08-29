
import numpy as np

def calc_ratios(points,rD,scatter_perc=10):
    (A,B,C,D,T) = (0,0,0,0,0)
    cnt = 0
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
        else:
            cnt += 1            
    az = 0
    el = 0
    if T>0:
        k = min(max(scatter_perc,0.0),50.0)
        sum  = (A+B+C+D) + cnt*k/100.0
        az = ((C+D)-(A+B))/sum
        el = ((A+D)-(B+D))/sum
    return (az,el)