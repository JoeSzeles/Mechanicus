import tkinter as tk
from tkinter import ttk, Scrollbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg

def mandelbrot(left_boundary, width, height, max_iterations):
    # Create a blank image with the specified width and height
    img = np.zeros((height, width), dtype=np.uint8)

    # Generate the Mandelbrot set
    for x in range(width):
        for y in range(height):
            zx, zy = 0, 0
            cx = left_boundary + x / width * 3.5  # Adjusted to the cardioid left boundary
            cy = y / height * 2 - 1

            for i in range(max_iterations):
                if zx * zx + zy * zy >= 4:
                    break 
                zx, zy = zx * zx - zy * zy + cx, 2 * zx * zy + cy

            # Color the pixel based on the number of iterations
            img[y, x] = i

    return img

def generate_mandelbrot():
    left_boundary = float(left_boundary_entry.get())
    width = int(width_entry.get())
    height = int(height_entry.get())
    max_iterations = int(max_iterations_entry.get())

    # Generate the Mandelbrot set
    mandelbrot_image = mandelbrot(left_boundary, width, height, max_iterations)

    # Create a new figure with the desired size in inches
    fig, ax = plt.subplots(figsize=(6, 6), dpi=80)

    # Display the Mandelbrot set
    ax.imshow(mandelbrot_image, extent=(-2.5, 1.0, -1.0, 1.0), cmap='inferno', origin='lower', aspect='auto')

    # Remove the axis labels
    ax.set_xlabel("")
    ax.set_ylabel("")

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=6, column=0, columnspan=5)

    # Create vertical and horizontal scrollbars
    v_scrollbar = Scrollbar(window, orient="vertical", command=canvas_widget.yview)
    h_scrollbar = Scrollbar(window, orient="horizontal", command=canvas_widget.xview)
    canvas_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # Place the scrollbars
    v_scrollbar.grid(row=6, column=5, sticky="ns")
    h_scrollbar.grid(row=7, column=0, columnspan=5, sticky="ew")

    # Update the canvas's scroll region when the plot changes
    canvas_widget.bind("<Configure>", lambda e: canvas_widget.configure(scrollregion=canvas_widget.bbox("all")))

    # Save the Matplotlib figure as an SVG file
    svg_filename = "mandelbrot_set.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)
    plt.close()

    # Convert the SVG file to PDF using cairosvg
    pdf_filename = "mandelbrot_set.pdf"
    with open(svg_filename, 'rb') as svg_file:
        cairosvg.svg2pdf(file_obj=svg_file, write_to=pdf_filename)

    # Display a message
    result_label.config(text=f"Mandelbrot set saved as {pdf_filename}")

    # Load the generated PDF and display it using CairoSVG
    cairosvg.svg2png(url=svg_filename, write_to=pdf_filename + ".png")
    img = tk.PhotoImage(file=pdf_filename + ".png")
    image_label = ttk.Label(window, image=img)
    image_label.grid(row=8, column=0, columnspan=5)
    image_label.image = img

# Rest of the code for creating the Tkinter window and interface

# Create the main window
window = tk.Tk()
window.title("Mandelbrot Set at Cardioid Left Boundary")

# Create and place labels and entry fields for input
left_boundary_label = ttk.Label(window, text="Left Boundary (Re):")
left_boundary_label.grid(row=0, column=0)
left_boundary_entry = ttk.Entry(window)
left_boundary_entry.grid(row=0, column=1)
left_boundary_entry.insert(0, "-2.0")

width_label = ttk.Label(window, text="Width (pixels):")
width_label.grid(row=1, column=0)
width_entry = ttk.Entry(window)
width_entry.grid(row=1, column=1)
width_entry.insert(0, "800")

height_label = ttk.Label(window, text="Height (pixels):")
height_label.grid(row=2, column=0)
height_entry = ttk.Entry(window)
height_entry.grid(row=2, column=1)
height_entry.insert(0, "800")

max_iterations_label = ttk.Label(window, text="Max Iterations:")
max_iterations_label.grid(row=3, column=0)
max_iterations_entry = ttk.Entry(window)
max_iterations_entry.grid(row=3, column=1)
max_iterations_entry.insert(0, "1000")

generate_button = ttk.Button(window, text="Generate Mandelbrot Set", command=generate_mandelbrot)
generate_button.grid(row=4, column=0, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=2)

# Run the Tkinter main loop
window.mainloop()
