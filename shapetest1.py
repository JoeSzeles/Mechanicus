import xml.etree.ElementTree as ET
import numpy as np



# Load the SVG file
tree = ET.parse('shapes_test.svg')
root = tree.getroot()

# Print the root element to check the namespace
print(root)

# Find the path element for the shape
path = root.find(".//{http://www.w3.org/2000/svg}path")

# Print the path element to check if it was found
print(path)

if path is not None:
    # Extract the 'd' attribute of the path element
    d = path.attrib['d']
    # Rest of the code...
else:
    print("Path element not found")

# Extract the 'd' attribute of the path element
d = path.attrib['d']

# Parse the path commands to get a list of coordinates
coords = []
last_point = None

for cmd in d.split():
    if cmd.isalpha():
        # Move-to command: start a new subpath
        if cmd == 'M':
            x, y = map(float, d.split()[1:3])
            coords.append((x, y))
            last_point = (x, y)
        # Line-to command: add a straight line segment to the current subpath
        elif cmd == 'L':
            x, y = map(float, d.split()[1:3])
            coords.append((x, y))
            last_point = (x, y)
        # Vertical line-to command: add a straight vertical line segment to the current subpath
        elif cmd == 'V':
            y = float(d.split()[1])
            coords.append((last_point[0], y))
            last_point = (last_point[0], y)
        # Horizontal line-to command: add a straight horizontal line segment to the current subpath
        elif cmd == 'H':
            x = float(d.split()[1])
            coords.append((x, last_point[1]))
            last_point = (x, last_point[1])
        # Close path command: close the current subpath by connecting the last point to the first point
        elif cmd == 'Z':
            coords.append(coords[0])
    else:
        # Curve command: ignore for now
        pass

# Convert the list of coordinates to a numpy array
boundary = np.array(coords)

# Compute the bounding box of the boundary points
xmin, ymin = np.min(boundary, axis=0)
xmax, ymax = np.max(boundary, axis=0)

# Draw line patterns inside the shape
dx, dy = 10, 10  # distance between lines
nx, ny = int((xmax - xmin) / dx), int((ymax - ymin) / dy)  # number of lines in x and y directions

# Create a new SVG element for the line pattern
lines = ET.Element('path', {'fill': 'none', 'stroke': 'black', 'stroke-width': '1'})

# Add the line segments to the path element
for i in range(nx):
    x = xmin + i * dx
    lines.set('d', f'M {x} {ymin} L {x} {ymax}')
    root.append(lines)

for j in range(ny):
    y = ymin + j * dy
    lines.set('d', f'M {xmin} {y} L {xmax} {y}')
    root.append(lines)

# Save the modified SVG file
tree.write('modified.svg')