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
    # Send the G-code command directly to the engraver
    ser.write((command + '\n').encode())
    ser.flush()

# Function to toggle the laser state
def toggle_laser():
    global laser_on
    if laser_on:
        send_gcode('M5')  # Turn off the laser
        laser_on = False
    else:
        send_gcode('M3')  # Turn on the laser
        laser_on = True

# Function to send a pulse every 0.1 seconds if the laser is on
def pulse_laser():
    while True:
        if laser_on:
            send_gcode('M3')  # Turn on the laser
            time.sleep(0.01)
            send_gcode('M5')  # Turn off the laser
            time.sleep(0.01)

# Function to set current location to 0,0
def set_location_to_zero():
    send_gcode('G92 X0 Y0')

# Function to home the laser
def home_laser():
    send_gcode('G28')

# Function to draw a 100mm line in the X-axis at 1% power
def draw_test_line():
    send_gcode('G0 X100 Y100 F1000 S10')  # Move to X=100mm at a speed of 1000mm/min
    send_gcode('G1 X0 Y0 F1000')  # Move back to X=0 at the same speed
    send_gcode('M107')  # Turn off the laser

# Create a thread for pulsing the laser
laser_thread = threading.Thread(target=pulse_laser)
laser_thread.daemon = True
laser_thread.start()

try:
    # Create the main application window
    app = tk.Tk()
    app.title("Laser Engraver Calibration")

    # Create buttons for laser control, location reset, homing, and drawing a test line
    toggle_button = tk.Button(app, text="Toggle Laser On/Off", command=toggle_laser)
    reset_button = tk.Button(app, text="Set Location to 0,0", command=set_location_to_zero)
    home_button = tk.Button(app, text="Home Laser", command=home_laser)
    draw_line_button = tk.Button(app, text="Draw Test Line (100mm, 1%)", command=draw_test_line)

    # Pack the buttons into the window
    toggle_button.pack(pady=10)
    reset_button.pack(pady=10)
    home_button.pack(pady=10)
    draw_line_button.pack(pady=10)

    # Run the tkinter main loop
    app.mainloop()

except serial.SerialException:
    print("Failed to establish a serial connection. Check your COM port and settings.")
