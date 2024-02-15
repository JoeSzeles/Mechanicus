import tkinter as tk
from tkinter import filedialog
from PIL import Image
import math

def convert_and_print():
    # Load the bump map image
    img_path = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.png')])
    bump_map = Image.open(img_path).convert('L')  # Convert to grayscale

    # Get the size of the imported image
    img_width, img_height = bump_map.size

    # Apply a scaling factor
    scaling_factor = 0.25  # You can adjust this scaling factor as needed

    # Calculate the new dimensions based on the scaling factor
    new_width = int(img_width * scaling_factor)
    new_height = int(img_height * scaling_factor)

    # Resize the image to the new dimensions
    bump_map = bump_map.resize((new_width, new_height), Image.ANTIALIAS)

    # Invert the grayscale image
    bump_map = Image.eval(bump_map, lambda x: 255 - x)

    # Laser parameters
    laser_min = 0   # Minimum laser power (S0)
    laser_max = 1000  # Maximum laser power (S1000)
    laser_speed = 1000  # Laser speed

    # Define the desired resolution in lines per millimeter
    lines_per_mm_machine = 4

    # Get the image dimensions in pixels
    img_width, img_height = bump_map.size

    # Initialize the G-code string
    gcode_str = ''
    gcode_str += 'G21 ; Set units to millimeters\n'
    gcode_str += 'G90 ; Set absolute positioning\n'
    gcode_str += 'G28 ; Home all axes\n'
    gcode_str += 'M3 ; Activate laser\n'

    for y in range(img_height):
        # Determine the direction of travel for each row
        if y % 2 == 0:
            x_range = range(img_width)
        else:
            x_range = reversed(range(img_width))

        for x in x_range:
            pixel_value = bump_map.getpixel((x, y))
            x_pos = x / lines_per_mm_machine  # Calculate X position in millimeters
            y_pos = (img_height - y) / lines_per_mm_machine  # Calculate Y position in millimeters

            # Calculate laser power based on pixel grayscale value
            laser_power = int(pixel_value * (laser_max - laser_min) / 255 + laser_min)

            gcode_str += 'G1 X{:.2f} Y{:.2f} S{} F{} ; Move to position with laser power\n'.format(x_pos, y_pos, laser_power, laser_speed)

    # Turn off the laser
    gcode_str += 'M5 ; Turn off laser\n'

    # Finish the G-code
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(400)#speed
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

# Create and pack a button for generating G-code
generate_button = tk.Button(window, text="Generate G-code", command=convert_and_print)
generate_button.pack()

# Start the tkinter main loop
window.mainloop()



