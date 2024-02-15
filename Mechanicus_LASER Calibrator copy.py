import serial
import tkinter as tk
import threading
import time

# Define the serial connection
ser = serial.Serial('COM4', 115200)

# Variable to track the laser state
laser_on = False

# Function to send G-code commands to the laser engraver
def send_gcode(command):
    ser.write((command + '\n').encode())
    ser.flush()

# Function to toggle the laser state
def toggle_laser():
    global laser_on
    if laser_on:
        send_gcode('M5')  # Turn off the laser
    else:
        send_gcode('M3')  # Turn on the laser
    laser_on = not laser_on  # Toggle the laser state

# Function to set current location to 0,0
def set_location_to_zero():
    send_gcode('G92 X0 Y0')

# Function to home the laser
def home_laser():
    send_gcode('G28')

try:
    # Create the main application window
    app = tk.Tk()
    app.title("Laser Engraver Calibration")

    # Create buttons for laser control, location reset, and homing
    toggle_button = tk.Button(app, text="Toggle Laser On/Off", command=toggle_laser)
    reset_button = tk.Button(app, text="Set Location to 0,0", command=set_location_to_zero)
    home_button = tk.Button(app, text="Home Laser", command=home_laser)

    # Pack the buttons into the window
    toggle_button.pack(pady=10)
    reset_button.pack(pady=10)
    home_button.pack(pady=10)

    # Run the tkinter main loop
    app.mainloop()

except serial.SerialException:
    print("Failed to establish a serial connection. Check your COM port and settings.")
