import numpy as np
import matplotlib.pyplot as plt

# Define the number of points to interpolate along the parabolic path
num_points = 50

# Define the control points A, C, and B in the X-Z plane
point_a = (0, 0)  # Replace with your actual coordinates
point_c = (50, 15)  # Replace with your actual coordinates
point_b = (100, 0)  # Replace with your actual coordinates

# Calculate the parameters for the parabolic equation
x_a, z_a = point_a
x_c, z_c = point_c
x_b, z_b = point_b

# Calculate the coefficients of the parabolic equation z = ax^2 + bx + c
a = ((z_a - z_b) / ((x_a - x_b) * (x_a - x_c)) - (z_a - z_c) / ((x_a - x_b) * (x_a - x_c))) / (x_c - x_b)
b = ((z_a - z_b) / (x_a - x_b)) - a * (x_a + x_b)
c = z_a - a * x_a ** 2 - b * x_a

# Interpolate points along the parabolic path in the X-Z plane
parabolic_points = []
for t in np.linspace(0, 1, num_points):
    x = x_a + t * (x_b - x_a)
    z = a * x ** 2 + b * x + c
    parabolic_points.append((x, z))

# Separate x and z coordinates for plotting
x_coords, z_coords = zip(*parabolic_points)

# Create a plot of the parabolic path in the X-Z plane
plt.figure(figsize=(8, 6))
plt.plot(x_coords, z_coords, marker='o', linestyle='-', color='b')
plt.title('Parabolic Path in X-Z Plane')
plt.xlabel('X-coordinate')
plt.ylabel('Z-coordinate')
plt.grid(True)
plt.show()
