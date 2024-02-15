def reverse_layers(input_file_path, output_file_path):
    with open(input_file_path, 'r') as f:
        lines = f.readlines()

    layer_count = None
    new_lines = []

    for line in lines:
        if line.startswith(';LAYER_COUNT:'):
            layer_count = int(line.split(':')[1])
            new_lines.append(line)
        elif line.startswith(';LAYER:'):
            layer_number = int(line.split(':')[1])
            reversed_layer_number = layer_count - layer_number - 1
            new_lines.append(line.replace(f';LAYER:{layer_number}', f';LAYER:{reversed_layer_number}'))
        else:
            new_lines.append(line)

    with open(output_file_path, 'w') as f:
        f.writelines(new_lines)

input_gcode_file = 'wood_test_dome.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed.gcode'

reverse_layers(input_gcode_file, output_gcode_file)

def extract_layer_blocks(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    layer_blocks = []
    current_block = []
    current_z = None

    for line in lines:
        if line.startswith(';LAYER:'):
            if current_block:
                if current_z is None and len(layer_blocks) > 0:
                    current_block[0] = current_block[0].replace(';LAYER:', ';LAYER:0')
                layer_blocks.append((current_z, current_block))
            current_block = []
            current_z = None
        elif line.startswith(';TIME_ELAPSED:'):
            if current_z is None and len(layer_blocks) > 0:
                current_z = layer_blocks[-1][0]
        elif line.startswith('G1 F300 Z'):
            current_z = float(line.split('Z')[1])
        current_block.append(line)

    if current_block:
        if current_z is None and len(layer_blocks) > 0:
            current_z = layer_blocks[-1][0]
        layer_blocks.append((current_z, current_block))

    return layer_blocks

def reverse_and_save_layer_blocks(layer_blocks, output_file_path):
    with open(output_file_path, 'w') as f:
        for z, layer_block in reversed(layer_blocks):
            f.writelines(layer_block)

input_gcode_file = 'wood_test_dome_layers_reversed.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed_separated2.gcode'

layer_blocks = extract_layer_blocks(input_gcode_file)
reverse_and_save_layer_blocks(layer_blocks, output_gcode_file)
















