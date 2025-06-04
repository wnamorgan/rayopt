import numpy as np

def generate_hex_grid(N, xlim=(0, 1), ylim=(0, 1)):
    # Horizontal spacing
    dx = (xlim[1] - xlim[0]) / N
    dy = dx * np.sqrt(3) / 2  # vertical spacing for hex grid

    # Create a skewed hexagonal grid using a basis:
    # a1 = [dx, 0], a2 = [dx/2, dy]
    max_x = xlim[1]
    max_y = ylim[1]
    x_vals = []
    y_vals = []

    for i in range(N * 2):  # oversample to ensure coverage
        for j in range(N * 2):
            x = xlim[0] + i * dx + (j % 2) * dx / 2
            y = ylim[0] + j * dy
            if xlim[0] <= x <= max_x and ylim[0] <= y <= max_y:
                x_vals.append(x)
                y_vals.append(y)

    return np.array(x_vals), np.array(y_vals)




def generate_random_grid(N, xlim=(0, 1), ylim=(0, 1)):
    dx = (xlim[1] - xlim[0]) / N
    dy = (ylim[1] - ylim[0]) / N

    x_vals = []
    y_vals = []

    for i in range(N):
        for j in range(N):
            x = xlim[0] + (i + np.random.rand()) * dx
            y = ylim[0] + (j + np.random.rand()) * dy
            x_vals.append(x)
            y_vals.append(y)

    return np.array(x_vals), np.array(y_vals)


def generate_uniform_grid(N, xlim=(0, 1), ylim=(0, 1)):
    x = np.linspace(xlim[0], xlim[1], N)
    y = np.linspace(ylim[0], ylim[1], N)
    xx, yy = np.meshgrid(x, y)
    return xx.ravel(), yy.ravel()

def generate_hex_grid2(N, xlim=(0, 1), ylim=(0, 1)):
    """
    Generate a hexagonal grid with approximately N x N points
    within the rectangular region defined by xlim and ylim.

    Returns:
        x_flat: 1D array of x coordinates
        y_flat: 1D array of y coordinates
    """
    # Width and height of the domain
    x_min, x_max = xlim
    y_min, y_max = ylim
    width = x_max - x_min
    height = y_max - y_min

    # Horizontal and vertical spacing for hexagons
    dx = width / N
    dy = dx * np.sqrt(3) / 2

    # Number of rows to cover the vertical span
    n_rows = int(np.ceil(height / dy)) + 1
    n_cols = N + 1  # Pad by 1 to ensure edge coverage

    x = []
    y = []
    for j in range(n_rows):
        yj = y_min + j * dy
        if yj > y_max:
            continue
        offset = dx / 2 if j % 2 else 0
        for i in range(n_cols):
            xi = x_min + i * dx + offset
            if xi > x_max:
                continue
            x.append(xi)
            y.append(yj)

    return np.array(x), np.array(y)

def generate_jittered_grid(N, xlim=(0, 1), ylim=(0, 1)):
    dx = (xlim[1] - xlim[0]) / N
    dy = (ylim[1] - ylim[0]) / N

    x_vals = []
    y_vals = []

    rng = np.random.default_rng(seed=42)

    for i in range(N):
        for j in range(N):
            x = xlim[0] + (i + rng.uniform(0.2, 0.8)) * dx
            y = ylim[0] + (j + rng.uniform(0.2, 0.8)) * dy
            x_vals.append(x)
            y_vals.append(y)

    return np.array(x_vals), np.array(y_vals)