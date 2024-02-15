import tkinter as tk
import svgwrite
import math
import matplotlib.pyplot as plt

def generate_concentric_circles(radius, increment, save_path):
    # Create an SVG drawing object
    dwg = svgwrite.Drawing(save_path, profile='tiny', size=(400, 400))
    
    # Create a matplotlib plot for visualization
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Draw the main circle
    main_circle = dwg.circle(center=(200, 200), r=radius, stroke=svgwrite.rgb(0, 0, 0, '%'), fill='none')
    dwg.add(main_circle)

    # Draw concentric circles with increments
    for i in range(increment, radius, increment):
        circle = dwg.circle(center=(200, 200), r=i, stroke=svgwrite.rgb(0, 0, 0, '%'), fill='none')
        dwg.add(circle)

    # Save the SVG file
    dwg.save()
    
    # Show the plot
    plt.gca().add_patch(plt.Circle((200, 200), radius, fill=False))
    for i in range(increment, radius, increment):
        plt.gca().add_patch(plt.Circle((200, 200), i, fill=False))
    plt.xlim(0, 400)
    plt.ylim(0, 400)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def create_circle():
    radius = int(radius_entry.get())
    increment = int(increment_entry.get())
    save_path = file_entry.get()

    generate_concentric_circles(radius, increment, save_path)

# Create a Tkinter window
window = tk.Tk()
window.title("Concentric Circles SVG Generator")

# Create labels and entry fields for input
radius_label = tk.Label(window, text="Main Circle Radius:")
radius_label.pack()
radius_entry = tk.Entry(window)
radius_entry.pack()

increment_label = tk.Label(window, text="Increment Size:")
increment_label.pack()
increment_entry = tk.Entry(window)
increment_entry.pack()

file_label = tk.Label(window, text="Save as SVG File:")
file_label.pack()
file_entry = tk.Entry(window)
file_entry.pack()

generate_button = tk.Button(window, text="Generate SVG and Plot", command=create_circle)
generate_button.pack()

window.mainloop()
