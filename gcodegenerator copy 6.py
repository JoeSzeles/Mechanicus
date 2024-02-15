import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re
from datetime import datetime as dt
from optimise import optimise_path, get_total_distance
from utils import *
import sys
import importlib
import config3
importlib.reload(config3)
from config3 import *
sys.setrecursionlimit(30000) # set the recursion limit to 10000
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_toolpath(commands, z_draw_value, material_height_value):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x_vals = []
    y_vals = []
    z_vals = []

    for command in commands:
        parts = command.split()
        if parts[0] == 'G1':
            x = next((float(s[1:]) for s in parts if s.startswith('X')), None)
            y = next((float(s[1:]) for s in parts if s.startswith('Y')), None)
            z = next((float(s[1:]) for s in parts if s.startswith('Z')), None)
            if x is not None and y is not None and z is not None:
                x_vals.append(x)
                y_vals.append(y)
                z_vals.append(z)

    ax.plot(x_vals, y_vals, z_vals)

    # Add labels and lines for points A, B, and C
    ax.text(x_vals[0], y_vals[0], material_height_value, 'A', fontsize=12, color='red')
    ax.text(x_vals[-1], y_vals[-1], material_height_value, 'B', fontsize=12, color='red')
    
    # Calculate the coordinates of point C (the middle point)
    x_c = (x_vals[0] + x_vals[-1]) / 2
    y_c = (y_vals[0] + y_vals[-1]) / 2
    z_c = z_draw_value

    # Add label and line for point C
    ax.text(x_c, y_c, z_c, 'C', fontsize=12, color='red')
    ax.plot([x_vals[0], x_c, x_vals[-1], x_vals[0]], [y_vals[0], y_c, y_vals[-1], y_vals[0]], [material_height_value, z_c, material_height_value, material_height_value], color='blue')

    plt.show()
    # Call this function after generating the G-code
    return x_vals[0], y_vals[0], material_height_value, x_c, y_c, z_c, x_vals[-1], y_vals[-1], material_height_value
    




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
                    x += x_offset
                    y += y_offset
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



def g_string(x, y, z=False, prefix="G1", p=3, feed_rate=None):
    if z is not False:
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



