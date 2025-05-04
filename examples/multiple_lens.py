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
    text = """
        S       0      0    10 AIR
        S  25.907     10  10.6 SCHOTT-BK|N-BK7
        S 147.341  5.083  8.98 AIR
        S  34.804  2.355  6.05 LZOS-F|F4
        S  17.340  1.694  5.25 AIR
        A       0  2.542  5.15 AIR
        S  -17.34  2.542   5.2 LZOS-F|F4
        S -34.804  1.694    6. AIR
        S -138.87  2.355   8.6 SCHOTT-BK|N-BK7
        S -24.396  5.083 10.24 AIR
        S       0 89.832    63 AIR
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