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
from config3 import *
sys.setrecursionlimit(30000) # set the recursion limit to 10000
from datetime import datetime as dt
import importlib
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog

# Modify these variables as needed
Z_line_start = 5.0  # Initial Z position when a line starts
Z_line_center = 2.0  # Z position in the middle of a line
Z_line_end = 0.0  # Z position at the end of a line
Z_line_speed = 400.0  # Initial feed rate for Z movement

# Other existing variables
feed_rate = 100.0  # Default feed rate for XY movement
draw_speed = 100.0  # Default feed rate for drawing
zDraw = 5  # Z position for drawing
zTravel = 15.0  # Z position for non-drawing travel
zLift = 15.0  # Z position for lifting the tool
Z_gradient_length = 0.1  # Length of gradient transition along the line

num_points = 300  # Number of points for Z-axis interpolation

def calculate_z_values(start, end, num_points, z_start, z_end, gradient_length):
    # Calculate the length of the line segment
    length = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5

    # Calculate the gradient based on the specified gradient_length in mm
    gradient_length = min(gradient_length, length)  # Ensure gradient_length doesn't exceed the actual length
    gradient_ratio = gradient_length / length

    # Calculate a list of Z-axis values along the line segment
    z_values = []
    for i in range(num_points):
        t = i / (num_points - 1)  # Interpolation parameter [0, 1]
        z_interpolated = z_start + (z_end - z_start) * t

        # Apply the gradient transition within the specified gradient_length
        if t < gradient_ratio:
            z_interpolated = z_start + (Z_line_center - z_start) * (t / gradient_ratio)
        elif t > (1.0 - gradient_ratio):
            z_interpolated = Z_line_center + (z_end - Z_line_center) * ((t - (1.0 - gradient_ratio)) / gradient_ratio)

        z_values.append(z_interpolated)
    return z_values

def open_svg_file():
    file_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if file_path:
        entry_file_path.delete(0, tk.END)  # Clear the entry field
        entry_file_path.insert(0, file_path)  # Display the selected file path
        
        

def generate_gcode():
    svg_file_path = entry_file_path.get()
    z_line_start = float(entry_start.get())
    z_line_center = float(entry_center.get())
    z_line_end = float(entry_end.get())
    z_line_speed = float(entry_speed.get())

    # Define the path for the output G-code file
    gcode_file_path = "output.gcode"  # You can change this as needed

    # Call your existing get_shapes function
    shapes = get_shapes(svg_file_path, scale_factor=scaleF, offset_x=0, offset_y=0)

    # Pass the Z-line parameters and draw_speed when calling shapes_2_gcode
    commands = shapes_2_gcode(shapes, z_line_start, z_line_center, z_line_end, z_line_speed, draw_speed)

    with open(gcode_file_path, 'w+') as output:
        for command in commands:
            output.write(command + "\n")

    print(f"G-Code generated and saved to {gcode_file_path}")
    
    
def get_shapes(svg_path, auto_scale=False, scale_factor=scaleF, offset_x=x_offset, offset_y=y_offset, feed_rate=feed_rate):
    

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

    return shapes

def g_string(x, y, z=None, prefix="G1", p=3, feed_rate=None):
    if z is not None:
        if feed_rate is not None:
            feed_rate_str = f"F{feed_rate:.2f}"  # Use 2 decimal places for feed rate
            return f"{prefix} X{x:.3f} Y{y:.3f} Z{z:.3f} {feed_rate_str}"
        else:
            return f"{prefix} X{x:.3f} Y{y:.3f} Z{z:.3f}"
    else:
        if feed_rate is not None:
            feed_rate_str = f"F{feed_rate:.2f}"  # Use 2 decimal places for feed rate
            return f"{prefix} X{x:.3f} Y{y:.3f} {feed_rate_str}"
        else:
            return f"{prefix} X{x:.3f} Y{y:.3f}"


