import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
line_length = 100  # Line length remains the same
num_repetitions = 80
amplitude_x = 2  # Amplitude of the sinusoidal pattern for X-axis
amplitude_y = 1  # Amplitude of the sinusoidal pattern for Y-axis
min_laser_power = 0
max_laser_power = 1000
frequency_x = 4  # Frequency of the sinusoidal pattern for X-axis
frequency_y = 4  # Frequency of the sinusoidal pattern for Y-axis
feed_rate = 250  # Set the feed rate to 500 units per minute (adjust as needed)

# Function to calculate laser power based on Y-axis position
def calculate_laser_power(y_position):
    raw_power = min_laser_power + (max_laser_power - min_laser_power) * (1 + amplitude_y * math.sin(2 * math.pi * frequency_y * y_position / line_length)) / 2
    # Ensure laser power is within [0, 1000] and round it to the nearest integer
    return max(0, min(int(round(raw_power)), 1000))

# Create lists to store X, Y, and Z coordinates
x_coords = []
y_coords = []
z_coords = []

# Laser off at the beginning
x_coords.append(0)
y_coords.append(0)
z_coords.append(0)

# Loop through the X-axis positions
for x_position in range(num_repetitions):
    # Calculate the Y offset with a sinusoidal pattern for the current X position
    y_offset = amplitude_x * math.sin(2 * math.pi * frequency_x * x_position / num_repetitions)
    
    for y_position in range(int(line_length)):
        laser_power = calculate_laser_power(y_position)
        # Store the coordinates with 2 decimal places, including the Y offset
        x_coords.append(round(x_position * 0.3, 2))  # X-axis
        y_coords.append(round(y_position + y_offset, 2))  # Y-axis with offset
        z_coords.append(laser_power)  # Z-axis

    # Laser power for the return path (from top to bottom)
    for y_position in range(int(line_length) - 1, -1, -1):
        laser_power = calculate_laser_power(y_position)
        # Store the coordinates with 2 decimal places, including the Y offset
        x_coords.append(round(x_position * 0.3, 2))  # X-axis
        y_coords.append(round(y_position + y_offset, 2))  # Y-axis with offset
        z_coords.append(laser_power)  # Z-axis

# Laser off at the end
x_coords.append(0)
y_coords.append(line_length)
z_coords.append(0)


# Create a 3D plot with a larger figure size
fig = plt.figure(figsize=(15, 8))  # You can adjust the width and height as needed
ax = fig.add_subplot(111, projection='3d')
# Plot the 3D surface
ax.scatter(x_coords, y_coords, z_coords, c=z_coords, cmap='viridis')

# Set labels for the axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z (Laser Power)')

# Show the plot
plt.show()

# Specify the file path where you want to save the G-code
gcode_file_path = "3D_SINUS7.gcode"

# Create a file to write the G-code
with open(gcode_file_path, "w") as gcode_file:
    # Laser on at the beginning
    gcode_file.write("M3\n")
    
    # Loop through the X-axis positions
    for x_position in range(num_repetitions):
        # Calculate the Y offset with a sinusoidal pattern for the current X position
        y_offset = amplitude_x * math.sin(2 * math.pi * frequency_x * x_position / num_repetitions)
        
        for y_position in range(int(line_length)):
            laser_power = calculate_laser_power(y_position)
            # Construct the G-code command with 2 decimal places for X and Y, and include the feed rate
            gcode_command = f"G1 X{x_position * 0.3:.2f} Y{y_position + y_offset:.2f} S{laser_power} F{feed_rate}"
            # Write the G-code command to the file
            gcode_file.write(gcode_command + "\n")

        # Laser power for the return path (from top to bottom)
        for y_position in range(int(line_length) - 1, -1, -1):
            laser_power = calculate_laser_power(y_position)
            # Construct the G-code command with 2 decimal places for X and Y, and include the feed rate
            gcode_command = f"G1 X{x_position * 0.3:.2f} Y{y_position + y_offset:.2f} S{laser_power} F{feed_rate}"
            # Write the G-code command to the file
            gcode_file.write(gcode_command + "\n")

    # Laser off at the end
    gcode_file.write("M5\n")

print("G-code generation complete. Saved to '3D_SINUS7.gcode'.")
