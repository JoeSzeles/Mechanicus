import cv2
import numpy as np
import serial
from PIL import Image, ImageTk
import tkinter as tk
import time

# Global variables to keep track of laser state and target position
laser_on = False
target_x = None
target_y = None

# Function to send G-code commands to control the CNC
def send_gcode(gcode_line):
    # Open serial port
    ser = serial.Serial('COM4', 115200)

    # Send the G-code command to the CNC
    ser.write(gcode_line.encode())

# Function to start the laser
def start_laser():
    global laser_on
    laser_on = True
    send_gcode("M106 S255")  # Turn on laser at full power

# Function to stop the laser
def stop_laser():
    global laser_on
    laser_on = False
    send_gcode("M107")  # Turn off laser

# Function to move the CNC to a specific position
def move_to_position(x, y, speed):
    # Construct the G-code command for movement
    gcode_line = f"G1 X{x} Y{y} F{speed}\n"
    # Send the G-code command
    send_gcode(gcode_line)

def tracer():
    WINDOW = "1280x960"
    # Create a window with a label for showing the image
    root = tk.Tk()
    root.geometry(WINDOW)  # Set the window size to 1280x960
    label = tk.Label(root)
    label.pack()

    # Open the webcam
    # Capture a frame from the webcam
    cap = cv2.VideoCapture(1)
    
    while True:
        frame = process_frame(cap)
        if frame is None:
            break

        # Convert the frame to a PIL Image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # Convert the resized image to a Tkinter-compatible format
        img_tk = ImageTk.PhotoImage(image=img)
        # Update the label with the resized image
        label.config(image=img_tk)
        label.image = img_tk
        
        # Wait for 0.01 seconds before updating again
        root.update()
        time.sleep(0.01)

def process_frame(cap):
    global target_x, target_y

    ret, frame = cap.read()
    if not ret:
        return None

    # Define the color range for detecting the green point
    lower_green = np.array([35, 70, 70])
    upper_green = np.array([90, 255, 255])

    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to isolate the green point
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest green contour (assuming it's the target point)
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            # Calculate the center of the green point
            target_x = int(moments["m10"] / moments["m00"])
            target_y = int(moments["m01"] / moments["m00"])

            # If the green point is detected, set the shape_detected flag to True

            # Overlay the detected green point on the frame
            cv2.circle(frame, (target_x, target_y), 5, (255, 0, 0), -1)  # Overlay circle in blue

            # Calculate the difference between the current position and the target position
            if target_x is not None and target_y is not None:
                # Calculate the new position
                new_x = target_x
                new_y = target_y

                # Constrain the new position within the 20 x 13 cm area
                new_x = max(0, min(new_x, 20))
                new_y = max(0, min(new_y, 13))

                # Calculate the distance to the new position
                diff_x = new_x - current_x
                diff_y = new_y - current_y

                # Set the movement speed based on the distance
                speed = 5000

                # Move the CNC towards the new position
                move_to_position(new_x, new_y, speed=speed)

    else:
        # If the green point is not detected and the shape was previously detected, stop the laser
        if target_x is not None and target_y is not None:
            stop_laser()

    return frame

# Initialize the current position to a starting point (adjust as needed)
current_x = 0
current_y = 0

time.sleep(0.01)
tracer()
