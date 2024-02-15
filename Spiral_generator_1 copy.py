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

# Define the dimensions of the rectangular mosaic
Xo = 12  # Number of times to replicate along the x-axis
Yo = 6   # Number of times to replicate along the y-axis
Xgap = 0  # Gap between replicated patterns along the x-axis
Ygap = 0  # Gap between replicated patterns along the y-axis

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
for x in np.linspace(0, mosaic_width, n_points):
    rectangle_x.append(x)
    rectangle_y.append(0)

# Right edge of the rectangle
for y in np.linspace(0, mosaic_height, n_points):
    rectangle_x.append(mosaic_width)
    rectangle_y.append(y)

# Bottom edge of the rectangle
for x in np.linspace(mosaic_width, 0, n_points):
    rectangle_x.append(x)
    rectangle_y.append(mosaic_height)

# Left edge of the rectangle
for y in np.linspace(mosaic_height, 0, n_points):
    rectangle_x.append(0)
    rectangle_y.append(y)

# Plot the rectangle
plt.figure(figsize=(10, 10))
plt.plot(rectangle_x, rectangle_y, 'r-')

# Plot the mosaic without connecting lines (spiral outline)
current_spiral = []
for x, y in zip(x_values, y_values):
    current_spiral.append((x, y))

current_spiral = np.array(current_spiral)

# Replicate the spiral pattern according to your specified pattern (blue spirals)
x_offset = 0
y_offset = 0

for _ in range(Xo):
    plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
    x_offset += pattern_width + Xgap

for _ in range(Yo):
    plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
    y_offset += pattern_height + Ygap

for _ in range(Xo):
    plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
    x_offset -= pattern_width + Xgap

for _ in range(Yo):
    plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
    y_offset -= pattern_height + Ygap

# Create a new rectangle (centered, 2 blocks wider, and 2 blocks higher than the original)
new_width = mosaic_width + 2 * pattern_width
new_height = mosaic_height + 2 * pattern_height
new_x = (mosaic_width - new_width) / 2
new_y = (mosaic_height - new_height) / 2

new_rectangle_x2 = []
new_rectangle_y2 = []

# Top edge of the new rectangle
for x in np.linspace(new_x, new_x + new_width, n_points):
    new_rectangle_x2.append(x)
    new_rectangle_y2.append(new_y)

# Right edge of the new rectangle
for y in np.linspace(new_y, new_y + new_height, n_points):
    new_rectangle_x2.append(new_x + new_width)
    new_rectangle_y2.append(y)

# Bottom edge of the new rectangle
for x in np.linspace(new_x + new_width, new_x, n_points):
    new_rectangle_x2.append(x)
    new_rectangle_y2.append(new_y + new_height)

# Left edge of the new rectangle
for y in np.linspace(new_y + new_height, new_y, n_points):
    new_rectangle_x2.append(new_x)
    new_rectangle_y2.append(y)

# Plot the new rectangle
plt.plot(new_rectangle_x2, new_rectangle_y2, 'r-')

# Calculate the spacing between spiral patterns
x_spacing = pattern_width + Xgap if Xgap > 0 else pattern_width
y_spacing = pattern_height + Ygap if Ygap > 0 else pattern_height

# Plot the spiral patterns within the new rectangle (green spirals)
green_spiral_x_offset = new_x
green_spiral_y_offset = new_y

for _ in range(Xo):
    for _ in range(Yo):
        shifted_x_values = [x + green_spiral_x_offset for x in x_values]
        shifted_y_values = [y + green_spiral_y_offset for y in y_values]
        plt.plot(shifted_x_values, shifted_y_values, 'g-')
        green_spiral_x_offset += pattern_width + Xgap
    green_spiral_x_offset = new_x
    green_spiral_y_offset += pattern_height + Ygap

plt.title("Square Root Spiral Pattern with Specified Replication")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.grid(True)
plt.axis('equal')
plt.show()
