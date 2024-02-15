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


import xml.etree.ElementTree as ET
import re
import sys
import importlib

import xml.etree.ElementTree as ET
import re
import sys
import importlib

def get_shapes(svg_path, auto_scale=False, scale_factor=1.0, offset_x=0.0, offset_y=0.0):
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
        
        if tag_suffix == 'line':  # Check if the shape is a line
            shape_properties = {}
            shape_properties['type'] = tag_suffix
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
                
                if len(coords) == 2:  # Check if it's a line (two points)
                    shape_properties['coordinates'] = coords
                    shapes.append(shape_properties)
    
    importlib.reload(config3)
    return shapes

# Example usage:
lines = get_shapes("test9.svg")
for idx, line in enumerate(lines, 1):
    print(f"Line {idx}:")
    print(f"Type: {line['type']}")
    print(f"Coordinates: {line['coordinates']}")
    print()
