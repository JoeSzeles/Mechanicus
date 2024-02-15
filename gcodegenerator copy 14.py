import numpy as np
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re
import sys
import importlib
import config3
importlib.reload(config3)
from config3 import *

def get_shapes(svg_path, auto_scale=False, scale_factor=scaleF, offset_x=x_offset, offset_y=y_offset):
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    shapes = []
    tree = ET.parse(svg_path)
    root = tree.getroot()
    pointRatio = 0.352778
    width = root.get('width')
    height = root.get('height')
    if width is None or height is None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()
    if width is None or height is None:
        print("Unable to get width and height for the svg")
        sys.exit(1)
    width = float(re.findall(r"[-+]?\d*\.\d+|\d+", width)[0])
    height = float(re.findall(r"[-+]?\d*\.\d+|\d+", height)[0])
    if units == "points":
        width *= pointRatio
        height *= pointRatio
    if auto_scale:
        print("\nauto scaling")
        bb_size = max(width, height)
        bed_size = max(bed_max_x, bed_max_y)
        scale_factor = bed_size / bb_size
        print("width / height        ", width, height)
        print("scale factor          ", scale_factor, "\n")
    else:
        scaleF = 1
    for elem in root.iter():
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue
        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()
            coords = []
            if d:
                p = point_generator(d, m, smoothness)
                first = True
                for x, y in p:
                    if units == "points":
                        x *= pointRatio
                        y *= pointRatio
                    y = -y + height
                    x *= scale_factor
                    y *= scale_factor
                    x += offset_x
                    y += offset_y
                    if first:
                        coords.append((x, y))
                    else:
                        if not (x, y) == coords[-1]:
                            coords.append((x, y))
                    if first:
                        first = False
                if len(coords) >= 2:  # check if shape has at least 3 points
                    shapes.append(coords)
    importlib.reload(config3)
    return shapes

def interpolate_parabolic(point_a, point_b, point_c, num_points):
    x_a, y_a = point_a
    x_c, y_c = point_c
    x_b, y_b = point_b

    # Calculate the coefficients of the parabolic equation z = ax^2 + bx + c
    a = ((y_a - y_b) / ((x_a - x_b) * (x_a - x_c)) - (y_a - y_c) / ((x_a - x_b) * (x_a - x_c))) / (x_c - x_b)
    b = ((y_a - y_b) / (x_a - x_b)) - a * (x_a + x_b)
    c = y_a - a * x_a ** 2 - b * x_a

    # Interpolate points along the parabolic path in the X-Z plane
    x_values = np.linspace(x_a, x_b, num_points)
    z_values = [a * x ** 2 + b * x + c for x in x_values]

    return x_values, z_values

def generate_gcode_for_parabolic_path(parabolic_points_x, parabolic_points_z, gcode_file_path, feed_rate, z_draw_value):
    # Open the G-code file for writing
    with open(gcode_file_path, 'w') as gcode_file:
        # Move to the initial point
        gcode_file.write(f"G0 X{parabolic_points_x[0]:.3f} Z{z_draw_value:.3f} F{feed_rate:.2f}\n")

        # Iterate through the parabolic points and write G-code commands
        for x, z in zip(parabolic_points_x, parabolic_points_z):
            gcode_file.write(f"G1 X{x:.3f} Z{z:.3f} F{feed_rate:.2f}\n")

        # Lift the tool at the end of the path
        gcode_file.write(f"G1 Z{z_draw_value:.3f} F{feed_rate:.2f}\n")

# Function to extract points A, B, and C from the first line segment in the SVG file
def extract_points_from_svg(svg_file_path):
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(svg_file_path)
        root = tree.getroot()
        # Assuming that the SVG contains <line> elements for the lines
        lines = root.findall(".//{http://www.w3.org/2000/svg}line")
        
        if len(lines) > 0:
            # Extract the coordinates of the first line segment
            line = lines[0]
            x1 = float(line.get("x1"))
            y1 = float(line.get("y1"))
            x2 = float(line.get("x2"))
            y2 = float(line.get("y2"))
            
            # Points A and B are the start and end of the line, and point C is the midpoint
            point_a = (x1, y1)
            point_b = (x2, y2)
            point_c = ((x1 + x2) / 2, (y1 + y2) / 2)
            
            return point_a, point_b, point_c
        else:
            print("No line segments found in the SVG.")
            return None
    except Exception as e:
        print(f"Error extracting points from SVG: {e}")
        return None

# Example usage:
svg_file_path = "test9.svg"  # Replace with the path to your SVG file
output_gcode_path = "parabolic_path2.gcode"  # Specify the desired G-code file path
feed_rate = 100  # Adjust the feed rate as needed
z_draw_value = 5.0  # Set the Z draw value as needed
num_points = 50  # Adjust the number of points as needed

# Extract points A, B, and C from the SVG
points = extract_points_from_svg(svg_file_path)

if points:
    point_a, point_b, point_c = points

    # Interpolate the parabolic path
    parabolic_points_x, parabolic_points_z = interpolate_parabolic(point_a, point_b, point_c, num_points)

    # Generate and save G-code for the parabolic path
    generate_gcode_for_parabolic_path(parabolic_points_x, parabolic_points_z, output_gcode_path, feed_rate, z_draw_value)

    print(f"G-Code generated and saved to {output_gcode_path}")
