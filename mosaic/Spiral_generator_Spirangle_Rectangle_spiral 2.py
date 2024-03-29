import tkinter as tk
from tkinter import ttk, Scrollbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg

def rectangular_spirangle_points(N, width_increment, height_increment, angle_increment):
    x_values = []
    y_values = []
    x, y = 0, 0
    for _ in range(N):
        # Calculate the end coordinates of the four line segments forming a rectangle
        for _ in range(4):
            x_end = x + width_increment * np.cos(np.radians(angle_increment))
            y_end = y + height_increment * np.sin(np.radians(angle_increment))
            
            # Append the line segment to the spiral
            x_values.extend([x, x_end])
            y_values.extend([y, y_end])
            
            # Update the current position
            x, y = x_end, y_end
            
            # Rotate by 90 degrees to form the next side of the rectangle
            angle_increment += 90
        # Increase the width and height for the next rectangle
        width_increment += 0.1
        height_increment += 0.1
    return x_values, y_values








# Function to generate the Ulam spiral mosaic
def generate_mosaic():
    Nsteps = int(concentric_rectangles_entry.get())
    Xblocks = int(x_blocks_entry.get())
    YBlocks = int(y_blocks_entry.get())
    Xgap = int(x_gap_entry.get())
    Ygap = int(y_gap_entry.get())
    n_points = int(n_points_entry.get())
    # Get input values for 'N', 'angle_increment', and 'length_increment'
    N = int(N_entry.get())
    angle_increment = float(angle_increment_entry.get())
    length_increment = float(length_increment_entry.get())
    width_increment = float(angle_increment_entry.get())
    height_increment = float(length_increment_entry.get())
    angle_increment = float(angle_increment_entry.get())

    # Generate points for the rectangular spiral pattern
    x_values, y_values = rectangular_spirangle_points(N, width_increment, height_increment, angle_increment)

    # Create a new figure with the desired size in inches
    fig, ax = plt.subplots(figsize=(6, 6), dpi=80)

    # Plot the rectangular spiral
    ax.plot(x_values, y_values, label="Rectangular Spiral")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Rectangular Spiral")
    ax.legend()

    # Save the Matplotlib figure as an SVG file
    svg_filename = "rectangular_spiral.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)
    plt.close()

    # Convert the SVG file to PDF using cairosvg
    pdf_filename = "rectangular_spiral.pdf"
    with open(svg_filename, 'rb') as svg_file:
        cairosvg.svg2pdf(file_obj=svg_file, write_to=pdf_filename)

    # Display a message
    result_label.config(text=f"Spirangle saved as {pdf_filename}")

    # Load the generated PDF and display it using CairoSVG
    cairosvg.svg2png(url=svg_filename, write_to=pdf_filename + ".png")
    img = tk.PhotoImage(file=pdf_filename + ".png")
    image_label = ttk.Label(window, image=img)
    image_label.grid(row=10, column=0, columnspan=5)
    image_label.image = img
    




    # Create a loop to draw concentric rectangles with Ulam spiral
    for step in range(Nsteps):
        Xo = Xblocks - step * 2  # Number of times to replicate along the x-axis
        Yo = YBlocks - step * 2  # Number of times to replicate along the y-axis

        # Calculate the size of the individual pattern
        pattern_width = max(x_values) - min(x_values)
        pattern_height = max(y_values) - min(y_values)

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

        # Plot the mosaic without connecting lines (Ulam spiral outline)
        current_spiral = []
        for x, y in zip(x_values, y_values):
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
    canvas_widget.grid(row=8, column=0, columnspan=5)

    # Create vertical and horizontal scrollbars
    v_scrollbar = Scrollbar(window, orient="vertical", command=canvas_widget.yview)
    h_scrollbar = Scrollbar(window, orient="horizontal", command=canvas_widget.xview)
    canvas_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Place the scrollbars
    v_scrollbar.grid(row=8, column=5, sticky="ns")
    h_scrollbar.grid(row=9, column=0, columnspan=5, sticky="ew")

    # Update the canvas's scroll region when the plot changes
    canvas_widget.bind("<Configure>", lambda e: canvas_widget.configure(scrollregion=canvas_widget.bbox("all")))

    # Save the Matplotlib figure as an SVG file
    svg_filename = "concentric_rectangles_ulam.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)
    plt.close()

    # Convert the SVG file to PDF (if needed)
    pdf_filename = "concentric_rectangles_ulam.pdf"
    cairosvg.svg2pdf(url=svg_filename, write_to=pdf_filename)

    # Cleanup the temporary SVG file
    import os
    # os.remove(svg_filename)

    # Display a message
    result_label.config(text=f"Mosaic saved as {pdf_filename}")


# Function to handle the window close event
def on_closing():
    window.destroy()  # Close the Tkinter application

# Create the main window
window = tk.Tk()
window.title("Spirangle Rectangle Spirals")

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

N_label = ttk.Label(window, text="Number of Line Segments:")
N_label.grid(row=5, column=0)
N_entry = ttk.Entry(window)
N_entry.grid(row=5, column=1)
N_entry.insert(0, "36")  # Default value for 'N'

angle_increment_label = ttk.Label(window, text="Angle Increment (degrees):")
angle_increment_label.grid(row=6, column=0)
angle_increment_entry = ttk.Entry(window)
angle_increment_entry.grid(row=6, column=1)
angle_increment_entry.insert(0, "10")  # Default value for 'angle_increment'

length_increment_label = ttk.Label(window, text="Length Increment:")
length_increment_label.grid(row=7, column=0)
length_increment_entry = ttk.Entry(window)
length_increment_entry.grid(row=7, column=1)
length_increment_entry.insert(0, "1")  # Default value for 'length_increment'

n_points_label = ttk.Label(window, text="Number of Points:")
n_points_label.grid(row=5, column=3)
n_points_entry = ttk.Entry(window)
n_points_entry.grid(row=5, column=4)
n_points_entry.insert(0, "1000")  # Default value for 'n_points'

generate_button = ttk.Button(window, text="Generate Mosaic", command=generate_mosaic)
generate_button.grid(row=6, column=3, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=10, column=0, columnspan=2)

# Run the Tkinter main loop
window.mainloop()
