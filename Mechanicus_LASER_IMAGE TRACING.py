import tkinter as tk
from tkinter import filedialog
from PIL import Image

def convert_and_print():
    # Load the image
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x, bed_max_y
    bed_size_x = bed_max_x
    bed_size_y = bed_max_y
    feedrate = 8000

    # Load the image
    img = Image.open('temp2.png').convert('L')

    # Get the image dimensions in pixels
    img_width, img_height = img.size
    print('Image dimensions:', img_width, 'x', img_height)

    # Calculate the scaling factor
    scaling_factor_x = bed_size_x / img_width
    scaling_factor_y = bed_size_y / img_height

    # Use the larger scaling factor to fill the bed in either X or Y direction
    scaling_factor = max(scaling_factor_x, scaling_factor_y)

    # Calculate the scaled dimensions
    scaled_width = int(img_width * scaling_factor)
    scaled_height = int(img_height * scaling_factor)
    print('Image dimensions after scaling:', scaled_width, 'x', scaled_height)

    # Scale the image
    img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    # Convert the image to G-code
    gcode_str = ''  # Initialize G-code string
    gcode_str += 'G21 ; Set units to millimeters\n'  # Set units to millimeters
    gcode_str += 'G90 ; Set absolute positioning\n'  # Set absolute positioning
    gcode_str += 'G28 ; Home all axes\n'  # Home all axes

    is_printing = False  # A flag to keep track of whether the print head is currently down

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixel_value = img.getpixel((x, y))
            if pixel_value > 50:  # Check if the pixel value is greater than 128 (white)
                if not is_printing:
                    # If the print head is currently up, move to the start position of the new line and turn on the laser (S)
                    x_pos = x  # Scale the X-coordinate
                    gcode_str += 'G1 X{:.3f} Y{:.3f} F{} S300 ; Move to print and turn on laser\n'.format(x_pos, bed_size_y - y, feedrate)
                    is_printing = True
            else:  # Pixel is black
                if is_printing:
                    # If the print head is currently down, turn off the laser (S0)
                    gcode_str += 'S0 ; Turn off laser\n'
                    is_printing = False

    # Finish the G-code
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
    gcode_str += 'M5 ; Turn off laser\n'  # Turn off the laser at the end of G-code

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
