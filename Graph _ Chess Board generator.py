import tkinter as tk
from tkinter import filedialog
import svgwrite

def generate_chessboard():
    # Get values from input boxes
    board_width_mm = float(board_width_entry.get())
    board_height_mm = float(board_height_entry.get())
    square_size_mm = float(square_size_entry.get())
    output_file_path = output_file_entry.get()

    # Calculate the number of squares in a row and column
    num_squares_x = int(board_width_mm / square_size_mm)
    num_squares_y = int(board_height_mm / square_size_mm)

    # Create an SVG drawing
    dwg = svgwrite.Drawing(output_file_path, profile='tiny', size=(f"{board_width_mm}mm", f"{board_height_mm}mm"))

    # Define SVG line style for board squares
    square_colors = ["white", "black"]
    row_labels = "87654321"  # Rows A to H
    col_labels = "abcdefgh"  # Columns 1 to 8

    for i in range(num_squares_x):
        for j in range(num_squares_y):
            square_color = square_colors[(i + j) % 2]
            dwg.add(dwg.rect(insert=(i * square_size_mm, j * square_size_mm), size=(square_size_mm, square_size_mm), fill=square_color))

    # Draw row labels (A to H)
    for i, label in enumerate(row_labels):
        dwg.add(dwg.text(label, insert=(board_width_mm + 5, i * square_size_mm + square_size_mm / 2), fill="black", font_size=square_size_mm * 0.75, font_family="Arial"))

    # Draw column labels (1 to 8)
    for i, label in enumerate(col_labels):
        dwg.add(dwg.text(label, insert=(i * square_size_mm + square_size_mm / 2, board_height_mm + 10), fill="black", font_size=square_size_mm * 0.75, font_family="Arial"))

    # Save the SVG file
    dwg.save()
    result_label.config(text=f"Chessboard generated and saved to {output_file_path}!")

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Files", "*.svg")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("Chessboard Generator")

# Create input boxes and labels
board_width_label = tk.Label(root, text="Board Width (mm):")
board_width_label.pack()
board_width_entry = tk.Entry(root)
board_width_entry.pack()
board_width_entry.insert(0, "200")  # Default value

board_height_label = tk.Label(root, text="Board Height (mm):")
board_height_label.pack()
board_height_entry = tk.Entry(root)
board_height_entry.pack()
board_height_entry.insert(0, "200")  # Default value

square_size_label = tk.Label(root, text="Square Size (mm):")
square_size_label.pack()
square_size_entry = tk.Entry(root)
square_size_entry.pack()
square_size_entry.insert(0, "25")  # Default value

output_file_label = tk.Label(root, text="Output File:")
output_file_label.pack()
output_file_entry = tk.Entry(root)
output_file_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_button.pack()

generate_button = tk.Button(root, text="Generate Chessboard", command=generate_chessboard)
generate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
