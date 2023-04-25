import xml.etree.ElementTree as ET
from simplepath import parsePath



def read_svg_file(svg_path):
    svg_tree = ET.parse(svg_path)
    root = svg_tree.getroot()
    coords = []
    coord_dict = {}
    for path in root.iter('{http://www.w3.org/2000/svg}path'):
        path_data = path.get('d')
        path_coords = parsePath(path_data)
        for segment in path_coords:
            command, params = segment
            if command == 'L':
                start_coord = tuple(params[:2])
                end_coord = tuple(params[2:])
                if start_coord not in coord_dict:
                    coord_dict[start_coord] = len(coords)
                    coords.append(start_coord)
                if end_coord not in coord_dict:
                    coord_dict[end_coord] = len(coords)
                    coords.append(end_coord)
    return coords, coord_dict



   





   
