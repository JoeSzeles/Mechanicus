import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to generate and display the mandala
def generate_mandala():
    R = float(R_entry.get())  # Radius of the innermost circle (center)
    A = float(A_entry.get())  # Amplitude or maximum variation in radius
    n = int(n_entry.get())    # Number of segments or "petals"
    Npoints = int(n_points_entry.get())
    # Generate theta values (angles)
    theta = np.linspace(0, 2 * np.pi, Npoints)  # You can adjust the number of points

    # Calculate the radius values for each theta
    r = R + A * np.cos(n * theta)

    # Convert polar coordinates to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Create a plot
    plt.figure(figsize=(6, 6))
    plt.plot(x, y)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')  # Turn off the axis

    # Save the mandala
    plt.savefig('mandala.png', dpi=300, bbox_inches='tight')

    # Display the mandala in the tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=4, column=0, columnspan=2)

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


result_label = ttk.Label(window, text="")
result_label.grid(row=9, column=0, columnspan=2)


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
n_label.grid(row=9, column=3)
n_entry = ttk.Entry(window)
n_entry.grid(row=9, column=4)
n_entry.insert(0, "66")  # Default value for n

generate_button = ttk.Button(window, text="Generate Mandala", command=generate_mandala)
generate_button.grid(row=9, column=5, columnspan=2)






# Run the tkinter main loop
window.mainloop()
