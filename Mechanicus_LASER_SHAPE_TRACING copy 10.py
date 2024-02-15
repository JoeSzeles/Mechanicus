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

# Function to set the current position to 0,0
def set_current_position_to_zero():
    gcode_line = "G92 X0 Y0"
    send_gcode(gcode_line)
# Function to set the current position to 0,0
def Activate_laser():
    gcode_line = "M3 S15"
    send_gcode(gcode_line)
def Turn_off_laser():
    gcode_line = "M5 S0"
    send_gcode(gcode_line)
# Function to home the CNC machine
def home():
    gcode_line = "G28"
    send_gcode(gcode_line)

# Function to move the CNC to the center
def go_to_center():
    center_x = cnc_width / 2
    center_y = cnc_height / 2
    gcode_line = f"G0 X{center_x} Y{center_y}"
    send_gcode(gcode_line)

# Function to scale the video coordinates to CNC coordinates
def scale_coordinates(x, y):
    x_scale = cnc_width / video_width
    y_scale = cnc_height / video_height
    scaled_x = x * x_scale
    scaled_y = y * y_scale
    return scaled_x, scaled_y

# Function to send G-code commands to control the CNC
def send_gcode(gcode_line):
    try:
        ser = serial.Serial(serial_port, 115200)
        ser.write(gcode_line.encode())
        ser.close()
    except serial.SerialException as e:
        print(f"Serial Error: {e}")

# Function to move the CNC to a specific position
def move_to_position(x, y, speed):
    x = max(0, min(x, cnc_width))
    y = max(0, min(y, cnc_height))
    gcode_line = f"G1 X{x} Y{y} F{speed}\n"
    send_gcode(gcode_line)

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
        Activate_laser()
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            green_x = int(moments["m10"] / moments["m00"])
            green_y = int(moments["m01"] / moments["m00"])
            return frame, green_x, green_y
        Turn_off_laser()
    return frame, None, None
    
# Function to start the CNC control and object tracking
def tracer():
    # Open the webcam
    cap = cv2.VideoCapture(1)

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
    
    center_x = video_width // 2
    center_y = video_height // 2
    

    while True:
        frame, green_x, green_y = process_frame(cap)
        if frame is None:
            break

        if green_x is not None and green_y is not None:
            dx = -int(- green_x) / 6
            dy = -int( - green_y) / 6
            move_to_position(dx, dy, speed=9000)

        frame = frame[:video_width, :video_height]

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        label.config(image=img_tk)
        label.image = img_tk

        root.update()
        time.sleep(0.00001)

    cap.release()
    root.destroy()

# Entry point
if __name__ == "__main__":
    time.sleep(0.0001)
    tracer()
