import xml.etree.ElementTree as ET
import re

def draw_new_path(filepath):
    # open svg file
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # check if svg has a fill
    has_fill = False
    for child in root.iter():
        if 'fill' in child.attrib:
            has_fill = True
            break
    
    # start to draw new path inside the closed paths from svg
    new_paths = []
    closed_paths = []
    for child in root.iter():
        if child.tag == '{http://www.w3.org/2000/svg}path':
            path_data = child.attrib['d']
            if re.match('^M.*Z$', path_data):
                closed_paths.append(path_data)
    
    for path in closed_paths:
        # create new path with 3 pixel smaller size
        new_path_data = ''
        for command in re.findall('[A-Za-z][^A-Za-z]*', path):
            values = list(map(float, re.findall('[-+]?\d*\.\d+|[-+]?\d+', command)))
            if command[0] in ('M', 'L', 'T'):
                new_values = [v - 3 for v in values]
                new_command = command[0] + ' '.join(str(v) for v in new_values)
            elif command[0] in ('H', 'V'):
                new_values = [v - 3 for v in values]
                new_command = command[0] + ' '.join(str(v) for v in new_values)
            elif command[0] == 'C':
                new_values = [v - 3 for v in values[:-2]] + values[-2:]
                new_command = command[0] + ' '.join(str(v) for v in new_values)
            elif command[0] == 'S':
                new_values = [v - 3 for v in values[:-2]] + values[-2:]
                new_command = command[0] + ' '.join(str(v) for v in new_values)
            elif command[0] == 'Q':
                new_values = [v - 3 for v in values[:-2]] + values[-2:]
                new_command = command[0] + ' '.join(str(v) for v in new_values)
            elif command[0] == 'A':
                new_values = [v - 3 for v in values[:-2]] + values[-2:]
                new_command = command[0] + ' '.join(str(v) for v in new_values)
            else:
                new_command = command
            new_path_data += new_command
        
        # add new path to list
        new_paths.append(new_path_data)
    
    # continue until it becomes too small to draw
    while len(new_paths) > 0:
        if has_fill:
            fill = 'fill="none"'
        else:
            fill = ''
        new_path_data = new_paths.pop()
        new_path = ET.Element('path', d=new_path_data, stroke='black', stroke_width='1', fill='none', **{'vector-effect': 'non-scaling-stroke'})
        root.append(new_path)
        if max(map(abs, map(float, re.findall('[-+]?\d*\.\d+|[-+]?\d+', new_path_data)))) > 3:
            new_paths.extend(draw_new_path(new_path_data))
    # save new_paths to a new SVG file
    new_file_path = filepath.replace('.svg', '_new.svg')
    tree.write(new_file_path)
    return new_paths

draw_new_path('fill testsvg.svg')