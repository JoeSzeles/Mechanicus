import tkinter as tk
from tkinter import filedialog
from PIL import Image

def convert_and_print():
    # Load the normal map image
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x, bed_max_y
    bed_size_x = bed_max_x
    bed_size_y = bed_max_y
    feedrate = 8000

    # Laser parameters
    laser_min = 0   # Minimum laser power (S0)
    laser_max = 1000  # Maximum laser power (S1000)
    laser_speed = 1000  # Laser speed

    # Load the normal map image (assuming it's an RGB image)
    normal_map = Image.open('normal_map3.jpg').convert('RGB')

    # Get the image dimensions in pixels
    img_width, img_height = normal_map.size
    print('Image dimensions:', img_width, 'x', img_height)

    # Calculate the scaling factor
    scaling_factor_x = 1
    scaling_factor_y = 1

    # Use the larger scaling factor to fill the bed in either X or Y direction
    scaling_factor = max(scaling_factor_x, scaling_factor_y)

    # Calculate the scaled dimensions
    scaled_width = int(img_width * scaling_factor)
    scaled_height = int(img_height * scaling_factor)
    print('Image dimensions after scaling:', scaled_width, 'x', scaled_height)

    # Scale the normal map
    normal_map = normal_map.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    # Calculate the highest peak in the normal map
    max_peak = -float('inf')
    for y in range(normal_map.size[1]):
        for x in range(normal_map.size[0]):
            r, _, _ = normal_map.getpixel((x, y))
            max_peak = max(max_peak, r)

    # Set the initial laser power to minimum
    laser_power = laser_min

    # Convert the normal map to G-code with S values
    gcode_str = ''  # Initialize G-code string
    gcode_str += 'G21 ; Set units to millimeters\n'  # Set units to millimeters
    gcode_str += 'G90 ; Set absolute positioning\n'  # Set absolute positioning
    gcode_str += 'G28 ; Home all axes\n'  # Home all axes
    gcode_str += 'M3 ; Activate laser\n'  # Activate laser

    z_scale = 5  # Adjust this value to control the Z (height) scaling

    for y in range(normal_map.size[1]):
        # Determine the direction of travel for each row
        if y % 2 == 0:
            x_range = range(normal_map.size[0])
        else:
            x_range = reversed(range(normal_map.size[0]))

        for x in x_range:
            r, g, b = normal_map.getpixel((x, y))
            x_pos = x  # Scale the X-coordinate
            y_pos = bed_size_y - y  # Scale and invert the Y-coordinate
            z_pos = (((r / 255.0) * 2 - 1) * z_scale)  # Convert the red channel to height information (-1 to 1), scale it

            # Calculate laser power based on height
            laser_power = int(((z_pos + 1) / 2) * (laser_max - laser_min) + laser_min)

            gcode_str += 'G1 X{:.3f} Y{:.3f} S{} F{} ; Move to position with laser power\n'.format(x_pos, y_pos, laser_power, laser_speed)

    # Turn off the laser
    gcode_str += 'M5 ; Turn off laser\n'

    # Finish the G-code
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
    gcode_str += 'M84 ; Turn off motors\n'

    # Save the G-code to a file
    gcode_file = filedialog.asksaveasfilename(defaultextension='.gcode', filetypes=[('G-code files', '*.gcode')])
    with open(gcode_file, 'w') as f:
        f.write(gcode_str)

    print('G-code saved to:', gcode_file)

# Create a tkinter window
window = tk.Tk()
window.title("G-code Generator")

# Create and pack labels and entry fields for user input
cv = tk.Canvas(window, width=200, height=100)
cv.pack()

bed_max_x_label = tk.Label(window, text="Bed Max X Size:")
bed_max_x_label.pack()
bed_max_x_entry = tk.Entry(window)
bed_max_x_entry.pack()

bed_max_y_label = tk.Label(window, text="Bed Max Y Size:")
bed_max_y_label.pack()
bed_max_y_entry = tk.Entry(window)
bed_max_y_entry.pack()

# Create and pack a button for generating G-code
generate_button = tk.Button(window, text="Generate G-code", command=convert_and_print)
generate_button.pack()

# Start the tkinter main loop
window.mainloop()
