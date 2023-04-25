import tkinter as tk
import config


class ConfigWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuration")
        self.config = config
        self.create_widgets()

    def create_widgets(self):
        row = 0

        # line_speed
        tk.Label(self, text="Line Speed (mm/s)").grid(row=row, column=0)
        self.line_speed_var = tk.StringVar(value=self.config.line_speed)
        tk.Entry(self, textvariable=self.line_speed_var).grid(row=row, column=1)
        row += 1

        # curve_speed
        tk.Label(self, text="Curve Speed (mm/s)").grid(row=row, column=0)
        self.curve_speed_var = tk.StringVar(value=self.config.curve_speed)
        tk.Entry(self, textvariable=self.curve_speed_var).grid(row=row, column=1)
        row += 1

        # draw_speed
        tk.Label(self, text="Draw Speed (mm/s)").grid(row=row, column=0)
        self.draw_speed_var = tk.StringVar(value=self.config.draw_speed)
        tk.Entry(self, textvariable=self.draw_speed_var).grid(row=row, column=1)
        row += 1

        # travel_speed
        tk.Label(self, text="Travel Speed (mm/s)").grid(row=row, column=0)
        self.travel_speed_var = tk.StringVar(value=self.config.travel_speed)
        tk.Entry(self, textvariable=self.travel_speed_var).grid(row=row, column=1)
        row += 1

        # draw_height
        tk.Label(self, text="Draw Height (mm)").grid(row=row, column=0)
        self.draw_height_var = tk.StringVar(value=self.config.draw_height)
        tk.Entry(self, textvariable=self.draw_height_var).grid(row=row, column=1)
        row += 1

        # travel_height
        tk.Label(self, text="Travel Height (mm)").grid(row=row, column=0)
        self.travel_height_var = tk.StringVar(value=self.config.travel_height)
        tk.Entry(self, textvariable=self.travel_height_var).grid(row=row, column=1)
        row += 1

        # smoothness
        tk.Label(self, text="Smoothness (mm)").grid(row=row, column=0)
        self.smoothness_var = tk.StringVar(value=self.config.smoothness)
        tk.Entry(self, textvariable=self.smoothness_var).grid(row=row, column=1)
        row += 1

        # connect_tolerance
        tk.Label(self, text="Connect Tolerance (mm)").grid(row=row, column=0)
        self.connect_tolerance_var = tk.StringVar(value=self.config.connect_tolerance)
        tk.Entry(self, textvariable=self.connect_tolerance_var).grid(row=row, column=1)
        row += 1

        # laser_power
        tk.Label(self, text="Laser Power (%)").grid(row=row, column=0)
        self.laser_power_var = tk.StringVar(value=self.config.laser_power)
        tk.Entry(self, textvariable=self.laser_power_var).grid(row=row, column=1)
        row += 1

        # layer_height
        tk.Label(self, text="Layer Height (mm)").grid(row=row, column=0)
        self.layer_height_var = tk.StringVar(value=self.config.layer_height)
        tk.Entry(self, textvariable=self.layer_height_var).grid(row=row, column=1)
        row += 1

        # filament_diameter
        tk.Label(self, text="Filament Diameter (mm)").grid(row=row, column=0)
        self.filament_diameter_var = tk.StringVar(value=self.config.filament_diameter)
        tk.Entry(self, textvariable=self.filament_diameter_var).grid(row=row, column=1)
        row += 1

        # bed_temp
        tk.Label(self, text="Bed Temperature (°C)").grid(row=row, column=0)
        self.bed_temp_var = tk.StringVar(value=self.config.bed_temp)
        tk.Entry(self, textvariable=self.bed_temp_var).grid(row=row, column=1)
        row += 1

        # extruder_temp
        tk.Label(self, text="Extruder Temperature (°C)").grid(row=row, column=0)
        self.extruder_temp_var = tk.StringVar(value=self.config.extruder_temp)
        tk.Entry(self, textvariable=self.extruder_temp_var).grid(row=row, column=1)
        row += 1

        # fan_speed
        tk.Label(self, text="Fan Speed (%)").grid(row=row, column=0)
        self.fan_speed_var = tk.StringVar(value=self.config.fan_speed)
        tk.Entry(self, textvariable=self.fan_speed_var).grid(row=row, column=1)
        row += 1

        # nozzle_size
        tk.Label(self, text="Nozzle Size (mm)").grid(row=row, column=0)
        self.nozzle_size_var = tk.StringVar(value=self.config.nozzle_size)
        tk.Entry(self, textvariable=self.nozzle_size_var).grid(row=row, column=1)
        row += 1

        # button to save changes
        tk.Button(self, text="Save", command=self.save_config).grid(row=row, column=0, columnspan=2)

    def save_config(self):
        # update values in config module with new values from the GUI
        self.config.line_speed = float(self.line_speed_var.get())
        self.config.curve_speed = float(self.curve_speed_var.get())
        self.config.draw_speed = float(self.draw_speed_var.get())
        self.config.travel_speed = float(self.travel_speed_var.get())
        self.config.draw_height = float(self.draw_height_var.get())
        self.config.travel_height = float(self.travel_height_var.get())
        self.config.smoothness = float(self.smoothness_var.get())
        self.config.connect_tolerance = float(self.connect_tolerance_var.get())
        self.config.laser_power = float(self.laser_power_var.get())
        self.config.layer_height = float(self.layer_height_var.get())
        self.config.filament_diameter = float(self.filament_diameter_var.get())
        self.config.bed_temp = int(self.bed_temp_var.get())
        self.config.extruder_temp = int(self.extruder_temp_var.get())
        self.config.fan_speed = int(self.fan_speed_var.get())
        self.config.nozzle_size = float(self.nozzle_size_var.get())

        # save changes to config file
        self.config.save_config()

        # close window
        self.destroy()
