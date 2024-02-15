import os
import tkinter as tk
from tkinter import messagebox
import subprocess


def Spirals():
    # Function to execute the selected algorithm
        # Create the main Tkinter window

    window = tk.Toplevel(height=0 , width=0, bg="#263d42",cursor="circle", borderwidth=0)
    window.title("MECHANICUS_V.0.1 Beta. (c)Reservoir Frogs 2022")
    window.configure(bg="#263d42", borderwidth=0)
    
    def run_algorithm(filename):
        try:
            subprocess.run(["python", filename])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Function to load Python files from the "mosaic" folder
    def load_python_files():
        folder_path = "mosaic"  # Change this to your folder path

        if not os.path.exists(folder_path):
            messagebox.showerror("Error", f"The 'mosaic' folder does not exist.")
            return

        python_files = [f for f in os.listdir(folder_path) if f.endswith(".py")]

        if not python_files:
            messagebox.showinfo("Info", "No Python files found in the 'mosaic' folder.")

        button_frame = tk.Frame(window, bg="#263d42")  # Create a frame for buttons
        button_frame.pack()

        buttons_per_row = 3  # Number of buttons per row
        current_row = []  # Track buttons in the current row

        for file in python_files:
            algo_name = os.path.splitext(file)[0]

            # Create a button for each algorithm with the desired background and text color
            algo_button = tk.Button(button_frame, text=algo_name, command=lambda file=file: run_algorithm(os.path.join(folder_path, file)), bg="#263d42", fg="white", width=40)
            current_row.append(algo_button)

            if len(current_row) == buttons_per_row:
                # If the current row is full, create a new row
                for button in current_row:
                    button.grid(row=len(button_frame.grid_slaves()) // buttons_per_row, column=len(button_frame.grid_slaves()) % buttons_per_row)
                current_row = []

        # Place any remaining buttons in the last row
        for button in current_row:
            button.grid(row=len(button_frame.grid_slaves()) // buttons_per_row, column=len(button_frame.grid_slaves()) % buttons_per_row)

   
    # Load Python files and create buttons
    load_python_files()
    # Start the main event loop
    window.mainloop()


