import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to execute the selected algorithm
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
    
    for file in python_files:
        # Remove the ".py" extension
        algo_name = os.path.splitext(file)[0]
        

        # Create a button for each algorithm with the desired background and text color and fixed width
        algo_button = tk.Button(root, text=algo_name, command=lambda file=file: run_algorithm(os.path.join(folder_path, file)), bg="#263d42", fg="white", width=250)
        algo_button.pack()

# Create the main Tkinter window
root = tk.Tk()
root.title("MECHANICUS V.0.1 Beta. (c)Reservoir Frogs 2023")
root.configure(bg="#263d42", borderwidth=0)
root.iconphoto(True, tk.PhotoImage(file='icon/icon.png'))
root.geometry('324x900+0+0')

# Load Python files and create buttons
load_python_files()

# Start the main event loop
root.mainloop()
