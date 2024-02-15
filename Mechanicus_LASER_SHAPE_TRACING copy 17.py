import cv2
import numpy as np
import serial
from PIL import Image, ImageTk
import tkinter as tk
import time

# Initialize default values
video_width, video_height = 480, 480
cnc_width, cnc_height = 400, 400  # in millimeters
serial_port = 'COM4'

# Initialize variables
video_center_x = video_width // 2
video_center_y = video_height // 2
cnc_center_x = cnc_width // 2
cnc_center_y = cnc_height // 2

# Initialize the current CNC position at the bottom left corner (0, 0)
current_x = 0
current_y = 0

# Function to set the current position to 0,0
def set_current_position_to_zero():
    global current_x, current_y
    current_x = 0
    current_y = 0
    send_gcode("G0 X0 Y0")

# Function to activate the laser
def activate_laser():
    send_gcode("M3 S15")

# Function to turn off the laser
def turn_off_laser():
    send_gcode("M5 S0")

# Function to home the CNC machine
def home():
    send_gcode("G28")

# Function to move the CNC to the center
def go_to_center():
    send_gcode(f'G0 X{cnc_center_x} Y{cnc_center_y}')

# Function to send G-code commands to control the CNC
def send_gcode(gcode_line):
    try:
        ser = serial.Serial(serial_port, 115200)
        ser.write((gcode_line + "\n").encode())
        ser.close()
    except serial.SerialException as e:
        print(f"Serial Error: {e}")

# Function to move the CNC to a specific position
def move_to_position(x, y):
    global current_x, current_y
    x = max(0, min(x, cnc_width))
    y = max(0, min(y, cnc_height))
    gcode_line = f"G0 X{x} Y{y}"
    send_gcode(gcode_line)
    print(gcode_line)
    current_x = x
    current_y = y

# Function to process the video frame and detect the green object
def process_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None, None, None

    lower_green = np.array([35, 70, 70])
    upper_green = np.array([90, 255, 255])

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            green_x = int(moments["m10"] / moments["m00"])
            green_y = int(moments["m01"] / moments["m00"])
            return frame, green_x, green_y
        else:
            turn_off_laser()
    return frame, None, None

# Updated tracker function
def tracker():
    # Open the webcam
    cap = cv2.VideoCapture(1)

    while True:
        frame, green_x, green_y = process_frame(cap)
        if frame is None:
            break

        if green_x is not None and green_y is not None:
            # Calculate the vector from the center of the video feed to the green point
            vector_x = green_x - video_center_x
            vector_y = green_y - video_center_y

            # Calculate the CNC position based on the vector
            new_x = current_x + vector_x
            new_y = current_y - vector_y  # Invert Y-axis for CNC

            # Ensure the new position is within the CNC bed limits
            new_x = max(0, min(new_x, cnc_width))
            new_y = max(0, min(new_y, cnc_height))

            # Move the CNC to the new position
            move_to_position(new_x, new_y)

        frame = frame[:video_width, :video_height]

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        label.config(image=img_tk)
        label.image = img_tk

        root.update()
        time.sleep(0.1)

    cap.release()
    root.destroy()

# Entry point
if __name__ == "__main__":
    # Create the tkinter app
    root = tk.Tk()
    root.title("CNC Control App")

    # Create input fields for dimensions and serial port
    tk.Label(root, text="Video Width:").grid(row=0, column=0)
    video_width_entry = tk.Entry(root)
    video_width_entry.insert(0, str(video_width))
    video_width_entry.grid(row=0, column=1)

    tk.Label(root, text="Video Height:").grid(row=1, column=0)
    video_height_entry = tk.Entry(root)
    video_height_entry.insert(0, str(video_height))
    video_height_entry.grid(row=1, column=1)

    tk.Label(root, text="CNC Width (mm):").grid(row=2, column=0)
    cnc_width_entry = tk.Entry(root)
    cnc_width_entry.insert(0, str(cnc_width))
    cnc_width_entry.grid(row=2, column=1)

    tk.Label(root, text="CNC Height (mm):").grid(row=3, column=0)
    cnc_height_entry = tk.Entry(root)
    cnc_height_entry.insert(0, str(cnc_height))
    cnc_height_entry.grid(row=3, column=1)

    tk.Label(root, text="Serial Port:").grid(row=4, column=0)
    serial_port_entry = tk.Entry(root)
    serial_port_entry.insert(0, serial_port)
    serial_port_entry.grid(row=4, column=1)

    # Create buttons to trigger CNC functions
    tk.Button(root, text="Set Current Position to (0, 0)", command=set_current_position_to_zero).grid(row=5, column=0, columnspan=2)
    tk.Button(root, text="Home CNC", command=home).grid(row=6, column=0, columnspan=2)
    tk.Button(root, text="Go to Center", command=go_to_center).grid(row=7, column=0, columnspan=2)

    label = tk.Label(root)
    label.grid(row=8, column=0, columnspan=2)

    tracker()  # Start the tracker function

    # Main loop
    root.mainloop()
