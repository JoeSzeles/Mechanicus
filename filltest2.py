import math
import xml.etree.ElementTree as ET
svg_file="filltest.svg"
def calculate_area(svg_file):
    
    tree = ET.parse(svg_file)
    root = tree.getroot()
    area = 0
    
    for child in root:
        if child.tag == "{http://www.w3.org/2000/svg}path":
            # Get the path data
            path_data = child.attrib["d"]
            
            # Divide the path into triangles
            points = path_data.split(" ")
            for i in range(2, len(points)):
                triangle_data = f"{points[0]} {points[i-1]} {points[i]}"
                area += calculate_triangle_area(triangle_data)
                print(area)
            
        elif child.tag == "{http://www.w3.org/2000/svg}rect":
            # Get the rectangle dimensions
            width = float(child.attrib["width"])
            height = float(child.attrib["height"])
            
            # Calculate the area
            area += width * height
    print(area)
    return area

def calculate_triangle_area(triangle_data):
    # Get the coordinates of the triangle vertices
    vertices = triangle_data.split(" ")
    x1, y1, x2, y2, x3, y3 = map(float, vertices)
    
    # Print the vertices to check if they are correct
    print(f"Vertices: ({x1}, {y1}), ({x2}, {y2}), ({x3}, {y3})")
    
    # Calculate the base and height of the triangle
    base = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    height = abs((x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1)) / base
    
    # Print the base and height to check if they are correct
    print(f"Base: {base}, Height: {height}")
    
    # Calculate the area of the triangle
    area = (base * height) / 2
    
    # Print the area to check if it is correct
    print(f"Area: {area}")
    
    return area
    
calculate_area(svg_file)
