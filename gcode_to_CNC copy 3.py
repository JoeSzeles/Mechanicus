def reverse_layers(input_file, output_file):
    with open(input_file, 'r') as f:
        gcode_lines = f.readlines()

    layers = []
    current_layer = []

    in_layer = False

    for line in gcode_lines:
        if line.startswith(';LAYER:'):
            if current_layer:
                layers.append(current_layer.copy())
                current_layer = []
            in_layer = True
        elif line.startswith(';TIME_ELAPSED:'):
            in_layer = False

        if in_layer:
            current_layer.append(line)

    if current_layer:  # Append the last layer
        layers.append(current_layer.copy())

    layers.reverse()

    with open(output_file, 'w') as out_f:
        for layer in layers:
            out_f.writelines(layer)

def rename_layers(input_file, output_file):
    with open(input_file, 'r') as f:
        gcode_lines = f.readlines()

    layers = []
    current_layer = []
    current_layer_number = 0

    for line in gcode_lines:
        if line.startswith(';LAYER:'):
            if current_layer:
                layers.append(current_layer.copy())
                current_layer = []

            current_layer.append(f';LAYER:{current_layer_number}\n')
            current_layer_number += 1
        else:
            current_layer.append(line)

    with open(output_file, 'w') as out_f:
        for layer in layers:
            out_f.writelines(layer)



# Rest of your code
input_gcode_file = 'wood_test_dome.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed4.gcode'

# Reverse the layers
reverse_layers(input_gcode_file, output_gcode_file)

# Rename the layers starting from 0
rename_layers(output_gcode_file, output_gcode_file)



