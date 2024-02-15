import tkinter as tk
from tkinter import ttk, Scrollbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg
# Define a function to generate points along the rectangular spiral
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

# Function to generate the rectangular spiral mosaic
def generate_mosaic():
    N = int(N_entry.get())
    width_increment = float(width_increment_entry.get())
    height_increment = float(height_increment_entry.get())
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
    svg_filename = "rectangular_spiral.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)
    plt.close()

    # Convert the SVG file to PDF (if needed)
    pdf_filename = "rectangular_spiral.pdf"
    cairosvg.svg2pdf(url=svg_filename, write_to=pdf_filename)

    # Display a message
    result_label.config(text=f"Spirangle saved as {pdf_filename}")


# Create the main window
window = tk.Tk()
window.title("Rectangular Spiral")

# Create and place labels and entry fields for input
N_label = ttk.Label(window, text="Number of Rectangles:")
N_label.grid(row=0, column=0)
N_entry = ttk.Entry(window)
N_entry.grid(row=0, column=1)
N_entry.insert(0, "10")  # Default value for 'N'

width_increment_label = ttk.Label(window, text="Width Increment:")
width_increment_label.grid(row=1, column=0)
width_increment_entry = ttk.Entry(window)
width_increment_entry.grid(row=1, column=1)
width_increment_entry.insert(0, "1")  # Default value for 'width_increment'

height_increment_label = ttk.Label(window, text="Height Increment:")
height_increment_label.grid(row=2, column=0)
height_increment_entry = ttk.Entry(window)
height_increment_entry.grid(row=2, column=1)
height_increment_entry.insert(0, "1")  # Default value for 'height_increment'

angle_increment_label = ttk.Label(window, text="Angle Increment (degrees):")
angle_increment_label.grid(row=3, column=0)
angle_increment_entry = ttk.Entry(window)
angle_increment_entry.grid(row=3, column=1)
angle_increment_entry.insert(0, "90")  # Default value for 'angle_increment'

generate_button = ttk.Button(window, text="Generate Spiral", command=generate_mosaic)
generate_button.grid(row=4, column=0, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=2)

# Run the Tkinter main loop
window.mainloop()
