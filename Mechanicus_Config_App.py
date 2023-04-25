import csv
import tkinter as tk
from tkinter import ttk
from tkinter import END
import inspect
####CONFIG WINDOW##############################################################

def Config():
    
    configwin = tk.Toplevel(height=0 , width=0, bg="#263d42",cursor="circle", borderwidth=0)
    configwin.title("MECHANICUS_V.0.1 Beta. (c)Reservoir Frogs 2022")
    configwin.configure(bg="#263d42", borderwidth=0)
    configwin.geometry("300x800+1200+100")
    
    ######### CONFIG INPUT VARIABLES ############################
    
    line_speed1 = tk.Text(configwin, height=1, width=5)
    line_speed1.insert(END, '8000')  # in mm/s
    line_speed1.grid(row=0, column=1)
    
    curve_speed1 = tk.Text(configwin, height=1, width=5)
    curve_speed1.insert(END, '5000')  # in mm/s
    curve_speed1.grid(row=1, column=1)
    
    draw_speed1 = tk.Text(configwin, height=1, width=5)
    draw_speed1.insert(END, '8000')  # in mm/s
    draw_speed1.grid(row=2, column=1)
    
    travel_speed1 = tk.Text(configwin, height=1, width=5)
    travel_speed1.insert(END, '8000')  # in mm/s
    travel_speed1.grid(row=3, column=1)
    
    draw_height1 = tk.Text(configwin, height=1, width=5)
    draw_height1.insert(END, '1.0')  # in mm
    draw_height1.grid(row=4, column=1)
    
    travel_height1 = tk.Text(configwin, height=1, width=5)
    travel_height1.insert(END, '1.8')  # in mm
    travel_height1.grid(row=5, column=1)
    
    smoothness1 = tk.Text(configwin, height=1, width=5)
    smoothness1.insert(END, '0.3')  # in mm
    smoothness1.grid(row=6, column=1)
    
    connect_tolerance1 = tk.Text(configwin, height=1, width=5)
    connect_tolerance1.insert(END, '0.1')  # in mm
    connect_tolerance1.grid(row=7, column=1)
    
    laser_power1 = tk.Text(configwin, height=1, width=5)
    laser_power1.insert(END, '255')  # max value
    laser_power1.grid(row=8, column=1)
    
    layer_height1 = tk.Text(configwin, height=1, width=5)
    layer_height1.insert(END, '0.3')  # in mm
    layer_height1.grid(row=9, column=1)
    
    print_accel1 = tk.Text(configwin, height=1, width=5)
    print_accel1.insert(END, '8000')  # in mm
    print_accel1.grid(row=10, column=1)
    
    travel_accel1 = tk.Text(configwin, height=1, width=5)
    travel_accel1.insert(END, '8000')  # in mm
    travel_accel1.grid(row=11, column=1)
    
    max_jerk1 = tk.Text(configwin, height=1, width=5)
    max_jerk1.insert(END, '8000')  # in mm/s
    max_jerk1.grid(row=12, column=1)
    
    layers1 = tk.Text(configwin, height=1, width=5)
    layers1.insert(END, '1')  # in mm/s
    layers1.grid(row=13, column=1)
    
    scaleF1 = tk.Text(configwin, height=1, width=5)
    scaleF1.insert(END, '0.8')  # in mm/s
    scaleF1.grid(row=14, column=1)
    
    x_offset1 = tk.Text(configwin,height=1, width=5)
    x_offset1.insert(END, '30')  # in mm/s
    x_offset1.grid(row=15, column=1)
    
    y_offset1 = tk.Text(configwin,height=1, width=5)
    y_offset1.insert(END, '30')  # in mm/s
    y_offset1.grid(row=16, column=1)
    
    bed_max_x1= tk.Text(configwin,height =1,width = 5) # in mm/s
    bed_max_x1.insert(END, '300')# in mm
    bed_max_x1.grid(row=17, column=1)
    
    bed_max_y1= tk.Text(configwin,height =1,width = 5) # in mm/s
    bed_max_y1.insert(END, '300')# in mm
    bed_max_y1.grid(row=18, column=1)
    
    refill_pos1= tk.Text(configwin,height =1,width = 5) # in mm/s
    refill_pos1.insert(END, '40,100,20')# in mm
    refill_pos1.grid(row=19, column=1)
    
    
    zTravel1= tk.Text(configwin,height =1,width = 5) # in mm/s
    zTravel1.insert(END, '1.2')# in mm
    zTravel1.grid(row=20, column=1)
    
    zDraw1= tk.Text(configwin,height =1,width = 5) # in mm/s
    zDraw1.insert(END, '0.5')# in mm
    zDraw1.grid(row=21, column=1)
    
    zLift1= tk.Text(configwin,height =1,width = 5) # in mm/s
    zLift1.insert(END, '0.8')# in mm
    zLift1.grid(row=22, column=1)
    
    feed_rate1= tk.Text(configwin,height =1,width = 5) # in mm/s
    feed_rate1.insert(END, '8000')# in mm
    feed_rate1.grid(row=23, column=1)
    
    zrefill1= tk.Text(configwin,height =1,width = 5) # in mm/s
    zrefill1.insert(END, '1.0')# in mm
    zrefill1.grid(row=24, column=1)
    
    # Create labels and text boxes for each variable
    tk.Label(configwin, text="Line speed (mm/s):").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Curve speed (mm/s):").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Draw speed (mm/s):").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Travel speed (mm/s):").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Draw height (mm):").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Travel height (mm):").grid(row=5, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Smoothness (mm):").grid(row=6, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Connect tolerance (mm):").grid(row=7, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Laser power (%):").grid(row=8, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Layer height (mm):").grid(row=9, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Print acceleration (mm/s²):").grid(row=10, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Travel acceleration (mm/s²):").grid(row=11, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Max jerk (mm/s):").grid(row=12, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Number of layers:").grid(row=13, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Scale factor:").grid(row=14, column=0, padx=5, pady=5)
    tk.Label(configwin, text="X offset:").grid(row=15, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Y offset:").grid(row=16, column=0, padx=5, pady=5)
    tk.Label(configwin, text="bed_max_x (mm):").grid(row=17, column=0, padx=5, pady=5)
    tk.Label(configwin, text="bed_max_y (mm):").grid(row=18, column=0, padx=5, pady=5)
    tk.Label(configwin, text="refill position(x,y)").grid(row=29, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Travel height (mm):").grid(row=20, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Draw height (mm)").grid(row=21, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Lift height(mm)").grid(row=22, column=0, padx=5, pady=5)
    tk.Label(configwin, text="Speed").grid(row=23, column=23, padx=5, pady=5)
    tk.Label(configwin, text="Refill height (mm):").grid(row=24, column=0, padx=5, pady=5)
    
    
    def save_config():
    
        file_path = 'config3.py'
        # Get the values from the GUI inputs
        line_speed = line_speed1.get('1.0', 'end-1c')
        curve_speed = curve_speed1.get('1.0', 'end-1c')
        draw_speed = draw_speed1.get('1.0', 'end-1c')
        travel_speed = travel_speed1.get('1.0', 'end-1c')
        draw_height = draw_height1.get('1.0', 'end-1c')
        travel_height = travel_height1.get('1.0', 'end-1c')
        smoothness = smoothness1.get('1.0', 'end-1c')
        connect_tolerance = connect_tolerance1.get('1.0', 'end-1c')
        laser_power = laser_power1.get('1.0', 'end-1c')
        layer_height = layer_height1.get('1.0', 'end-1c')
        print_accel = print_accel1.get('1.0', 'end-1c')
        travel_accel = travel_accel1.get('1.0', 'end-1c')
        max_jerk = max_jerk1.get('1.0', 'end-1c')
        layers = layers1.get('1.0', 'end-1c')
        scaleF = scaleF1.get('1.0', 'end-1c')
        x_offset = x_offset1.get('1.0', 'end-1c')
        y_offset = y_offset1.get('1.0', 'end-1c')
        bed_max_x = bed_max_x1.get('1.0', 'end-1c')
        bed_max_y = bed_max_y1.get('1.0', 'end-1c')
        refill_pos = refill_pos1.get('1.0', 'end-1c')
        zTravel = zTravel1.get('1.0', 'end-1c')
        zDraw = zDraw1.get('1.0', 'end-1c')
        zLift = zLift1.get('1.0', 'end-1c')
        feed_rate = feed_rate1.get('1.0', 'end-1c')
        
        # Create a list of tuples containing the header and value for each variable
        variables = [
        ('line_speed', line_speed),
        ('curve_speed', curve_speed),
        ('draw_speed', draw_speed),
        ('travel_speed', travel_speed),
        ('draw_height', draw_height),
        ('travel_height', travel_height),
        ('smoothness', smoothness),
        ('connect_tolerance', connect_tolerance),
        ('laser_power', laser_power),
        ('layer_height', layer_height),
        ('print_accel', print_accel),
        ('travel_accel', travel_accel),
        ('max_jerk', max_jerk),
        ('layers', layers),
        ('scaleF', scaleF),
        ('x_offset', x_offset),
        ('y_offset', y_offset),
        ('bed_max_x', bed_max_x),
        ('bed_max_y', bed_max_y),
        ('refill_pos', refill_pos),
        ('zTravel', zTravel),
        ('zDraw', zDraw),
        ('zLift', zLift),
        ('feed_rate', feed_rate)
        ]
        # Open the file and write the code
        with open(file_path, 'w') as f:
            f.write('#!/usr/bin/env python\n')
            f.write('#config.py\n')
            f.write('import tkinter as tk\n')
            f.write('from tkinter import ttk\n')
            f.write('from tkinter import END\n')
            f.write('"""G-code emitted at the start of processing the SVG file"""\n')
            f.write('preamble = "G90"\n')
            f.write('"""G-code emitted at the end of processing the SVG file"""\n')
            f.write('postamble = "(postamble)"\n')
            f.write('"""G-code emitted before processing a SVG shape"""\n')
            f.write('shape_preamble = "G1 Z0.4"\n')
            f.write('#shape_preamble = "Z0"\n')
            f.write('"""G-code emitted after processing a SVG shape"""\n')
            f.write('shape_postamble = "G1 0.4"\n')
            f.write('#shape_postamble = "Z100)"\n')
            f.write('""" scale gcode to fit bed size"""\n')
            f.write('auto_scale = False\n')
            f.write('""" optimize path - slow for large files"""\n')
            f.write('optimise = True\n')
            f.write('"""\n')
            f.write("illustrator exports svg's in points, not mm\n")
            f.write('set to "mm" if you don\'t want to convert to mm\n')
            f.write('"""\n')
            f.write('units = "points"\n')
    
            # Write the variables
            for variable_name, variable_value in variables:
                f.write(f"{variable_name} = {variable_value}\n")
                
    save_button = tk.Button(configwin, text="Save", command=save_config)
    save_button.grid(row=25, column=3) 
    
    configwin.mainloop()
Config()
    
 
    
    