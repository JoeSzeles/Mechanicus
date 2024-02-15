import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import make_interp_spline

Z_start = 19
Z_center = 17
Z_end = 19

# Example line A to B
point_A = (0, 0, Z_start)
point_B = (100, 0, Z_end)
line_length = 100
gradient_length = 4

# Calculate points C and D
point_C = (point_A[0] + gradient_length, point_A[1], Z_center)
point_D = (point_B[0] - gradient_length, point_B[1], Z_center)

# Calculate point E (the midpoint of C and D)
point_E = ((point_C[0] + point_D[0]) / 2, (point_C[1] + point_D[1]) / 2, Z_center)

# Define control points for the Bezier spline
control_points_x = [point_A[0], point_E[0], point_B[0]]
control_points_y = [point_A[1], point_E[1], point_B[1]]
control_points_z = [point_A[2], Z_center, point_B[2]]

# Create the Bezier spline
t = np.linspace(0, 1, 100)
spline_x = make_interp_spline([0, 0.5, 1], control_points_x, k=2)
spline_y = make_interp_spline([0, 0.5, 1], control_points_y, k=2)

# Limit the Z values to not go below Z values of C and D
spline_z = make_interp_spline([0, 0.5, 1], [max(Z_start, Z_center), Z_center, max(Z_end, Z_center)], k=2)

x_values, y_values, z_values = spline_x(t), spline_y(t), spline_z(t)

# Create Z values based on the gradient length
z_gradient_values = []
for x in x_values:
    if x <= point_E[0]:
        z_gradient_values.append(point_A[2] + ((Z_center - Z_start) / gradient_length) * (x - point_A[0]))
    else:
        z_gradient_values.append(Z_center + ((Z_end - Z_center) / gradient_length) * (x - point_E[0]))

# Find the minimum Z value between points C and D
z_min_between_C_and_D = min(z_values)

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_values, y_values, z_values, label='Line')
ax.plot(x_values, y_values, z_gradient_values, label='Gradient', linestyle='dashed')
ax.plot([point_C[0], point_D[0]], [point_C[1], point_D[1]], [point_C[2], point_D[2]], label='New Line', color='green')  # New line passing through point E
ax.scatter([point_A[0], point_C[0], point_D[0], point_B[0], point_E[0]], [point_A[1], point_C[1], point_D[1], point_B[1], point_E[1]],
           [point_A[2], point_C[2], point_D[2], point_B[2], point_E[2]], color='red', marker='o', label='Points')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')
ax.legend()

# Add labels to points
ax.text(point_A[0], point_A[1], point_A[2], 'A', color='red', fontsize=12, ha='right')
ax.text(point_C[0], point_C[1], point_C[2], 'C', color='red', fontsize=12, ha='right')
ax.text(point_D[0], point_D[1], point_D[2], 'D', color='red', fontsize=12, ha='right')
ax.text(point_B[0], point_B[1], point_B[2], 'B', color='red', fontsize=12, ha='right')
ax.text(point_E[0], point_E[1], point_E[2], 'E', color='red', fontsize=12, ha='right')

# Show the minimum Z value between C and D
print(f"Minimum Z value between C and D: {z_min_between_C_and_D}")

# Show the plot
plt.show()
