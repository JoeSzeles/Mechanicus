import tkinter as tk
from tkinter import ttk, Scrollbar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cairosvg

# Function to generate Doppler spirals
def generate_doppler_spirals(a, b, n_spirals, n_points):
    main_circle_radius = 1.0  # Radius of the main circle
    
    # Calculate evenly spaced angles for the origins of Doppler spirals
    origin_angles = np.linspace(0, 2 * np.pi, n_spirals, endpoint=False)
    
    # Initialize arrays to store x and y values for all spirals
    x_values = []
    y_values = []

    for angle in origin_angles:
        t_values = np.linspace(0, a * np.pi, n_points)
        x_spiral = main_circle_radius * np.cos(angle) + a * np.cos(t_values) * np.cos(2 * t_values)
        y_spiral = main_circle_radius * np.sin(angle) + a * np.sin(t_values) * np.cos(2 * t_values)
        
        x_values.append(x_spiral)
        y_values.append(y_spiral)

    return x_values, y_values

# Function to generate the mandala-like pattern
def generate_mandala():
    n_spirals = int(spirals_entry.get())  # Number of spirals
    a = float(a_entry.get())  # 'a' parameter of Doppler spirals
    b = float(b_entry.get())  # 'b' parameter of Doppler spirals
    n_points = int(n_points_entry.get())  # Number of points per spiral

    x_spirals, y_spirals = generate_doppler_spirals(a, b, n_spirals, n_points)

    # Create a new figure with the desired size in inches
    fig, ax = plt.subplots(figsize=(6, 6), dpi=80)

    # Plot the Doppler spirals
    for i in range(n_spirals):
        ax.plot(x_spirals[i], y_spirals[i], 'bo')  # Adjust the style and color as needed

    # Set the aspect ratio to equal and remove axis labels
    ax.set_aspect('equal')
    ax.set_axis_off()

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
    svg_filename = "mandala.svg"
    plt.savefig(svg_filename, format="svg", bbox_inches="tight", dpi=300)
    plt.close()

    # Convert the SVG file to PDF using cairosvg
    pdf_filename = "mandala.pdf"
    with open(svg_filename, 'rb') as svg_file:
        cairosvg.svg2pdf(file_obj=svg_file, write_to=pdf_filename)

    # Display a message
    result_label.config(text=f"Mandala saved as {pdf_filename}")

# Rest of the code for creating the Tkinter window and interface


# Create the main window
window = tk.Tk()
window.title("Doppler Spiral Mandala Generator")

# Create and place labels and entry fields for input
spirals_label = ttk.Label(window, text="Number of Spirals:")
spirals_label.grid(row=0, column=0)
spirals_entry = ttk.Entry(window)
spirals_entry.grid(row=0, column=1)
spirals_entry.insert(0, "6")  # Default value for number of spirals

a_label = ttk.Label(window, text="Value of 'a':")
a_label.grid(row=1, column=0)
a_entry = ttk.Entry(window)
a_entry.grid(row=1, column=1)
a_entry.insert(0, "0.5")  # Default value for 'a'

b_label = ttk.Label(window, text="Value of 'b':")
b_label.grid(row=2, column=0)
b_entry = ttk.Entry(window)
b_entry.grid(row=2, column=1)
b_entry.insert(0, "0.2")  # Default value for 'b'

n_points_label = ttk.Label(window, text="Number of Points per Spiral:")
n_points_label.grid(row=3, column=0)
n_points_entry = ttk.Entry(window)
n_points_entry.grid(row=3, column=1)
n_points_entry.insert(0, "500")  # Default value for number of points

generate_button = ttk.Button(window, text="Generate Mandala", command=generate_mandala)
generate_button.grid(row=4, column=0, columnspan=2)

result_label = ttk.Label(window, text="")
result_label.grid(row=5, column=0, columnspan=2)

# Run the Tkinter main loop
window.mainloop()
