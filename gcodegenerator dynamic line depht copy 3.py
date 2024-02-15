import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import make_interp_spline

def generate_bezier_spline_semi_circle(radius, z_start, z_center, z_end, num_points, gradient_length_percentage):
    # Generate points for a semi-circle
    theta = np.linspace(0, np.pi, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    # Calculate the gradient length as a percentage of the overall length
    gradient_length = round((gradient_length_percentage / 100) * (2 * radius), 2)

    # Calculate points C and D
    point_C = (x[1], y[1], z_center)
    point_D = (x[-2], y[-2], z_center)

    # Define control points for the Bezier spline
    control_points_x = [x[0], point_C[0], point_D[0], x[-1]]
    control_points_y = [y[0], point_C[1], point_D[1], y[-1]]
    control_points_z = [z_start, z_center, z_center, z_end]

    # Create the Bezier spline
    t = np.linspace(0, 1, num_points)
    spline_x = make_interp_spline([0, 0.333, 0.666, 1], control_points_x, k=2)
    spline_y = make_interp_spline([0, 0.333, 0.666, 1], control_points_y, k=2)
    spline_z = make_interp_spline([0, 0.333, 0.666, 1], control_points_z, k=2)
    x_values, y_values, z_values = spline_x(t), spline_y(t), spline_z(t)

    # Create Z values based on a smooth gradient
    z_gradient_values = []
    t_gradient = np.linspace(0, 1, num_points)  # Finer resolution for the gradient
    for i, x_val in enumerate(x_values):
        if x_val <= point_C[0]:
            z_gradient_values.append(z_start + ((z_center - z_start) / gradient_length) * (x_val - x[0]))
        elif x_val >= point_D[0]:
            z_gradient_values.append(z_center + ((z_end - z_center) / gradient_length) * (x_val - x[-1]))
        else:
            # Smooth transition between the two gradient segments
            t_segment = (x_val - point_C[0]) / (point_D[0] - point_C[0])
            z_gradient_values.append(z_center + t_segment * ((z_end - z_start) / gradient_length))

    return x_values, y_values, z_values, z_gradient_values, control_points_x, control_points_y, control_points_z

# Generate Bezier spline for the semi-circle
# Define the bed size
bed_size_x = 300  # mm
bed_size_y = 300  # mm

z_end = 19.2
gradient_length_percentage = 20
# Example usage of the function with adjustable parameters:
z_start = 19.2
z_center = 18.5
z_end = 19.2
gradient_length_percentage = 20

# Adjust the radius and number of points to fit within the bed size
radius = min(bed_size_x, bed_size_y) / 2  # Radius is half of the minimum bed dimension
num_points = 16

x_values, y_values, z_values, z_gradient_values, control_points_x, control_points_y, control_points_z = generate_bezier_spline_semi_circle(
    radius=radius, z_start=z_start, z_center=z_center, z_end=z_end,
    num_points=num_points, gradient_length_percentage=gradient_length_percentage
)

x_values, y_values, z_values, z_gradient_values, control_points_x, control_points_y, control_points_z = generate_bezier_spline_semi_circle(
    radius=50, z_start=z_start, z_center=z_center, z_end=z_end,
    num_points=16, gradient_length_percentage=gradient_length_percentage
)

# Create the 3D plot to visualize the Bezier spline and gradient
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_values, y_values, z_values, label='Semi-circle')
ax.plot(x_values, y_values, z_gradient_values, label='Gradient', linestyle='dashed')
ax.scatter(control_points_x, control_points_y, control_points_z, color='red', marker='o', label='Control Points')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')
ax.legend()
plt.show()

def generate_marlin_gcode_for_bezier_spline(x_values, y_values, z_values, feedrate, output_file):
    # Open the output file for writing
    with open(output_file, 'w') as file:
        # Write G-code commands to move to the starting position
        file.write("; Move to the starting point\n")
        file.write("G28 ; Home all axes\n")
        file.write("G1 Z0 F{0} ; Move Z to starting position\n".format(feedrate))
        file.write("G1 X{0} Y{1} Z{2} F{3} ; Move to the starting position\n".format(
            x_values[0], y_values[0], z_values[0], feedrate))

        # Write G-code commands to follow the Bezier spline
        file.write("; Follow Bezier Spline\n")
        for i in range(1, len(x_values)):
            file.write("G1 X{0} Y{1} Z{2} F{3} ; Move to next point\n".format(
                x_values[i], y_values[i], z_values[i], feedrate))

    print("G-code written to", output_file)

# Example usage of the function to generate Marlin G-code
feedrate = 3000  # Adjust the feedrate as needed
output_file = "bezier_spline.gcode"

generate_marlin_gcode_for_bezier_spline(x_values, y_values, z_values, feedrate, output_file)
