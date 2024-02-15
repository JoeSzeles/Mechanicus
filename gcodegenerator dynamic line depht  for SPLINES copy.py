import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
import re
from datetime import datetime as dt
from utils import *
import sys
import importlib
import config3
importlib.reload(config3)
from config3 import *
import tkinter as tk  # Import the tkinter library
from tkinter import filedialog


# Define a function to generate dynamic strokes between two points with given depth and width
def generate_dynamic_strokes(start, end, depth, width, num_points):
    dynamic_strokes = []
    
    # Calculate the step size for points
    step = (end[0] - start[0]) / num_points
    
    for i in range(num_points):
        x = start[0] + i * step
        # Calculate the position along the depth of the dynamic stroke
        z = start[1] - (depth / 2) + (depth * i / num_points)
        dynamic_strokes.append((x, z))
    
    # Add the last point to ensure the end point is reached
    dynamic_strokes.append(end)
    
    return dynamic_strokes

# Define your optimization algorithm here
def optimise_path(shapes):
    optimized_path = []
    for shape in shapes:
        optimized_shape = nearest_neighbor(shape)
        optimized_path.append(optimized_shape)
    return optimized_path

def nearest_neighbor(points):
    n = len(points)
    visited = [False] * n
    optimized_path = [0]  # Start with the first point as the initial path
    current_point = 0

    for _ in range(n - 1):
        min_distance = float('inf')
        nearest_point = None

        for i in range(n):
            if not visited[i]:
                distance = ((points[current_point][0] - points[i][0]) ** 2 + 
                            (points[current_point][1] - points[i][1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = i

        visited[nearest_point] = True
        optimized_path.append(nearest_point)
        current_point = nearest_point

    return [points[i] for i in optimized_path]

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

def g_string(x, y, z=None, prefix="G1", p=3, feed_rate=None):
    if z is not None:
        if feed_rate is not None:
            feed_rate_str = f"F{feed_rate:.3g}"  # Adjust the precision as needed
            return f"{prefix} X{x:.3f} Y{y:.3f} Z{z:.3f} {feed_rate_str}"
        else:
            return f"{prefix} X{x:.3f} Y{y:.3f} Z{z:.3f}"
    else:
        if feed_rate is not None:
            feed_rate_str = f"F{feed_rate:.3g}"  # Adjust the precision as needed
            return f"{prefix} X{x:.3f} Y{y:.3f} {feed_rate_str}"
        else:
            return f"{prefix} X{x:.3f} Y{y:.3f}"

def shapes_2_gcode(shapes, z_start, z_center, z_end, draw_speed, gradient_length_mm, min_points=20):
    t1 = dt.now()
    with open("header.txt") as h:
        header = h.read()
    commands = [f"{header}"]
    commands.append(shape_preamble)

    for i, shape in enumerate(shapes):
        start = shape[0]
        end = shape[-1]
        total_path_length = sum(((shape[j][0] - shape[j - 1][0]) ** 2 + (shape[j][1] - shape[j - 1][1]) ** 2) ** 0.5 for j in range(1, len(shape)))

        if i < len(shapes) - 1:
            next_start = shapes[i + 1][0]
            if end == next_start:
                # end of current shape is connected to the start of the next shape
                commands.append(g_string(start[0], start[1], z_start, "G0", feed_rate=travel_speed))  # Move to the next shape's starting point
                for j in shape:
                    # Calculate Z-axis position along the path
                    path_length = sum(((shape[k][0] - shape[k - 1][0]) ** 2 + (shape[k][1] - shape[k - 1][1]) ** 2) ** 0.5 for k in range(1, shape.index(j) + 1))
                    if path_length < gradient_length_mm:
                        z = z_start + (z_center - z_start) * (path_length / gradient_length_mm)
                    elif path_length < total_path_length - gradient_length_mm:
                        z = z_center
                    else:
                        remaining_length = total_path_length - path_length
                        z = z_center + (z_end - z_center) * ((gradient_length_mm - remaining_length) / gradient_length_mm)

                    commands.append(g_string(j[0], j[1], z, f'G1', draw_speed, feed_rate=draw_speed))
            else:
                # end of current shape is not connected to the start of the next shape
                commands.append(g_string(start[0], start[1], z_start, "G0", feed_rate=travel_speed))  # Move to the new shape's starting point
                commands.append(g_string(start[0], start[1], z_start, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to z_start

                if len(shape) <= min_points:
                    # Special case for straight lines with points less than or equal to min_points
                    path_length = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
                    for k in range(min_points):
                        x = start[0] + (k / (min_points - 1)) * (end[0] - start[0])
                        y = start[1] + (k / (min_points - 1)) * (end[1] - start[1])

                        # Calculate Z-axis position along the path
                        if path_length < gradient_length_mm:
                            z = z_start + (z_center - z_start) * (path_length / gradient_length_mm)
                        elif path_length < total_path_length - gradient_length_mm:
                            z = z_center
                        else:
                            remaining_length = total_path_length - path_length
                            z = z_center + (z_end - z_center) * ((gradient_length_mm - remaining_length) / gradient_length_mm)

                        commands.append(g_string(x, y, z, f'G1', draw_speed, feed_rate=draw_speed))
                else:
                    for j in shape[1:]:  # Start from the second point to avoid double lowering at the beginning
                        # Calculate Z-axis position along the path
                        path_length = sum(((shape[k][0] - shape[k - 1][0]) ** 2 + (shape[k][1] - shape[k - 1][1]) ** 2) ** 0.5 for k in range(1, shape.index(j) + 1))
                        if path_length < gradient_length_mm:
                            z = z_start + (z_center - z_start) * (path_length / gradient_length_mm)
                        elif path_length < total_path_length - gradient_length_mm:
                            z = z_center
                        else:
                            remaining_length = total_path_length - path_length
                            z = z_center + (z_end - z_center) * ((gradient_length_mm - remaining_length) / gradient_length_mm)

                        commands.append(g_string(j[0], j[1], z, f'G1', draw_speed, feed_rate=draw_speed))
                commands.append(g_string(end[0], end[1], z_start, "G0", feed_rate=travel_speed))  # Lift at the end of the shape
        else:
            # last shape
            commands.append(g_string(start[0], start[1], z_start, "G0", feed_rate=travel_speed))  # Move to the last shape's starting point
            commands.append(g_string(start[0], start[1], z_start, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to z_start

            if len(shape) <= min_points:
                # Special case for straight lines with points less than or equal to min_points
                path_length = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
                for k in range(min_points):
                    x = start[0] + (k / (min_points - 1)) * (end[0] - start[0])
                    y = start[1] + (k / (min_points - 1)) * (end[1] - start[1])

                    # Calculate Z-axis position along the path
                    if path_length < gradient_length_mm:
                        z = z_start + (z_center - z_start) * (path_length / gradient_length_mm)
                    elif path_length < total_path_length - gradient_length_mm:
                        z = z_center
                    else:
                        remaining_length = total_path_length - path_length
                        z = z_center + (z_end - z_center) * ((gradient_length_mm - remaining_length) / gradient_length_mm)

                    commands.append(g_string(x, y, z, f'G1', draw_speed, feed_rate=draw_speed))
            else:
                for j in shape[1:]:  # Start from the second point to avoid double lowering at the beginning
                    # Calculate Z-axis position along the path
                    path_length = sum(((shape[k][0] - shape[k - 1][0]) ** 2 + (shape[k][1] - shape[k - 1][1]) ** 2) ** 0.5 for k in range(1, shape.index(j) + 1))
                    if path_length < gradient_length_mm:
                        z = z_start + (z_center - z_start) * (path_length / gradient_length_mm)
                    elif path_length < total_path_length - gradient_length_mm:
                        z = z_center
                    else:
                        remaining_length = total_path_length - path_length
                        z = z_center + (z_end - z_center) * ((gradient_length_mm - remaining_length) / gradient_length_mm)

                    commands.append(g_string(j[0], j[1], z, f'G1', draw_speed, feed_rate=draw_speed))
            commands.append(g_string(end[0], end[1], z_start, "G0", feed_rate=travel_speed))  # Return to zTravel

    commands += ["(home)", f"G0 {z_start}", f"G0 X0 Y0"]

    timer(t1, "shapes_2_gcode   ")
    return commands


def get_total_distance(shapes):
    total_distance = 0
    for shape in shapes:
        for i in range(1, len(shape)):
            x1, y1 = shape[i - 1]
            x2, y2 = shape[i]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            total_distance += distance
    return total_distance

def generate_gcode(svg_path, gcode_path, z_start, z_center, z_end, gradient_length_mm):
    
    shapes = get_shapes(svg_path, scale_factor=scaleF, offset_x=0, offset_y=0)

    if optimise:
        pre_distance = get_total_distance(shapes)

        print("unoptimized distance: ", get_total_distance(shapes))

        new_order = optimise_path(shapes)

        post_distance = get_total_distance(new_order)

        print("optimized distance: ", post_distance)
        print("factor: ", post_distance / pre_distance)

        commands = shapes_2_gcode(new_order, z_start, z_center, z_end, draw_speed, gradient_length_mm)
    else:
        commands = shapes_2_gcode(shapes, z_start, z_center, z_end, draw_speed, gradient_length_mm)

    with open(gcode_path, 'w+') as output:
        for command in commands:
            output.write(command + "\n")

    print(f"G-Code generated and saved to {gcode_path}")

def write_file(output, commands):
    t1 = dt.now()
    with open(output, 'w+') as output_file:
        for i in commands:
            output_file.write(i + "\n")
    timer(t1, "writing file     ")



# Define a function to open a file dialog for selecting an SVG file
def browse_svg():
    file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if file_path:
        input_svg_entry.delete(0, tk.END)
        input_svg_entry.insert(0, file_path)

# Define a function to open a file dialog for selecting a G-code file
def browse_gcode():
    file_path = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("G-code files", "*.gcode")])
    if file_path:
        output_gcode_entry.delete(0, tk.END)
        output_gcode_entry.insert(0, file_path)

# Define a function to generate G-code when the "Generate" button is clicked
def generate_gcode_from_gui():
    svg_file_path = input_svg_entry.get()
    gcode_file_path = output_gcode_entry.get()
    z_start = float(z_start_entry.get())
    z_center = float(z_center_entry.get())
    z_end = float(z_end_entry.get())
    gradient_length_mm = float(gradient_length_entry.get())

    generate_gcode(svg_file_path, gcode_file_path, z_start, z_center, z_end, gradient_length_mm)

# Create a Tkinter window
root = tk.Tk()
root.title("SVG to G-code Converter")

# Create labels and entry fields for input and output paths and settings
input_svg_label = tk.Label(root, text="Input SVG File:")
input_svg_label.pack()
input_svg_entry = tk.Entry(root)
input_svg_entry.pack()
browse_svg_button = tk.Button(root, text="Browse", command=browse_svg)
browse_svg_button.pack()

output_gcode_label = tk.Label(root, text="Output G-code File:")
output_gcode_label.pack()
output_gcode_entry = tk.Entry(root)
output_gcode_entry.pack()
browse_gcode_button = tk.Button(root, text="Browse", command=browse_gcode)
browse_gcode_button.pack()

z_start_label = tk.Label(root, text="Z Start (mm):")
z_start_label.pack()
z_start_entry = tk.Entry(root)
z_start_entry.pack()
z_start_entry.insert(0, "19")

z_center_label = tk.Label(root, text="Z Center (mm):")
z_center_label.pack()
z_center_entry = tk.Entry(root)
z_center_entry.pack()
z_center_entry.insert(0, "10")

z_end_label = tk.Label(root, text="Z End (mm):")
z_end_label.pack()
z_end_entry = tk.Entry(root)
z_end_entry.pack()
z_end_entry.insert(0, "19")

gradient_length_label = tk.Label(root, text="Gradient Length (mm):")
gradient_length_label.pack()
gradient_length_entry = tk.Entry(root)
gradient_length_entry.pack()
gradient_length_entry.insert(0, "20")

# Create a "Generate" button
generate_button = tk.Button(root, text="Generate G-code", command=generate_gcode_from_gui)
generate_button.pack()

root.mainloop()