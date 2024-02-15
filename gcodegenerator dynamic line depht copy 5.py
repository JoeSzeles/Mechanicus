import math
import xml.etree.ElementTree as ET

# Function to parse SVG and extract shape coordinates
def parse_svg(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    shapes = []
    
    for line in root.findall(".//{http://www.w3.org/2000/svg}line"):
        x1 = float(line.get("x1"))
        y1 = float(line.get("y1"))
        x2 = float(line.get("x2"))
        y2 = float(line.get("y2"))
        shapes.append(("line", ((x1, y1), (x2, y2))))
    
    for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
        d = path.get("d")
        # You can use a suitable SVG path parser to extract coordinates from 'd'
        # For simplicity, this example assumes you're working with simple paths
        # with only 'M' (move to) and 'L' (line to) commands
        commands = d.split()
        points = []
        i = 0
        while i < len(commands):
            command = commands[i]
            if command == 'M':
                x = float(commands[i+1])
                y = float(commands[i+2])
                points.append((x, y))
                i += 3
            elif command == 'L':
                x = float(commands[i+1])
                y = float(commands[i+2])
                points.append((x, y))
                i += 3
            else:
                i += 1
        if len(points) > 1:
            shapes.append(("path", points))
    
    return shapes

# Input SVG file name
input_svg_file = "test9.svg"

# Parse SVG and extract shape coordinates
shapes = parse_svg(input_svg_file)

# Output file name
output_file = "test8.gcode"

# Generate G-code
gcode = []

# Move to initial position
gcode.append("G0 Z10")  # Move to initial Z position

# Process each line or path from the SVG
for shape_type, coordinates in shapes:
    if shape_type == "line":
        # Extract start and end points of the line
        A, B = coordinates
        # Placeholder: Generate G-code for the line segment
        # Modify the G-code generation logic for your specific requirements
        gcode.append(f"G1 X{A[0]} Y{A[1]} Z10 F100")  # Example G-code for a line

    elif shape_type == "path":
        # Extract points from the path
        points = coordinates
        # Placeholder: Generate G-code for the path
        # Modify the G-code generation logic for your specific requirements
        for x, y in points:
            gcode.append(f"G1 X{x} Y{y} Z10 F100")  # Example G-code for a path point

# Write the G-code to the output file
with open(output_file, 'w') as file:
    for line in gcode:
        file.write(line + "\n")

print(f"G-code saved to '{output_file}'")
