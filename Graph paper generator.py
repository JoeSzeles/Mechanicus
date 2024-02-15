import tkinter as tk
from tkinter import filedialog
import svgwrite

def generate_graph_paper():
    # Get values from input boxes
    paper_width_mm = float(paper_width_entry.get())
    paper_height_mm = float(paper_height_entry.get())
    grid_size_mm = float(grid_size_entry.get())
    bold_line_interval_mm = float(bold_line_interval_entry.get())

    # Get the output file path
    output_file_path = output_file_entry.get()

    # Convert grid size and bold line interval from mm to inches
    grid_size_in = grid_size_mm / 25.4
    bold_line_interval_in = bold_line_interval_mm / 25.4

    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_file_path, profile='tiny', size=(f"{paper_width_mm}mm", f"{paper_height_mm}mm"))

    # Define SVG line style for bold and regular lines
    bold_line_color = "black"
    regular_line_color = "black"
    bold_line_width = 0.4  # Adjust as needed for bolder lines
    regular_line_width = 0.1  # Adjust as needed for regular lines

    # Draw vertical grid lines
    for x in range(0, int(paper_width_mm) + 1, int(grid_size_mm)):
        if x % int(bold_line_interval_mm) == 0:
            dwg.add(dwg.line(start=(x, 0), end=(x, paper_height_mm), stroke=bold_line_color, stroke_width=bold_line_width))
        else:
            dwg.add(dwg.line(start=(x, 0), end=(x, paper_height_mm), stroke=regular_line_color, stroke_width=regular_line_width))

    # Draw horizontal grid lines
    for y in range(0, int(paper_height_mm) + 1, int(grid_size_mm)):
        if y % int(bold_line_interval_mm) == 0:
            dwg.add(dwg.line(start=(0, y), end=(paper_width_mm, y), stroke=bold_line_color, stroke_width=bold_line_width))
        else:
            dwg.add(dwg.line(start=(0, y), end=(paper_width_mm, y), stroke=regular_line_color, stroke_width=regular_line_width))

    # Save the SVG file
    dwg.save()
    result_label.config(text=f"Graph paper generated and saved to {output_file_path}!")

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Files", "*.svg")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("Graph Paper Generator")

# Create input boxes and labels
paper_width_label = tk.Label(root, text="Paper Width (mm):")
paper_width_label.pack()
paper_width_entry = tk.Entry(root)
paper_width_entry.pack()
paper_width_entry.insert(0, "400")  # Default value

paper_height_label = tk.Label(root, text="Paper Height (mm):")
paper_height_label.pack()
paper_height_entry = tk.Entry(root)
paper_height_entry.pack()
paper_height_entry.insert(0, "400")  # Default value

grid_size_label = tk.Label(root, text="Grid Size (mm):")
grid_size_label.pack()
grid_size_entry = tk.Entry(root)
grid_size_entry.pack()
grid_size_entry.insert(0, "2")  # Default value

bold_line_interval_label = tk.Label(root, text="Bold Line Interval (mm):")
bold_line_interval_label.pack()
bold_line_interval_entry = tk.Entry(root)
bold_line_interval_entry.pack()
bold_line_interval_entry.insert(0, "10")  # Default value

output_file_label = tk.Label(root, text="Output File:")
output_file_label.pack()
output_file_entry = tk.Entry(root)
output_file_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_button.pack()

generate_button = tk.Button(root, text="Generate", command=generate_graph_paper)
generate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