def shapes_2_gcode(shapes, z_draw_value, material_height_value):
    t1 = dt.now()
    with open("header.txt") as h:
        header = h.read()
    commands = [f"{header}"]
    commands.append(shape_preamble)

    for i, shape in enumerate(shapes):
        start = shape[0]
        end = shape[-1]
        
        # Calculate the coordinates of point C (the middle point)
        x_c = (start[0] + end[0]) / 2
        y_c = (start[1] + end[1]) / 2
        
        if i < len(shapes) - 1:
            next_start = shapes[i + 1][0]
            if end == next_start:
                # end of current shape is connected to start of next shape
                commands.append(g_string(start[0], start[1], material_height_value, "G0", feed_rate=travel_speed))  # Move to point A
                commands.append(g_string(x_c, y_c, z_draw_value, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to Z_draw (point C)
                commands.append(g_string(end[0], end[1], material_height_value, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to material height (point B)
            else:
                # end of current shape is not connected to start of next shape
                commands.append(g_string(start[0], start[1], material_height_value, "G0", feed_rate=travel_speed))  # Move to point A
                commands.append(g_string(x_c, y_c, z_draw_value, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to Z_draw (point C)
                commands.append(g_string(end[0], end[1], material_height_value, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to material height (point B)
        else:
            # last shape
            commands.append(g_string(start[0], start[1], material_height_value, "G0", feed_rate=travel_speed))  # Move to point A
            commands.append(g_string(x_c, y_c, z_draw_value, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to Z_draw (point C)
            commands.append(g_string(end[0], end[1], material_height_value, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to material height (point B)

    commands += ["(home)", f"G0 {material_height_value}", f"G0 X0 Y0"]

    timer(t1, "shapes_2_gcode   ")
    importlib.reload(config3)
    return commands





            
              
def generate_gcode(svg_path, gcode_path, z_draw_value, material_height_value):
    shapes = get_shapes(svg_path, scale_factor=scaleF, offset_x=0, offset_y=0)

    if optimise:
        pre_distance = get_total_distance(shapes)

        print("unoptimized distance: ", get_total_distance(shapes))

        new_order = optimise_path(shapes)

        post_distance = get_total_distance(new_order)

        print("optimized distance: ", post_distance)
        print("factor: ", post_distance / pre_distance)

        commands = shapes_2_gcode(new_order, z_draw_value, material_height_value)
    else:
        commands = shapes_2_gcode(shapes, z_draw_value, material_height_value)

    with open(gcode_path, 'w+') as output:
        for command in commands:
            output.write(command + "\n")

    print(f"G-Code generated and saved to {gcode_path}")

# Rest of your code...

    


    



def write_file(output, commands):
    
    t1 = dt.now()
    with open(output, 'w+') as output_file:
        for i in commands:
            output_file.write(i + "\n")
    timer(t1, "writing file     ")
import tkinter as tk
from tkinter import filedialog

# Function to handle the "Calculate" button click
def calculate_gcode():
    input_svg_path = input_svg_path_entry.get()
    output_gcode_path = output_gcode_path_entry.get()
    
    # Get the values of z_draw and material_height
    z_draw_value = z_draw.get()
    material_height_value = material_height.get()
    
    # You can add validation or error handling here before generating G-code
    
    # Call your generate_gcode function with input and output paths, z_draw, and material_height
    generate_gcode(input_svg_path, output_gcode_path, z_draw_value, material_height_value)   
     
    # Update the status label
    status_label.config(text="G-Code generated and saved.")

# Create the main Tkinter window
window = tk.Tk()
window.title("SVG to G-Code Converter")

# Create DoubleVar variables for z_draw and material height (M)
z_draw = tk.DoubleVar(value=15.0)  # Default value of 15.0 for point C (z_draw)
material_height = tk.DoubleVar(value=19.0)  # Default material height for points A and B (M)

# Label and entry for input SVG path
input_svg_label = tk.Label(window, text="Input SVG File:")
input_svg_label.pack()
input_svg_path_entry = tk.Entry(window)
input_svg_path_entry.pack()

# Button to browse for input SVG file
def browse_input_file():
    input_svg_path = filedialog.askopenfilename(filetypes=[("SVG Files", "*.svg")])
    input_svg_path_entry.delete(0, tk.END)  # Clear any previous text
    input_svg_path_entry.insert(0, input_svg_path)

browse_input_button = tk.Button(window, text="Browse", command=browse_input_file)
browse_input_button.pack()

# Label and entry for output G-code path
output_gcode_label = tk.Label(window, text="Output G-Code File:")
output_gcode_label.pack()
output_gcode_path_entry = tk.Entry(window)
output_gcode_path_entry.pack()

# Button to browse for output G-code file
def browse_output_file():
    output_gcode_path = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("G-Code Files", "*.gcode")])
    output_gcode_path_entry.delete(0, tk.END)  # Clear any previous text
    output_gcode_path_entry.insert(0, output_gcode_path)

browse_output_button = tk.Button(window, text="Browse", command=browse_output_file)
browse_output_button.pack()

# Entry and label for z_draw (point C)
z_draw_label = tk.Label(window, text="Z_Draw (Point C):")
z_draw_label.pack()
z_draw_entry = tk.Entry(window, textvariable=z_draw)
z_draw_entry.pack()

# Entry and label for material height (M)
material_height_label = tk.Label(window, text="Material Height (M) for Points A and B:")
material_height_label.pack()
material_height_entry = tk.Entry(window, textvariable=material_height)
material_height_entry.pack()

# Calculate button
calculate_button = tk.Button(window, text="Calculate G-Code", command=calculate_gcode)
calculate_button.pack()

# Status label to display messages
status_label = tk.Label(window, text="")
status_label.pack()

# Start the Tkinter main loop
window.mainloop()
