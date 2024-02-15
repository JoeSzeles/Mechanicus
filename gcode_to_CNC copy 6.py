def reverse_layers(input_file_path, output_file_path):
    with open(input_file_path, 'r') as f:
        lines = f.readlines()

    layer_count = None
    layer_lines = []
    in_layer_block = False

    for line in lines:
        if line.startswith(';LAYER_COUNT:'):
            layer_count = int(line.split(':')[1])
            layer_lines.append(line)
        elif line.startswith(';LAYER:'):
            in_layer_block = True
            layer_lines.append(line)
        elif line.startswith(';TIME_ELAPSED:'):
            in_layer_block = False
            layer_lines.append(line)
        elif in_layer_block:
            layer_lines.append(line)

    with open(output_file_path, 'w') as f:
        new_layer_number = layer_count - 1
        for line in layer_lines:
            if line.startswith(';LAYER:'):
                line = f';LAYER:{new_layer_number}\n'
                new_layer_number -= 1
            f.write(line)

input_gcode_file = 'wood_test_dome.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed_separated.gcode'

reverse_layers(input_gcode_file, output_gcode_file)
def extract_layer_blocks(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    layer_blocks = []
    current_block = []

    for line in lines:
        if line.startswith(';LAYER:'):
            if current_block:
                layer_blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)

    if current_block:
        layer_blocks.append(current_block)

    return layer_blocks

def reverse_and_save_layer_blocks(layer_blocks, output_file_path):
    with open(output_file_path, 'w') as f:
        for layer_block in reversed(layer_blocks):
            for line in layer_block:
                if not line.startswith(';LAYER:') and not line.startswith(';TIME_ELAPSED:'):
                    f.write(line)

input_gcode_file = 'wood_test_dome.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed_separated4.gcode'

with open(input_gcode_file, 'r') as f:
    lines = f.readlines()

layer_blocks = []
current_block = []

for line in lines:
    if line.startswith(';LAYER:'):
        if current_block:
            layer_blocks.append(current_block)
        current_block = [line]
    else:
        current_block.append(line)

if current_block:
    layer_blocks.append(current_block)

reverse_and_save_layer_blocks(layer_blocks, output_gcode_file)


















