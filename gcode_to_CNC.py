def extract_reverse_rename_layers(input_file, output_file):
    with open(input_file, 'r') as f:
        gcode_lines = f.readlines()

    layers = []
    current_layer = []

    in_layer = False

    for line in gcode_lines:
        if line.startswith(';LAYER:'):
            if current_layer:
                layers.append(current_layer)
                current_layer = []
            in_layer = True
        elif line.startswith(';TIME_ELAPSED:') or line.startswith(';LAYER_HEIGHT:') or line.startswith(';MESH:'):
            in_layer = False

        if in_layer:
            current_layer.append(line)

    # Reverse the order of layers
    layers.reverse()

    # Save the reversed and renamed layers to the output file
    with open(output_file, 'w') as out_f:
        for i, layer in enumerate(layers):
            # Rename the layer
            new_layer_name = f';LAYER:{i}'
            renamed_layer = [line.replace(layer[0], new_layer_name, 1) if line.startswith(';LAYER:') else line for line in layer]
            out_f.writelines(renamed_layer)
            if i < len(layers) - 1:
                out_f.write('\n' * 3)

# Provide the input and output file paths
input_gcode_file = 'wood_test_dome.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed4.gcode'

# Call the function to extract and concatenate the layers
extract_reverse_rename_layers(input_gcode_file, output_gcode_file)
