import tkinter as tk
from tkinter import ttk, Scrollbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg
import time

# Function to generate Doppler spirals
def kaleidoscope_mandala(x_values, y_values, num_reflections):
    mirrored_x_values = []
    mirrored_y_values = []
    b = float(b_entry.get())
    for _ in range(num_reflections):
        # Reflect the mandala horizontally
        mirrored_x = -b * x_values
        mirrored_x_values.extend(mirrored_x)
        mirrored_y_values.extend(y_values)

        # Reflect the mandala vertically
        mirrored_y = -b * y_values
        mirrored_x_values.extend(x_values)
        mirrored_y_values.extend(mirrored_y)

        # Rotate the mandala
        x_values, y_values = y_values, -b * x_values
        mirrored_x_values.extend(x_values)
        mirrored_y_values.extend(y_values)

    return mirrored_x_values, mirrored_y_values
# Function to generate Mandala
def generate_mandala(R, A, n, Npoints):
    # Generate theta values (angles)
    theta = np.linspace(0, 2 * np.pi, Npoints)  # You can adjust the number of points

    # Calculate the radius values for each theta
    r = R + A * np.cos(n * theta)

    # Convert polar coordinates to Cartesian coordinates
    x_values = r * np.cos(theta)
    y_values = r * np.sin(theta)

    return x_values, y_values
def save_mandala(R, A, n, n_points):
    # Generate a unique filename based on the current timestamp
    timestamp = int(time.time())
    svg_filename = f"mandala_{timestamp}.svg"
    png_filename = f"mandala_{timestamp}.png"

    # Create a new figure for the mandala
    fig, ax = plt.subplots(figsize=(6, 6), dpi=72)  # Adjust size and dpi as needed

    # Generate Mandala
    x_values, y_values = generate_mandala(R, A, n, n_points)

    # Plot the Mandala
    plt.plot(x_values, y_values, 'b-')
    plt.axis('equal')
    plt.xlabel("")
    plt.ylabel("")

    # Save the Mandala as SVG
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)

    # Save the Mandala as PNG
    plt.savefig(png_filename, format="png", bbox_inches="tight", dpi=300)

    # Close the figure
    plt.close()

    # Display a message
    result_label.config(text=f"Mandala saved as {svg_filename} (SVG) and {png_filename} (PNG)")
def generate_mosaic_with_mandala():
    Nsteps = int(concentric_rectangles_entry.get())
    Xblocks = int(x_blocks_entry.get())
    YBlocks = int(y_blocks_entry.get())
    Xgap = int(x_gap_entry.get())
    Ygap = int(y_gap_entry.get())

    # Get the values of 'a' and 'n_points' from the input fields
    a = float(a_entry.get())
    b = float(b_entry.get())
    n_points = int(n_points_entry.get())

    # Get the values of 'R', 'A', and 'n' for the Mandala from the input fields
    R = float(R_entry.get())
    A = float(A_entry.get())
    n = int(n_entry.get())

    # Generate Mandala
    x_values, y_values = generate_mandala(R, A, n, n_points)

    # Apply kaleidoscope effect
    num_reflections = int(a_entry.get())  # You can adjust the number of reflections as needed
    mirrored_x, mirrored_y = kaleidoscope_mandala(x_values, y_values, num_reflections)

    # Create a new figure with the desired size in inches (300x300 mm)
    fig, ax = plt.subplots(figsize=(300/25.4, 300/25.4), dpi=72)

    # Create a single plot to combine all concentric rectangles in mm
    plt.figure(figsize=(10, 10))  # mm

    # Create a loop to draw concentric rectangles with spirals
    for step in range(Nsteps):
        Xo = Xblocks - step * 2  # Number of times to replicate along the x-axis
        Yo = YBlocks - step * 2  # Number of times to replicate along the y-axis

        # Calculate the size of the individual pattern
        pattern_width = max(mirrored_x) - min(mirrored_x)
        pattern_height = max(mirrored_y) - min(mirrored_y)

        # Calculate the total width and height of the mosaic
        mosaic_width = Xo * pattern_width + (Xo - 1) * Xgap
        mosaic_height = Yo * pattern_height + (Yo - 1) * Ygap

        # Create the rectangle as a list of points along the outline
        rectangle_x = []
        rectangle_y = []

        # Top edge of the rectangle
        for x in np.linspace(-mosaic_width / 2, mosaic_width / 2, n_points):
            rectangle_x.append(x)
            rectangle_y.append(mosaic_height / 2)

        # Right edge of the rectangle
        for y in np.linspace(-mosaic_height / 2, mosaic_height / 2, n_points):
            rectangle_x.append(mosaic_width / 2)
            rectangle_y.append(y)

        # Bottom edge of the rectangle
        for x in np.linspace(mosaic_width / 2, -mosaic_width / 2, n_points):
            rectangle_x.append(x)
            rectangle_y.append(-mosaic_height / 2)

        # Left edge of the rectangle
        for y in np.linspace(mosaic_height / 2, -mosaic_height / 2, n_points):
            rectangle_x.append(-mosaic_width / 2)
            rectangle_y.append(y)

        # Plot the mosaic without connecting lines (spiral outline)
        current_spiral = []
        for x, y in zip(mirrored_x, mirrored_y):
            current_spiral.append((x, y))

        current_spiral = np.array(current_spiral)

        # Calculate the offset for centering
        x_offset = mosaic_width / 2
        y_offset = mosaic_height / 2

        # Replicate the spiral pattern along the rectangle outline (blue spirals)
        for _ in range(Xo):
            plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
            x_offset -= pattern_width + Xgap

        for _ in range(Yo):
            plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
            y_offset -= pattern_height + Ygap

        for _ in range(Xo):
            plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
            x_offset += pattern_width + Xgap

        for _ in range(Yo):
            plt.plot(current_spiral[:, 0] + x_offset, current_spiral[:, 1] + y_offset, 'b-')
            y_offset += pattern_height + Ygap

    # Remove the axis labels
    plt.xlabel("")
    plt.ylabel("")

    plt.axis('equal')

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=17, column=5, columnspan=1)

    # Save the Matplotlib figure as an SVG file
    svg_filename = "concentric_mandalas.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)
    plt.close()

    # Convert the SVG file to PDF (if needed)
    pdf_filename = "concentric_rectangles.pdf"
    cairosvg.svg2pdf(url=svg_filename, write_to=pdf_filename)

    # Cleanup the temporary SVG file
    import os
    # os.remove(svg_filename)

    # Display a message
    result_label.config(text=f"Mosaic saved as {pdf_filename}")

    # Create vertical and horizontal scrollbars
    v_scrollbar = Scrollbar(window, orient="vertical", command=canvas_widget.yview)
    h_scrollbar = Scrollbar(window, orient="horizontal", command=canvas_widget.xview)
    canvas_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Update the canvas's scroll region when the plot changes
    canvas_widget.bind("<Configure>", lambda e: canvas_widget.configure(scrollregion=canvas_widget.bbox("all")))

