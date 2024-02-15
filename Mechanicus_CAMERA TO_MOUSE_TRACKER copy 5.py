import cv2
import numpy as np
import pyautogui

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        continue

    # Flip the frame horizontally to un-mirror it
    frame = cv2.flip(frame, 1)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the green color (you can adjust these)
    lower_green = np.array([35, 70, 70])
    upper_green = np.array([90, 255, 255])

    # Create a mask to isolate the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours of the green object in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables for the green dot position
    green_x, green_y = None, None

    # If green object is detected, track it
    if contours:
        # Find the largest contour (assumed to be the green object)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the coordinates of the center of the green object
        moments = cv2.moments(largest_contour)
        if moments["m00"] != 0:
            green_x = int(moments["m10"] / moments["m00"])
            green_y = int(moments["m01"] / moments["m00"])

    # Calculate the screen resolution (you may need to adjust this)
    screen_width, screen_height = pyautogui.size()

    # Map the green dot coordinates to the screen resolution
    if green_x is not None and green_y is not None:
        x_screen = int((green_x / frame.shape[1]) * screen_width)
        y_screen = int((green_y / frame.shape[0]) * screen_height)

        # Move the mouse cursor to the calculated position
        pyautogui.moveTo(x_screen, y_screen)

    # Display the frame with the green dot tracking
    cv2.imshow('Green Dot Tracking', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
