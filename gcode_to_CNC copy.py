def reverse_gcode_layers(input_file, output_file):
    with open(input_file, 'r') as f:
        gcode_lines = f.readlines()

    header_block = []
    layer_blocks = []
    footer_block = []
    current_block = []
    layer_counter = 0
    current_z = None
    last_z = None

    in_header = True

    for line in gcode_lines:
        if in_header:
            header_block.append(line)
            if line.startswith(';LAYER:'):
                in_header = False

        if not in_header:
            current_block.append(line)
            if line.startswith(';TIME_ELAPSED:'):
                if current_z is not None:
                    layer_blocks.append((layer_counter, current_block, last_z))
                    current_block = []
                    layer_counter += 1
                current_z = None
            if line.startswith('G0 ') or line.startswith('G1 '):
                z_index = line.find('Z')
                if z_index != -1:
                    last_z = float(line[z_index + 1:].split()[0])
                    current_z = last_z
                # Add relative Z movement after G0 command
                relative_z_movement = 'G91\nG0 Z0.1\nG90\n'
                current_block.append(relative_z_movement)

    footer_block.extend(current_block)  # Store the remaining lines as footer

    reversed_gcode = []
    reversed_gcode.extend(header_block)

    for layer_num, block, z in reversed(layer_blocks):
        reversed_gcode.extend([line.replace(f';LAYER:{layer_num}', f';LAYER:{layer_counter - layer_num - 1}') if line.startswith(';LAYER:') else line for line in block[::-1]])
        reversed_gcode.append(f'G0 Z{z}')

    reversed_gcode.extend([f'G0 Z25', ''])  # Add final G0 Z command and an empty line

    with open(output_file, 'w') as f:
        f.writelines(reversed_gcode)

# Provide the input and output file paths
input_gcode_file = 'wood_test_dome.gcode'
output_gcode_file = 'wood_test_dome_layers_reversed4.gcode'

# Call the function to reverse the layers
reverse_gcode_layers(input_gcode_file, output_gcode_file)
