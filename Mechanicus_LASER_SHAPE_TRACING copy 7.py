import cv2
import numpy as np
import serial
from PIL import Image, ImageTk
import tkinter as tk
import time

# Define the dimensions of the video feed and CNC workspace
video_width, video_height = 480, 480
cnc_width, cnc_height = 400, 400  # in millimeters
# Function to set the current position to 0,0
# Function to home the CNC machine
def home():
    gcode_line = "G28"
    send_gcode(gcode_line)

def set_current_position_to_zero():
    gcode_line = "G92 X0 Y0"
    send_gcode(gcode_line)
def go_to_center():
    gcode_line = "G0 X200 Y200"
    send_gcode(gcode_line)
# Function to scale the video coordinates to CNC coordinates
def scale_coordinates(x, y):
    # Calculate the scaling factors
    x_scale = cnc_width / video_width
    y_scale = cnc_height / video_height

    # Apply scaling to the coordinates
    scaled_x = x * x_scale
    scaled_y = y * y_scale

    return scaled_x, scaled_y

# Initialize a list to store G-code commands in the buffer
gcode_buffer = []

# Function to send G-code commands to control the CNC
def send_gcode(gcode_line):
    # Open serial port
    ser = serial.Serial('COM4', 115200)

    # Send the G-code command to the CNC
    ser.write(gcode_line.encode())

# Function to move the CNC to a specific position
def move_to_position(x, y, speed):
    # Limit movement within the 400 x 400 mm area
    x = max(0, min(x, 400))
    y = max(0, min(y, 400))
    
    # Construct the G-code command for movement
    gcode_line = f"G1 X{x} Y{y} F{speed}\n"
    
    # Add the G-code command to the buffer
    gcode_buffer.append(gcode_line)

    # Check if the buffer has reached the maximum size (5)
    if len(gcode_buffer) >= 1:
        # Send the buffered commands and wait for confirmation
        for cmd in gcode_buffer:
            send_gcode(cmd)
            # Add logic here to wait for confirmation (e.g., feedback from CNC)
            # You can use serial communication to receive confirmation
            # Once confirmed, remove the command from the buffer
        gcode_buffer.clear()  # Clear the buffer after sending

def tracer():
    WINDOW = "480x480"
    # Open the webcam
    # Capture a frame from the webcam
    cap = cv2.VideoCapture(1)
    # Function to home the CNC machine

    root = tk.Tk()
    root.geometry(WINDOW)  # Set the window size to 480x480
    label = tk.Label(root)
    label.pack()

    # Initialize the blue point (centered) coordinates
    center_x = video_width // 2
    center_y = video_height // 2
    home()
    go_to_center()
    while True:
        frame, green_x, green_y = process_frame(cap)
        if frame is None:
            break

        if green_x is not None and green_y is not None:
            # Calculate the required motion to follow the green point
            dx = -int(center_x - green_x)/6
            dy = -int(center_y - green_y)/6
            print (dx,dy)
            # Move the CNC by the calculated movement
            move_to_position(dx, dy, speed=9000)

        # Crop the frame to 480x480
        frame = frame[:480, :480]

        # Convert the frame to a PIL Image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # Convert the resized image to a Tkinter-compatible format
        img_tk = ImageTk.PhotoImage(image=img)
        # Update the label with the resized image
        label.config(image=img_tk)
        label.image = img_tk

        # Wait for 0.2 seconds before updating again
        root.update()
        time.sleep(0.00001)

    cap.release()  # Release the webcam when done
    root.destroy()  # Destroy the Tkinter window when done

def process_frame(cap):
    
    ret, frame = cap.read()
    if not ret:
        return None, None, None  # Return None for frame and coordinates

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
        send_gcode('G90')
        
        # Get the largest green contour (assuming it's the target point)
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            # Calculate the center of the green point
            green_x = int(moments["m10"] / moments["m00"])
            green_y = int(moments["m01"] / moments["m00"])

            return frame, green_x, green_y

    return frame, None, None  # Return frame with no green point

time.sleep(0.0001)
tracer()
