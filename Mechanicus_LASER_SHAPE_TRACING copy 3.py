import cv2
import numpy as np
import serial
from PIL import Image, ImageTk
import tkinter as tk
import time

# Function to send G-code commands to control the CNC
def send_gcode(gcode_line):
    # Open serial port
    ser = serial.Serial('COM4', 115200)

    # Send the G-code command to the CNC
    ser.write(gcode_line.encode())

# Function to move the CNC to a specific position
def move_to_position(x, y, speed):
    # Limit movement within the 200 x 130 mm area
    x = max(0, min(x, 200))
    y = max(0, min(y, 130))
    
    # Construct the G-code command for movement
    gcode_line = f"G1 X{x} Y{y} F{speed}\n"
    
    # Send the G-code command
    send_gcode(gcode_line)

def tracer():
    WINDOW = "640x480"
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
        
        # Wait for 0.2 seconds before updating again
        root.update()
        time.sleep(0.2)

def process_frame(cap):
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
            
            # Overlay the detected green point on the frame
            cv2.circle(frame, (target_x, target_y), 15, (255, 0, 0), -1)  # Overlay circle in blue

            # Move the CNC to the new position (directly set the position)
            move_to_position(target_x, target_y, speed=9000)

    return frame

time.sleep(0.5)
tracer()
