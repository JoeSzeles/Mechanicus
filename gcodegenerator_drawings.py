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



def g_string(x, y, z=False, prefix="G1", p=3):
    if z is not False:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f} Z{z:.{p}f}"
    else:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f}"
def shapes_2_gcode(shapes):
    t1 = dt.now()
    with open("header.txt") as h:
        header = h.read()
    commands = [f"{header}", f'F{feed_rate}']
    commands.append(shape_preamble)
    for i, shape in enumerate(shapes):
        start = shape[0]
        end = shape[-1]
        if i < len(shapes) - 1:
            next_start = shapes[i+1][0]
            if end == next_start:
                # end of current shape is connected to start of next shape
                for j in shape:
                    commands.append(g_string(j[0], j[1], zDraw))
            else:
                # end of current shape is not connected to start of next shape
                commands.append(g_string(start[0], start[1], zTravel, "G0"))
                for j in shape:
                    commands.append(g_string(j[0], j[1], zDraw, f"F{draw_speed}"))
                commands.append(g_string(end[0], end[1], zLift, "G0"))
        else:
            # last shape
            commands.append(g_string(start[0], start[1], zTravel, "G0"))
            for j in shape:
                commands.append(g_string(j[0], j[1], zDraw, f"F{draw_speed}"))
            commands.append(g_string(end[0], end[1], zTravel, "G0"))
            
    commands += ["(home)", f"G0 {zTravel}", f"G0 X0 Y0"]

    timer(t1, "shapes_2_gcode   ")
    importlib.reload(config3)
    return commands

                 
              
def generate_gcode(svg_path, gcode_path):
    shapes = get_shapes(svg_path, scale_factor=scaleF, offset_x=0, offset_y=0)

    if optimise:
        pre_distance = get_total_distance(shapes)

        print("unoptimized distance: ", get_total_distance(shapes))

        new_order = optimise_path(shapes)

        post_distance = get_total_distance(new_order)

        print("optimized distance: ", post_distance)
        print("factor: ", post_distance / pre_distance)

        commands = shapes_2_gcode(new_order)
    else:
        commands = shapes_2_gcode(shapes)

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

