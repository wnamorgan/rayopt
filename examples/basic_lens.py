# basic_lens.py

import rayopt as ro
from   rayopt import system_from_text, Analysis, GeometricTrace
from   rayopt.gaussian_trace import GaussianTrace
import matplotlib.pyplot as plt

def main():
    s = get_system()
    print(s)
    fig, ax = plt.subplots()
    s.plot(ax)
    t = GeometricTrace(s)
    h=0.0
    t.rays_clipping((0, h))
    t.plot(ax)

    #ro.Analysis(s,plot_transverse=False,plot_spots=False,plot_opds=False,plot_longitudinal=False)
    plt.show()

def get_system():
    method=2
    if method==0:
        s = ro.system_from_yaml("""
        object:
          pupil:
            radius: 1
        elements:
        - {}
        - {distance: 1, material: 1.5, roc: 5, radius: 1}
        - {distance: 0.8, material: AIR, roc: 1000000, radius: 1}
        - {distance: .2, material: 1.0}
        - {}
        """)
        s.update()
    elif method==1:
        text = """
            S       0      0     2 AIR
            S       1.25      1     1 SCHOTT-BK|N-BK7
            S       0    1.0     1 AIR
            S       0    2.0     2 AIR
            """
        columns = "type roc distance radius material"
        s = system_from_text(text, columns.split(),
            description="four element double gauss, intermediate optical design")
        s.object.angle = .36
        s.object.pupil.update_radius = True
        s.fields = 0, .7, 1.
        s.update()
    else:
        text = """
            S       0      0      10 AIR
            S       7.818  1       9 SCHOTT-BK|N-BK7
            S       0      8.2     9 AIR
            S       0      10.0     2 AIR
            """
        columns = "type roc distance radius material"
        s = system_from_text(text, columns.split(),
        description="four element double gauss, intermediate optical design")
        s.object.angle = 20
        s.object.pupil.update_radius = True
        s.fields = 0, .7, 1.

        s[1].conic = -1.81700
        s[1].aspherics = [0,2.93e-04, 0.0, 0.0, 0.0]

        s.update()
    return s

if __name__=='__main__':
    main()