import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import time

# Create a Tkinter window
root = tk.Tk()
root.title("Green Dot Tracker")

# Create a canvas to display the green dot
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Initialize variables
video_width, video_height = 130, 130  # Adjust to your actual video feed size
green_x, green_y = None, None

# Function to process the video frame and detect the green object
def process_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None, None

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the green color
    lower_green = np.array([35, 70, 70])
    upper_green = np.array([90, 255, 255])

    # Threshold the frame to get green objects
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest green contour
        largest_contour = max(contours, key=cv2.contourArea)
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            green_x = int(moments["m10"] / moments["m00"])
            green_y = int(moments["m01"] / moments["m00"])
        else:
            green_x, green_y = None, None
    else:
        green_x, green_y = None, None

    return frame, green_x, green_y

# Function to update the green dot's position on the canvas and print the coordinates
def update_green_dot():
    global green_x, green_y
    frame, green_x, green_y = process_frame(cap)

    # Clear the canvas
    canvas.delete("green_dot")

    if frame is not None and green_x is not None and green_y is not None:
        # Draw the green dot on the canvas in red
        canvas.create_oval(
            green_x - 5,
            green_y - 5,
            green_x + 5,
            green_y + 5,
            fill="red",
            outline="red",
            tags="green_dot",
        )

        # Print the coordinates
        print("Green Dot Coordinates:", green_x, green_y)

    # Update the canvas with the new frame
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_tk = ImageTk.PhotoImage(image=img)
    label.config(image=img_tk)
    label.image = img_tk

    # Schedule the next update after 100 milliseconds (10 times a second)
    root.after(100, update_green_dot)

# Open the webcam
cap = cv2.VideoCapture(1)

# Create a label to display the video feed
label = tk.Label(root)
label.pack()

# Start updating the green dot
update_green_dot()

# Run the Tkinter main loop
root.mainloop()

# Release the webcam
cap.release()
