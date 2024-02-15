import tkinter as tk
from tkinter import filedialog
from PIL import Image
import math

def convert_and_print():
    # Load the normal map image
    img_path = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.png')])
    normal_map = Image.open(img_path).convert('RGB')

    # Laser parameters
    laser_min = 0   # Minimum laser power (S0)
    laser_max = 1000  # Maximum laser power (S1000)
    laser_speed = 1000  # Laser speed

    # Define the desired resolution in lines per millimeter
    lines_per_mm_image = 2
    lines_per_mm_machine = 8

    # Get the image dimensions in pixels
    img_width, img_height = normal_map.size

    # Create a new image with lines
    line_image = Image.new('RGB', normal_map.size)
    for y in range(normal_map.size[1]):
        for x in range(normal_map.size[0]):
            r, g, _ = normal_map.getpixel((x, y))
            line_color = (r, g, 0)  # Use the red and green channels for lines

            line_image.putpixel((x, y), line_color)

    # Initialize the G-code string
    gcode_str = ''
    gcode_str += 'G21 ; Set units to millimeters\n'
    gcode_str += 'G90 ; Set absolute positioning\n'
    gcode_str += 'G28 ; Home all axes\n'
    gcode_str += 'M3 ; Activate laser\n'

    for y in range(line_image.size[1]):
        # Determine the direction of travel for each row
        if y % 2 == 0:
            x_range = range(line_image.size[0])
        else:
            x_range = reversed(range(line_image.size[0]))

        for x in x_range:
            r, g, _ = line_image.getpixel((x, y))
            x_pos = x / lines_per_mm_machine  # Calculate X position in millimeters
            y_pos = (img_height - y) / lines_per_mm_machine  # Calculate Y position in millimeters
            x_component = ((r / 255.0) * 2 - 1)  # Calculate X component (-1 to 1)
            y_component = ((g / 255.0) * 2 - 1)  # Calculate Y component (-1 to 1)

            # Calculate laser power based on the orientation of the normals
            laser_power = int(math.sqrt(x_component ** 2 + y_component ** 2) * (laser_max - laser_min) + laser_min)

            gcode_str += 'G1 X{:.2f} Y{:.2f} S{} F{} ; Move to position with laser power\n'.format(x_pos, y_pos, laser_power, laser_speed)

    # Turn off the laser
    gcode_str += 'M5 ; Turn off laser\n'

    # Finish the G-code
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(500)
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
