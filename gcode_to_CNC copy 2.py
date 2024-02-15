def extract_layer_blocks(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    layer_blocks = []
    current_block = []
    is_in_layer_block = False

    for line in lines:
        if line.startswith(';LAYER:'):
            if is_in_layer_block:
                layer_blocks.append(current_block)
                current_block = []
            is_in_layer_block = True
        elif is_in_layer_block and line.strip() == "":
            layer_blocks.append(current_block)
            current_block = []
            is_in_layer_block = False

        current_block.append(line)

    if current_block:
        layer_blocks.append(current_block)

    return layer_blocks

def reverse_and_save_layer_blocks(layer_blocks, output_file_path):
    with open(output_file_path, 'w') as f:
        for layer_block in reversed(layer_blocks):
            f.writelines(layer_block)

input_gcode_file = 'wood_test_dome_layers_reversed.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed_separated2.gcode'

layer_blocks = extract_layer_blocks(input_gcode_file)
reverse_and_save_layer_blocks(layer_blocks, output_gcode_file)









