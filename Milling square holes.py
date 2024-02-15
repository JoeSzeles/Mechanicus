import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
class GCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("G-Code Generator for Square Holes")
        
        self.create_ui()

    def create_ui(self):
        self.coordinate_mode = tk.StringVar(value="relative")
        self.coordinate_mode.trace("w", self.update_coordinate_mode)
        
        self.mode_label = ttk.Label(self.root, text="Coordinate Mode:")
        self.mode_frame = ttk.Frame(self.root)
        
        self.relative_radio = ttk.Radiobutton(self.mode_frame, text="Relative", variable=self.coordinate_mode, value="relative")
        self.absolute_radio = ttk.Radiobutton(self.mode_frame, text="Absolute", variable=self.coordinate_mode, value="absolute")
        
        self.mode_label.pack(pady=5)
        self.mode_frame.pack(pady=5)
        self.relative_radio.pack(side="left")
        self.absolute_radio.pack(side="left")
        
        self.width_label = ttk.Label(self.root, text="Rectangle Width:")
        self.width_entry = ttk.Entry(self.root)
        self.height_label = ttk.Label(self.root, text="Rectangle Height:")
        self.height_entry = ttk.Entry(self.root)
        self.tool_diameter_label = ttk.Label(self.root, text="Tool Diameter:")
        self.tool_diameter_entry = ttk.Entry(self.root)
        self.speed_label = ttk.Label(self.root, text="Milling Speed (F):")
        self.speed_entry = ttk.Entry(self.root)
        self.depth_label = ttk.Label(self.root, text="Depth of Hole:")
        self.depth_entry = ttk.Entry(self.root)
        self.layer_steps_label = ttk.Label(self.root, text="Layer Steps:")
        self.layer_steps_entry = ttk.Entry(self.root)
        
        self.center_x_label = ttk.Label(self.root, text="Center X (Absolute):")
        self.center_x_entry = ttk.Entry(self.root)
        self.center_y_label = ttk.Label(self.root, text="Center Y (Absolute):")
        self.center_y_entry = ttk.Entry(self.root)
        
        self.generate_button = ttk.Button(self.root, text="Generate G-code", command=self.generate_gcode)
        
        self.width_label.pack(pady=5)
        self.width_entry.pack(pady=5)
        self.height_label.pack(pady=5)
        self.height_entry.pack(pady=5)
        self.tool_diameter_label.pack(pady=5)
        self.tool_diameter_entry.pack(pady=5)
        self.speed_label.pack(pady=5)
        self.speed_entry.pack(pady=5)
        self.depth_label.pack(pady=5)
        self.depth_entry.pack(pady=5)
        self.layer_steps_label.pack(pady=5)
        self.layer_steps_entry.pack(pady=5)
        self.center_x_label.pack(pady=5)
        self.center_x_entry.pack(pady=5)
        self.center_y_label.pack(pady=5)
        self.center_y_entry.pack(pady=5)
        self.generate_button.pack(pady=10)
        
    def update_coordinate_mode(self, *args):
        if self.coordinate_mode.get() == "relative":
            self.center_x_label.config(state="disabled")
            self.center_x_entry.config(state="disabled")
            self.center_y_label.config(state="disabled")
            self.center_y_entry.config(state="disabled")
        else:
            self.center_x_label.config(state="normal")
            self.center_x_entry.config(state="normal")
            self.center_y_label.config(state="normal")
            self.center_y_entry.config(state="normal")
        
    def generate_gcode(self):
        try:
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            tool_diameter = float(self.tool_diameter_entry.get())
            speed = int(self.speed_entry.get())
            depth = float(self.depth_entry.get())
            layer_steps = float(self.layer_steps_entry.get())
            center_x = float(self.center_x_entry.get()) if self.center_x_entry.get() else 0.0
            center_y = float(self.center_y_entry.get()) if self.center_y_entry.get() else 0.0

            gcode = self.generate_square_holes_gcode(width, height, tool_diameter, speed, depth, layer_steps, center_x, center_y)

            file_path = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("G-code Files", "*.gcode")])
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(gcode)
                print("G-code saved to:", file_path)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            
    def generate_square_holes_gcode(self, width, height, tool_diameter, speed, depth, layer_steps, center_x, center_y):
        gcode = f"G21 ; Set units to millimeters\n"
        gcode += f"G91 ; Set to relative positioning mode\n"
        gcode += f"G0 Z0 F300\n"  # Move to safe Z height
    
        # Calculate the number of passes
        num_passes = int(depth / layer_steps) + 1
        
        for pass_num in range(num_passes):
            # Calculate starting point for the current pass
            start_x = center_x - width / 2
            start_y = center_y - height / 2 + pass_num * layer_steps
            
            # Move to starting point
            gcode += f"G0 X{start_x:.2f} Y{start_y:.2f} F{speed}\n"
            
            # Generate G-code for raster pattern
            while start_x + tool_diameter / 2 <= center_x + width / 2:
                gcode += f"G1 X{start_x + tool_diameter:.2f} F{speed}\n"
                gcode += f"G1 Y{start_y + height:.2f} F{speed}\n"
                gcode += f"G1 X{start_x:.2f} F{speed}\n"
                gcode += f"G1 Y{start_y:.2f} F{speed}\n"
                start_x += tool_diameter
            
            # Move up by layer step
            gcode += f"G1 Z{pass_num * layer_steps:.2f} F{speed}\n"
    
        gcode += f"M2 ; End of program\n"
        return gcode
    

if __name__ == "__main__":
    root = tk.Tk()
    app = GCodeGeneratorApp(root)
    root.mainloop()
