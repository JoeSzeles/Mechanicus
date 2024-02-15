import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

Z_start = 10
Z_center = 0
Z_end = 10

# Example line A to B
point_A = (0, 0, Z_start)  # Point A: (x, y, Z_start)
point_B = (100, 0, Z_end)  # Point B: (x, y, Z_end)
line_length = 100  # Length of the line in mm
gradient_length = 20  # Gradient length in mm

# Calculate points C and D
point_C = (point_A[0] + gradient_length, point_A[1], Z_center)  # Point C: (x, y, Z_center)
point_D = (point_B[0] - gradient_length, point_B[1], Z_center)  # Point D: (x, y, Z_center)

# Create points along the line for plotting
num_points = 100  # Number of points for visualization
points = np.linspace(0, line_length, num_points)
x_values = [point_A[0] + (point_B[0] - point_A[0]) * t / line_length for t in points]
y_values = [point_A[1] + (point_B[1] - point_A[1]) * t / line_length for t in points]
z_values = [point_A[2] + (point_B[2] - point_A[2]) * t / line_length for t in points]

# Create Z values based on the gradient length
z_gradient_values = []
for x in x_values:
    if x <= point_C[0]:
        z_gradient_values.append(point_A[2] + ((Z_center - Z_start) / gradient_length) * (x - point_A[0]))
    elif x >= point_D[0]:
        z_gradient_values.append(Z_center + ((Z_end - Z_center) / gradient_length) * (x - point_D[0]))
    else:
        z_gradient_values.append(Z_center)

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_values, y_values, z_values, label='Line')
ax.plot(x_values, y_values, z_gradient_values, label='Gradient', linestyle='dashed')
ax.scatter([point_A[0], point_C[0], point_B[0]], [point_A[1], point_C[1], point_B[1]],
           [point_A[2], point_C[2], point_B[2]], color='red', marker='o', label='Points')
ax.plot([point_D[0], point_B[0]], [point_D[1], point_B[1]], [point_D[2], point_B[2]], color='red', marker='o')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')
ax.legend()

# Add labels to points
ax.text(point_A[0], point_A[1], point_A[2], 'A', color='red', fontsize=12, ha='right')
ax.text(point_C[0], point_C[1], point_C[2], 'C', color='red', fontsize=12, ha='right')
ax.text(point_D[0], point_D[1], point_D[2], 'D', color='red', fontsize=12, ha='right')
ax.text(point_B[0], point_B[1], point_B[2], 'B', color='red', fontsize=12, ha='right')

# Show the plot
plt.show()