# Function to handle the window close event
def on_closing():
    window.destroy()  # Close the Tkinter application

# Create the main window
window = tk.Tk()
window.title("Mandala Spirals")

# Set a function to handle the window close event
window.protocol("WM_DELETE_WINDOW", on_closing)

# Create and place labels and entry fields for input
concentric_rectangles_label = ttk.Label(window, text="Number of Concentric Rectangles:")
concentric_rectangles_label.grid(row=0, column=0)
concentric_rectangles_entry = ttk.Entry(window)
concentric_rectangles_entry.grid(row=0, column=1)
concentric_rectangles_entry.insert(0, "3")

x_blocks_label = ttk.Label(window, text="X Blocks:")
x_blocks_label.grid(row=1, column=0)
x_blocks_entry = ttk.Entry(window)
x_blocks_entry.grid(row=1, column=1)
x_blocks_entry.insert(0, "30")

y_blocks_label = ttk.Label(window, text="Y Blocks:")
y_blocks_label.grid(row=2, column=0)
y_blocks_entry = ttk.Entry(window)
y_blocks_entry.grid(row=2, column=1)
y_blocks_entry.insert(0, "15")

x_gap_label = ttk.Label(window, text="X Gap:")
x_gap_label.grid(row=3, column=0)
x_gap_entry = ttk.Entry(window)
x_gap_entry.grid(row=3, column=1)
x_gap_entry.insert(0, "1")

y_gap_label = ttk.Label(window, text="Y Gap:")
y_gap_label.grid(row=4, column=0)
y_gap_entry = ttk.Entry(window)
y_gap_entry.grid(row=4, column=1)
y_gap_entry.insert(0, "1")

# Add input fields for 'a' and 'n_points'
a_label = ttk.Label(window, text="Number of reflections")
a_label.grid(row=5, column=0)
a_entry = ttk.Entry(window)
a_entry.grid(row=5, column=1)
a_entry.insert(0, "3")  # Default value for 'a'

b_label = ttk.Label(window, text="Value of 'b':")
b_label.grid(row=6, column=0)
b_entry = ttk.Entry(window)
b_entry.grid(row=6, column=1)
b_entry.insert(0, "0.2")  # Default value for 'b'

n_points_label = ttk.Label(window, text="Number of Points:")
n_points_label.grid(row=7, column=0)
n_points_entry = ttk.Entry(window)
n_points_entry.grid(row=7, column=1)
n_points_entry.insert(0, "100")  # Default value for 'n_points'

# Create and place labels and entry fields for input
R_label = ttk.Label(window, text="Radius (R):")
R_label.grid(row=8, column=0)
R_entry = ttk.Entry(window)
R_entry.grid(row=8, column=1)
R_entry.insert(0, "3.0")  # Default value for R

A_label = ttk.Label(window, text="Amplitude (A):")
A_label.grid(row=9, column=0)
A_entry = ttk.Entry(window)
A_entry.grid(row=9, column=1)
A_entry.insert(0, "0.6")  # Default value for A

n_label = ttk.Label(window, text="Number of Segments (n):")
n_label.grid(row=10, column=0)
n_entry = ttk.Entry(window)
n_entry.grid(row=10, column=1)
n_entry.insert(0, "66")  # Default value for n

generate_button = ttk.Button(window, text="Generate Mosaic with Mandala", command=generate_mosaic_with_mandala)
generate_button.grid(row=11, column=0, columnspan=2)
# Create "Save Mandala" button
# Create "Save Mandala" button
save_mandala_button = ttk.Button(window, text="Save Mandala", command=lambda: save_mandala(float(R_entry.get()), float(A_entry.get()), int(n_entry.get()), int(n_points_entry.get())))
save_mandala_button.grid(row=11, column=2, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=12, column=0, columnspan=2)


# Run the tkinter main loop
window.mainloop()

