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
    if False:
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
    else:
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
    return s

if __name__=='__main__':
    main()