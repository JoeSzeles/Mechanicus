import tkinter as tk
import serial
import keyboard  # Install the 'keyboard' library with pip if you haven't already

# Global variables to keep track of laser state
laser_on = False

def send_gcode(gcode_line):
    # Open serial port
    ser = serial.Serial('COM4', 115200)

    # Write the G-code command to the file (optional)
    with open('gcode_test4.gcode', 'a') as f:
        f.write(gcode_line)

    # Send the G-code command to the laser cutter
    ser.write(gcode_line.encode())

def start_laser():
    global laser_on
    laser_on = True
    send_gcode("M106 S255")  # Turn on laser at full power

def stop_laser():
    global laser_on
    laser_on = False
    send_gcode("M107")  # Turn off laser

def move(direction):
    # Get values from input boxes
    speed = speed_entry.get()
    distance = distance_entry.get()

    # Construct the G-code command for movement
    if direction == "Up":
        gcode_line = f"G1 Y-{distance} F{speed}\n"
    elif direction == "Down":
        gcode_line = f"G1 Y{distance} F{speed}\n"
    elif direction == "Left":
        gcode_line = f"G1 X-{distance} F{speed}\n"
    elif direction == "Right":
        gcode_line = f"G1 X{distance} F{speed}\n"
    else:
        return

    # Send the G-code command
    send_gcode(gcode_line)

def handle_key_event(event):
    global laser_on
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "F12":
            if not laser_on:
                start_laser()
            else:
                stop_laser()
        elif event.event_type == keyboard.KEY_DOWN and event.event_type == keyboard.KEY_UP:
            if event.event_type == keyboard.KEY_DOWN and event.name == "up":
                move("Up")
            elif event.event_type == keyboard.KEY_DOWN and event.name == "down":
                move("Down")
            elif event.event_type == keyboard.KEY_DOWN and event.name == "left":
                move("Left")
            elif event.event_type == keyboard.KEY_DOWN and event.name == "right":
                move("Right")

# Create the tkinter window
root = tk.Tk()
root.title("Laser Cutter Control")

# Create input boxes and labels for variables
speed_label = tk.Label(root, text="Speed:")
speed_label.pack()
speed_entry = tk.Entry(root)
speed_entry.pack()

distance_label = tk.Label(root, text="Distance:")
distance_label.pack()
distance_entry = tk.Entry(root)
distance_entry.pack()

# Create movement buttons
movement_frame = tk.Frame(root)
movement_frame.pack()

up_button = tk.Button(movement_frame, text="Up", command=lambda: move("Up"))
up_button.grid(row=0, column=1)

down_button = tk.Button(movement_frame, text="Down", command=lambda: move("Down"))
down_button.grid(row=2, column=1)

left_button = tk.Button(movement_frame, text="Left", command=lambda: move("Left"))
left_button.grid(row=1, column=0)

right_button = tk.Button(movement_frame, text="Right", command=lambda: move("Right"))
right_button.grid(row=1, column=2)

# Start the tkinter main loop
root.mainloop()

# Register the F12 key press event handler
keyboard.on_press_key("F12", handle_key_event)
keyboard.wait("esc")  # Wait for the 'esc' key to exit the program
