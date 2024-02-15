import matplotlib.pyplot as plt
import numpy as np

# Define the functions i(x) and j(x)
def i(x):
    result = 0
    for n in range(1, int(x) + 1):
        result += np.sin((np.pi / 2) * np.floor(np.sqrt(4 * n - 3)))
    return result

def j(x):
    result = 0
    for n in range(1, int(x) + 1):
        result += np.cos((np.pi / 2) * np.floor(np.sqrt(4 * n - 3)))
    return result

# Generate the points for the square root spiral
k = 100
m = 71  # Adjust the number of spiral turns
n_points = m * 3  # Number of points to generate
t_values = np.linspace(1, m, n_points)
x_values = [i(t) + (t % 1) * (i(t + 1) - i(t)) for t in t_values]
y_values = [j(t) + (t % 1) * (j(t + 1) - j(t)) for t in t_values]

# Initialize variables for concentric rectangles
Nsteps = 3  # Number of concentric rectangles
Xblocks = 30
YBlocks = 15
Xgap = 1  # Gap between replicated patterns along the x-axis
Ygap = 1  # Gap between replicated patterns along the y-axis

# Create a single plot to combine all concentric rectangles
plt.figure(figsize=(10, 10))

# Create a loop to draw concentric rectangles with spirals
for step in range(Nsteps):
    Xo = Xblocks - step * 2  # Number of times to replicate along the x-axis
    Yo = YBlocks - step * 2   # Number of times to replicate along the y-axis

    # Calculate the size of the individual pattern
    pattern_width = max(x_values) - min(x_values)
    pattern_height = max(y_values) - min(y_values)

    # Calculate the total width and height of the mosaic
    mosaic_width = Xo * pattern_width + (Xo - 1) * Xgap
    mosaic_height = Yo * pattern_height + (Yo - 1) * Ygap

    # Create the rectangle as a list of points along the outline
    rectangle_x = []
    rectangle_y = []

    # Top edge of the rectangle
    for x in np.linspace(-mosaic_width / 2, mosaic_width / 2, n_points):
        rectangle_x.append(x)
        rectangle_y.append(mosaic_height / 2)

    # Right edge of the rectangle
    for y in np.linspace(-mosaic_height / 2, mosaic_height / 2, n_points):
        rectangle_x.append(mosaic_width / 2)
        rectangle_y.append(y)

    # Bottom edge of the rectangle
    for x in np.linspace(mosaic_width / 2, -mosaic_width / 2, n_points):
        rectangle_x.append(x)
        rectangle_y.append(-mosaic_height / 2)

    # Left edge of the rectangle
    for y in np.linspace(mosaic_height / 2, -mosaic_height / 2, n_points):
        rectangle_x.append(-mosaic_width / 2)
        rectangle_y.append(y)

    # Plot the rectangle with red outline
    plt.plot(rectangle_x, rectangle_y, 'r-')

    # Plot the mosaic without connecting lines (spiral outline)
    current_spiral = []
    for x, y in zip(x_values, y_values):
        current_spiral.append((x, y))

    current_spiral = np.array(current_spiral)

    # Calculate the offset for centering
    x_offset = mosaic_width / 2
    y_offset = mosaic_height / 2

    # Replicate the spiral pattern along the rectangle outline (blue spirals)
    for _ in range(Xo):
        plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
        x_offset -= pattern_width + Xgap

    for _ in range(Yo):
        plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
        y_offset -= pattern_height + Ygap

    for _ in range(Xo):
        plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
        x_offset += pattern_width + Xgap

    for _ in range(Yo):
        plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
        y_offset += pattern_height + Ygap

# Title and labels for the combined plot
plt.title("Concentric Rectangles with Spirals")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.grid(True)
plt.axis('equal')
plt.show()
