import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class CNCMillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Milling App")
        
        self.create_ui()
        
        self.absolute_mode = False
        self.tool_diameter = 3.0
        self.milling_speed  = 500  # Default milling speed in mm/min
        self.hole_depth = 10.0  # Default hole depth in mm
        self.layer_height = 1.0  # Default layer height in mm

    def create_ui(self):
        
        self.center_label = ttk.Label(self.root, text="Center Point (X, Y, Z):")
        self.center_entry = ttk.Entry(self.root)

        self.center_label.pack(pady=5)
        self.center_entry.pack(pady=5)
        
        self.dimensions_label = ttk.Label(self.root, text="Rectangle Dimensions (X, Y):")
        self.dimensions_entry = ttk.Entry(self.root)
        self.tool_diameter_label = ttk.Label(self.root, text="Tool Diameter:")
        self.tool_diameter_entry = ttk.Entry(self.root)
        self.speed_label = ttk.Label(self.root, text="Milling Speed:")
        self.speed_entry = ttk.Entry(self.root)
        self.depth_label = ttk.Label(self.root, text="Hole Depth:")
        self.depth_entry = ttk.Entry(self.root)
        self.layer_height_label = ttk.Label(self.root, text="Layer Height:")
        self.layer_height_entry = ttk.Entry(self.root)
        self.absolute_mode_var = tk.BooleanVar(value=False)
        self.absolute_mode_checkbox = ttk.Checkbutton(self.root, text="Absolute Mode",
                                                      variable=self.absolute_mode_var)
        self.generate_button = ttk.Button(self.root, text="Generate G-code", command=self.generate_gcode)

        self.dimensions_label.pack(pady=5)
        self.dimensions_entry.pack(pady=5)
        self.tool_diameter_label.pack(pady=5)
        self.tool_diameter_entry.pack(pady=5)
        self.speed_label.pack(pady=5)
        self.speed_entry.pack(pady=5)
        self.depth_label.pack(pady=5)
        self.depth_entry.pack(pady=5)
        self.layer_height_label.pack(pady=5)
        self.layer_height_entry.pack(pady=5)
        self.absolute_mode_checkbox.pack(pady=5)
        self.generate_button.pack(pady=10)

    def generate_gcode(self):
        gcode = []  # Initialize an empty list to store G-code lines
        
        # Convert input values to appropriate types
        self.center_point = self.center_entry.get().split(",")
        if len(self.center_point) != 3:
            messagebox.showerror("Error", "Invalid center point format")
            return
        try:
            self.center_x = float(self.center_point[0].strip())
            self.center_y = float(self.center_point[1].strip())
            self.center_z = float(self.center_point[2].strip())
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid center point input: {e}")
            return
        
        # Calculate the boundary coordinates of the rectangle
        self.rect_width = float(self.dimensions_entry.get().split(",")[0].strip())
        try:
            dimensions_parts = self.dimensions_entry.get().split(",")
            if len(dimensions_parts) >= 2:
                self.rect_height = float(dimensions_parts[1].strip())
            else:
                raise ValueError("Invalid dimensions input format")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid dimensions input: {e}")
            return
        
        self.x_start = self.center_x - self.rect_width / 2
        self.x_min = self.x_start
        self.x_max = self.center_x + self.rect_width / 2
        self.y_start = self.center_y - self.rect_height / 2
        self.y_min = self.y_start
        self.y_max = self.center_y + self.rect_height / 2
        
        # Set the Z position for the first layer to the user-specified Z coordinate
        z_position = self.center_z
        z_start = self.center_z + 10
        z_end = self.center_z + 15
        gcode.append(f"G0 Z{z_start}")
        
        Hole_depth=float(self.depth_entry.get())
        Tool_widh=float(self.tool_diameter_entry.get())
        layer_height = float(self.layer_height_entry.get())
        Layer_count= int(Hole_depth / layer_height)
        Milling_speed=float(self.speed_entry.get())
        
        # Generate G-code for each layer
        for layer in range(0,Layer_count ):
            
            if layer == 0:
                z_position = self.center_z
            else:
                
            
                z_position = z_position - layer_height #Layer moving down Layer

            # Insert a comment line indicating the layer number
            gcode.append(f";LAYER: {layer}")
            # Move to the starting position of the layer
            #gcode.append(f"G0 Z{z_position:.2f}")
    
            # Move the tool to the adjusted starting position
            gcode.append(f"G0 X{self.x_start:.2f} Y{self.y_start:.2f} Z{z_position:.2f}")
    
            # Generate the outline of the rectangle
            gcode.append(f"G1 X{self.x_min:.2f} Y{self.y_min:.2f} F{Milling_speed }")
            gcode.append(f"G1 X{self.x_max:.2f} Y{self.y_min:.2f} F{Milling_speed }")
            gcode.append(f"G1 X{self.x_max:.2f} Y{self.y_max:.2f} F{Milling_speed }")
            gcode.append(f"G1 X{self.x_min:.2f} Y{self.y_max:.2f} F{Milling_speed }")
            gcode.append(f"G1 X{self.x_min:.2f} Y{self.y_min:.2f} F{Milling_speed }")
    
            # Generate the milling path within the rectangle
            y_position = self.y_min  # Start from the bottom of the rectangle
            while y_position <= self.y_max:
                gcode.append(f"G0 X{self.x_max:.2f} Y{y_position:.2f}")
                gcode.append(f"G1 X{self.x_min:.2f} Y{y_position:.2f} F{Milling_speed }")
                y_position += Tool_widh
            
        gcode.append(f"G0 Z{z_end}")  ###move up the finished
        gcode.append(f";End of Gcode")
        # Save the generated G-code to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("G-code Files", "*.gcode")])
        if file_path:
            with open(file_path, 'w') as f:
                for line in gcode:
                    f.write(line + "\n")
                messagebox.showinfo("Success", "G-code generated and saved successfully!")
    
    
    
   
   
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    root = tk.Tk()
    app = CNCMillingApp(root)
    root.mainloop()
