import gcodegenerator
import re
import matplotlib.pyplot as plt
def load_svg():
    # Set the path to the input SVG file

    # Set the path to the output GCode file
    gcode_path = 'SVG_export_1.gcode'

    # Convert the SVG file to GCode
    gcodegenerator.generate_gcode(svg_path, gcode_path)

    # Print a success message
    print('GCode generated and saved to %s' % gcode_path)

    # Extract X and Y coordinates from GCode file
    x_coords = []
    y_coords = []

    with open(gcode_path, 'r') as f:
        for line in f:
            if 'X' in line and 'Y' in line:
                match = re.findall(r'X([\d.]+).*Y([\d.]+).*Z([\d.]+)', line)
                if match:
                    x_coords.append(float(match[0][0]))
                    y_coords.append(float(match[0][1]))
    plt.style.use('dark_background')
    # Set the background color to black
    fig = plt.figure(facecolor='black')

    # Plot the coordinates with line color 255.167.23
    plt.plot(x_coords, y_coords, color=(255/255, 167/255, 23/255))

    # Show the plot
    plt.show()

