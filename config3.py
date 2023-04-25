#!/usr/bin/env python
#config.py
import tkinter as tk
from tkinter import ttk
from tkinter import END
"""G-code emitted at the start of processing the SVG file"""
preamble = "G1 Z10"
"""G-code emitted at the end of processing the SVG file"""
postamble = "(postamble)"
"""G-code emitted before processing a SVG shape"""
shape_preamble = "G1 Z10"
#shape_preamble = "Z0"
"""G-code emitted after processing a SVG shape"""
shape_postamble = "G1 Z10"
#shape_postamble = "Z100)"
""" scale gcode to fit bed size"""
auto_scale = False
""" optimize path - slow for large files"""
optimise = True
"""
illustrator exports svg's in points, not mm
set to "mm" if you don't want to convert to mm
"""
units = "points"
line_speed = 2000
curve_speed = 2000
draw_speed = 2000
travel_speed = 2000
draw_height = 0.1
travel_height = 1
smoothness = 0.02
connect_tolerance = 0.001
laser_power = 255
layer_height = 0.15
print_accel = 2000
travel_accel = 2000
max_jerk = 2000
layers = 1
scaleF = 1
x_offset = 1
y_offset = 0
bed_max_x = 300
bed_max_y = 300
refill_pos = 150,10,20
zTravel = 0.6
zDraw = 0.1
zLift = 0.4
feed_rate = 2000
zrefill=15
refill_lenght= 200
Refill = False
zColor=1.2
