def convert_and_print():
    ##convert image to gcode
    # Load the image
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    bed_size_x = 300
    bed_size_y = 300
    feedrate=8000
    print_height=5
    line_start = None  # Coordinates of the start of the current line
    line_end = None  # Coordinates of the end of the current line

    # Load the image
    img = Image.open('temp2.png').convert('L')

    # Get the image dimensions in pixels
    img_width, img_height = img.size
    print('Image dimensions:', img_width, 'x', img_height)
    # Calculate the scaling factor
    # Calculate the scaling factors
    scaling_factor_x = bed_size_x / img_width
    scaling_factor_y = bed_size_y / img_height

    # Use the larger scaling factor to fill the bed in either X or Y direction
    scaling_factor = max(scaling_factor_x, scaling_factor_y)
    # Calculate the scaled dimensions
    scaled_width = int(img_width * scaling_factor)
    scaled_height = int(img_height * scaling_factor)
    print('Image dimensions:', scaled_width, 'x', scaled_height)

    # Scale the image
    img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)


    # Create a G-code string
    gcode_str = ''
    gcode_str += 'G21 ; Set units to millimeters\n'
    gcode_str += 'G90 ; Set absolute positioning\n'
    gcode_str += 'G28 ; Home all axes\n'
    gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
    

    # Convert the image to G-code
    gcode_str = ''  # Initialize G-code string
    gcode_str += 'G21 ; Set units to millimeters\n'  # Set units to millimeters
    gcode_str += 'G90 ; Set absolute positioning\n'  # Set absolute positioning
    gcode_str += 'G28 ; Home all axes\n'  # Home all axes
    gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)  # Move up 5mm
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)  # Move to bottom left corner
    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)  # Move down to print

    # Initialize starting position and line state
    x_pos = 0
    y_pos = 0
    line_state = False


    is_printing = False  # A flag to keep track of whether the print head is currently down
    last_pos = None  # The last position where the print head was down
    for y in range(img.size[1]):
        x_pos = bed_size_x   # Scale the X-coordinate
        y_pos = bed_size_y - y   # Invert and scale the Y-coordinate
        gcode_str += 'G1 Y{:.3f} F{} ; Move to next row\n'.format(y_pos, feedrate)
        for x in range(img.size[0]):
            pixel_value = img.getpixel((x, y))
            if pixel_value > 128:  # Check if the pixel value is greater than 128 (white)
                if is_printing:
                    # If the print head is currently down, lift it up
                    gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                    gcode_str += 'G1 Z8 F{} ; Lift print head\n'.format(feedrate)
                    is_printing = False
            else:  # Pixel is black
                if not is_printing:
                    # If the print head is currently up, move to the start position of the new line
                    x_pos = x  # Scale the X-coordinate
                    gcode_str += 'G1 X{:.3f} F{} ; Move to print\n'.format(x_pos, feedrate)
                    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                    last_pos = (x_pos, y_pos)
                    is_printing = True
                else:
                    # If the print head is already down, continue the line
                    x_pos = x  # Scale the X-coordinate
                    if (x_pos - last_pos[0]) ** 2 + (y_pos - last_pos[1]) ** 2 >= 0.5 ** 2:
                        # If the next pixel is more than 0.5mm away from the current position, lift the print head and move to the new position
                        gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                        gcode_str += 'G1 X{:.3f} Y{:.3f} F{} ; Move to new line\n'.format(x_pos, y_pos, feedrate)
                        gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                        last_pos = (x_pos, y_pos)
                    else:
                        # If the next pixel is less than 0.5mm away from the current position, just continue the line
                        gcode_str += 'G1 X{:.3f} F{} ; Continue line\n'.format(x_pos, feedrate)
                        last_pos = (x_pos, y_pos)
    # If the last pixel of the image is not white, lift the print head
    if is_printing:
        gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
        gcode_str += 'G1 Z8 F{} ; Lift print head\n'.format(feedrate)

    # Finish the G-code
    gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
    gcode_str += 'M84 ; Turn off motors\n'

    # Save the G-code to    
    # Save the G-code to a file
    output_file = 'gcode_output3'  + '.gcode'
    with open(output_file, 'w') as f:
        f.write(gcode_str)
    
    print('G-code saved to:', output_file)