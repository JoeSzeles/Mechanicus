#!/usr/bin/env python
#config.py
import tkinter as tk
from tkinter import ttk
from tkinter import END
"""G-code emitted at the start of processing the SVG file"""
preamble = "G90"
"""G-code emitted at the end of processing the SVG file"""
postamble = "(postamble)"
"""G-code emitted before processing a SVG shape"""
shape_preamble = "G1 Z0.4"
#shape_preamble = "Z0"
"""G-code emitted after processing a SVG shape"""
shape_postamble = "G1 0.4"
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








######## CONFIG WINDOW END   ###################################################