def shapes_2_gcode(shapes):
    t1 = dt.now()
    with open("header.txt") as h:
        header = h.read()
    commands = [f"{header}"]
    commands.append(shape_preamble)

    for i, shape in enumerate(shapes):
        start = shape[0]
        end = shape[-1]
        if i < len(shapes) - 1:
            next_start = shapes[i + 1][0]
            if end == next_start:
                # end of current shape is connected to the start of the next shape
                commands.append(g_string(start[0], start[1], zTravel, "G0", feed_rate=travel_speed))  # Move to the next shape's starting point
                for j in shape:
                    commands.append(g_string(j[0], j[1], zDraw, f'G1', draw_speed, feed_rate=draw_speed))
            else:
                # end of current shape is not connected to the start of the next shape
                commands.append(g_string(start[0], start[1], zTravel, "G0", feed_rate=travel_speed))  # Move to the new shape's starting point
                commands.append(g_string(start[0], start[1], zDraw, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to zDraw
                for j in shape[1:]:  # Start from the second point to avoid double lowering at the beginning
                    commands.append(g_string(j[0], j[1], zDraw, f'G1', draw_speed, feed_rate=draw_speed))
                commands.append(g_string(end[0], end[1], zTravel, "G0", feed_rate=travel_speed))  # Lift at the end of the shape
        else:
            # last shape
            commands.append(g_string(start[0], start[1], zTravel, "G0", feed_rate=travel_speed))  # Move to the last shape's starting point
            commands.append(g_string(start[0], start[1], zDraw, f'G1', draw_speed, feed_rate=draw_speed))  # Lower to zDraw
            for j in shape[1:]:  # Start from the second point to avoid double lowering at the beginning
                commands.append(g_string(j[0], j[1], zDraw, f'G1', draw_speed, feed_rate=draw_speed))
            commands.append(g_string(end[0], end[1], zTravel, "G0", feed_rate=travel_speed))  # Return to zTravel

    commands += ["(home)", f"G0 {zTravel}", f"G0 X0 Y0"]

    timer(t1, "shapes_2_gcode   ")
    return commands







def generate_gcode():
    svg_file_path = entry_file_path.get()
    z_line_start = float(entry_start.get())
    z_line_center = float(entry_center.get())
    z_line_end = float(entry_end.get())
    z_line_speed = float(entry_speed.get())
    gradient_length = float(entry_gradient_length.get())  # Get the gradient length from the input field

    # Define the path for the output G-code file
    gcode_file_path = "output.gcode"  # You can change this as needed

    # Call your existing generate_gcode function with the correct arguments
    shapes = get_shapes(svg_file_path, scale_factor=scaleF, offset_x=0, offset_y=0)
    print("Shapes:", shapes)
    # Pass the Z-line parameters and draw_speed when calling shapes_2_gcode
    commands = shapes_2_gcode(shapes, z_line_start, z_line_center, z_line_end, z_line_speed, draw_speed, gradient_length)

    with open(gcode_file_path, 'w+') as output:
        for command in commands:
            output.write(command + "\n")

    print(f"G-Code generated and saved to {gcode_file_path}")






# Create a Tkinter window
root = tk.Tk()
root.title("G-Code Generator")

# Create input fields for the variables
frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10)

ttk.Label(frame, text="Select SVG File:").grid(column=0, row=0, sticky=tk.W)
entry_file_path = ttk.Entry(frame)
entry_file_path.grid(column=1, row=0)
select_button = ttk.Button(frame, text="Browse", command=open_svg_file)
select_button.grid(column=2, row=0)

ttk.Label(frame, text="Z_line_start:").grid(column=0, row=1, sticky=tk.W)
entry_start = ttk.Entry(frame)
entry_start.grid(column=1, row=1)

ttk.Label(frame, text="Z_line_center:").grid(column=0, row=2, sticky=tk.W)
entry_center = ttk.Entry(frame)
entry_center.grid(column=1, row=2)

ttk.Label(frame, text="Z_line_end:").grid(column=0, row=3, sticky=tk.W)
entry_end = ttk.Entry(frame)
entry_end.grid(column=1, row=3)

ttk.Label(frame, text="Z_line_speed:").grid(column=0, row=4, sticky=tk.W)
entry_speed = ttk.Entry(frame)
entry_speed.grid(column=1, row=4)

ttk.Label(frame, text="Z_gradient_length:").grid(column=0, row=6, sticky=tk.W)
entry_gradient_length = ttk.Entry(frame)
entry_gradient_length.grid(column=1, row=6)
# Create a button to generate G-code
generate_button = ttk.Button(frame, text="Generate G-Code", command=generate_gcode)
generate_button.grid(column=0, row=7, columnspan=3)

root.mainloop()