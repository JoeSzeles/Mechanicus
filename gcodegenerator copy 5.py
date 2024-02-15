# Define the parameters
start_point = (0, 0, 19)  # (X, Y, Z) coordinates of point A
line_length = 50  # Length of the line from A to B
end_point = (start_point[0] + line_length, start_point[1], start_point[2])  # Point B
mid_point = (start_point[0] + line_length / 2, start_point[1], 15)  # Point C

# Define the G-code header
gcode = [
    "G21",  # Metric units
    "G90",  # Absolute positioning
    "G92 X0 Y0 Z0",  # Set current position to (0, 0, 0)
]

# Move to the starting position (point A)
gcode.append(f"G0 X{start_point[0]} Y{start_point[1]} Z{start_point[2]}")

# Move to point C
gcode.append(f"G1 X{mid_point[0]} Y{mid_point[1]} Z{mid_point[2]}")

# Move to point B
gcode.append(f"G1 X{end_point[0]} Y{end_point[1]} Z{end_point[2]}")

# Define the G-code footer
gcode.append("G0 Z20")  # Move the tool away from the workpiece
gcode.append("M2")  # End of program

# Save the G-code to a file
with open("simple_v_cut.gcode", "w") as file:
    for line in gcode:
        file.write(line + "\n")

print("G-code generation completed. Saved as 'simple_v_cut.gcode'")
