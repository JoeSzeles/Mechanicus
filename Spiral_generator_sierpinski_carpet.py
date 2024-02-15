import tkinter as tk
from tkinter import ttk, Scrollbar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg
import time

# Function to generate a Sierpinski carpet
# Function to generate a Sierpinski carpet with color variation
def generate_sierpinski_carpet(size, n):
    def draw_carpet(x, y, size, n, color):
        if n == 0:
            return
        sub_size = size / 3

        # Create the 8 smaller sub-squares with different colors
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'cyan', 'magenta']
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue  # Skip the center square
                new_color = colors.pop(0) if colors else color
                plt.fill([x + i * sub_size, x + (i + 1) * sub_size, x + (i + 1) * sub_size, x + i * sub_size, x + i * sub_size],
                         [y + j * sub_size, y + j * sub_size, y + (j + 1) * sub_size, y + (j + 1) * sub_size, y + j * sub_size],
                         new_color, edgecolor="black")
                draw_carpet(x + i * sub_size, y + j * sub_size, sub_size, n - 1, new_color)

    # Create a new figure for the Sierpinski carpet
    fig, ax = plt.subplots(figsize=(size/72, size/72), dpi=72)  # Adjust size and dpi as needed
    ax.set_aspect('equal')  # Set aspect ratio to be equal

    # Generate the Sierpinski carpet with color variation
    draw_carpet(0, 0, size, n, 'gray')

    # Remove the axis labels
    plt.axis('off')

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=17, column=5, columnspan=1)

def save_sierpinski_carpet(n, size):
    # Generate a unique filename based on the current timestamp
    timestamp = int(time.time())
    svg_filename = f"sierpinski_carpet_{timestamp}.svg"
    png_filename = f"sierpinski_carpet_{timestamp}.png"

    # Create a new figure for the Sierpinski carpet
    fig, ax = plt.subplots(figsize=(size/72, size/72), dpi=72)  # Adjust size and dpi as needed
    ax.set_aspect('equal')  # Set aspect ratio to be equal

    # Generate the Sierpinski carpet
    generate_sierpinski_carpet(size, n)

    # Remove the axis labels
    plt.axis('off')

    # Save the Sierpinski carpet as SVG
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)

    # Save the Sierpinski carpet as PNG
    plt.savefig(png_filename, format="png", bbox_inches="tight", dpi=300)

    # Close the figure
    plt.close()

    # Display a message
    result_label.config(text=f"Sierpinski carpet saved as {svg_filename} (SVG) and {png_filename} (PNG)")

# Rest of your code remains the same

# Run the tkinter main loop
window = tk.Tk()
window.title("Sierpinski Carpet Generator")

# Create and place labels and entry fields for input
size_label = ttk.Label(window, text="Size:")
size_label.grid(row=13, column=0)
size_entry = ttk.Entry(window)
size_entry.grid(row=13, column=1)
size_entry.insert(0, "300")  # Default value for size

sierpinski_depth_label = ttk.Label(window, text="Sierpinski Depth:")
sierpinski_depth_label.grid(row=14, column=0)
sierpinski_depth_entry = ttk.Entry(window)
sierpinski_depth_entry.grid(row=14, column=1)
sierpinski_depth_entry.insert(0, "3")  # Default value for Sierpinski depth

generate_sierpinski_button = ttk.Button(window, text="Generate Sierpinski Carpet", command=lambda: generate_sierpinski_carpet(float(size_entry.get()), int(sierpinski_depth_entry.get())))
generate_sierpinski_button.grid(row=15, column=0, columnspan=2)

# Create "Save Sierpinski Carpet" button
save_sierpinski_button = ttk.Button(window, text="Save Sierpinski Carpet", command=lambda: save_sierpinski_carpet(int(sierpinski_depth_entry.get()), float(size_entry.get())))
save_sierpinski_button.grid(row=15, column=2, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=16, column=0, columnspan=4)

# Run the tkinter main loop
window.mainloop()
