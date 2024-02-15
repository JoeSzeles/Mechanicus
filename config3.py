#!/usr/bin/env python
#config.py
import tkinter as tk
from tkinter import ttk
from tkinter import END
"""G-code emitted at the start of processing the SVG file"""
preamble = "G1 Z60"
"""G-code emitted at the end of processing the SVG file"""
postamble = "(postamble)"
"""G-code emitted before processing a SVG shape"""
shape_preamble = "G1 Z60"
#shape_preamble = "Z0"
"""G-code emitted after processing a SVG shape"""
shape_postamble = "G1 Z60"
#shape_postamble = "Z100)"
""" scale gcode to fit bed size"""
auto_scale = False
""" optimize path - slow for large files"""
optimise = True
"""
illustrator exports svg's in points, not mm
set to "mm" if you don't want to convert to mm
"""
Serial_connection= 'COM3'
Baud = 115200
coordinates='absolute'
units = "points"
line_speed = 50
curve_speed = 40
draw_speed = 40
travel_speed = 3000
draw_height = 21
travel_height = 26
smoothness = 0.2
connect_tolerance = 0.001
laser_power = 1000
layer_height = 0.15
print_accel = 30
travel_accel = 200
max_jerk = 200
layers = 1
scaleF = 1
x_offset = 0
y_offset = 0
bed_max_x = 410
bed_max_y = 840
refill_pos = 150,10,20
zTravel = 20.5
zDraw = 17
zLift = 20.5
feed_rate = 30
zrefill=20
refill_lenght= 200
Refill = False
zColor=18
z_start= 19
z_center=15
z_end=19
gradient_length_mm=8 #mm
#material_thickness = 19
