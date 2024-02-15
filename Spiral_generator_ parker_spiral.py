import tkinter as tk
from tkinter import ttk, Scrollbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg

def parker_spiral_points(a, b, n_points):
    t_values = np.linspace(0, 4 * np.pi, n_points)  # Adjust the range of t as needed
    r_values = np.where(np.sin(t_values) == 0, 0, a / (np.sin(t_values) ** b))
    x_values = r_values * np.cos(t_values)
    y_values = r_values * np.sin(t_values)
    return x_values, y_values





# Function to generate the Ulam spiral mosaic
def generate_mosaic():
    Nsteps = int(concentric_rectangles_entry.get())
    Xblocks = int(x_blocks_entry.get())
    YBlocks = int(y_blocks_entry.get())
    Xgap = int(x_gap_entry.get())
    Ygap = int(y_gap_entry.get())
    n_points = int(n_points_entry.get())
    # Get input values for 'a' and 'b'
    # Get input values for 'a' and 'b'
    a = float(a_entry.get())
    b = float(b_entry.get())

    # Generate points for Seiffert's spiral
    x_values, y_values = parker_spiral_points(a, b, n_points)

    # Create a new figure with the desired size in inches
    fig, ax = plt.subplots(figsize=(16, 16), dpi=80)
    




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

# Rest of the code for creating the Tkinter window and interface


    



# Create the main window
window = tk.Tk()
window.title("Concentric Rectangles with Spirals")

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
a_label = ttk.Label(window, text="Value of 'a':")
a_label.grid(row=5, column=0)
a_entry = ttk.Entry(window)
a_entry.grid(row=5, column=1)
a_entry.insert(0, "1.0")  # Default value for 'a'

b_label = ttk.Label(window, text="Value of 'b':")
b_label.grid(row=6, column=0)
b_entry = ttk.Entry(window)
b_entry.grid(row=6, column=1)
b_entry.insert(0, "0.2")  # Default value for 'b'

n_points_label = ttk.Label(window, text="Number of Points:")
n_points_label.grid(row=7, column=0)
n_points_entry = ttk.Entry(window)
n_points_entry.grid(row=7, column=1)
n_points_entry.insert(0, "1000")  # Default value for 'n_points'

generate_button = ttk.Button(window, text="Generate Mosaic", command=generate_mosaic)
generate_button.grid(row=6, column=3, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=9, column=0, columnspan=2)

# Run the Tkinter main loop
window.mainloop()
