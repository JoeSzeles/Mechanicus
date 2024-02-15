import cv2
import numpy as np
import pyautogui

# Load the pre-trained eye cascade classifier
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        continue

    # Flip the frame horizontally to un-mirror it
    frame = cv2.flip(frame, 1)

    # Resize the frame to 50% of its original height
    frame = cv2.resize(frame, None, fx=1, fy=1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Initialize variables for eye centers
    eye1_center, eye2_center = None, None

    # If both eyes are detected, track them
    if len(eyes) >= 2:
        eyes = sorted(eyes, key=lambda x: x[0])  # Sort by x-coordinate to find left and right eyes

        # Calculate the centers of the two eyes
        eye1_center = (eyes[0][0] + eyes[0][2] // 2, eyes[0][1] + eyes[0][3] // 2)
        eye2_center = (eyes[1][0] + eyes[1][2] // 2, eyes[1][1] + eyes[1][3] // 2)

        # Calculate the tracking point as the midpoint between the two eyes
        tracking_point = ((eye1_center[0] + eye2_center[0]) // 2, (eye1_center[1] + eye2_center[1]) // 2)

        # Mark the eyes and tracking point on the frame
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)  # Draw eyes in green

        cv2.circle(frame, tracking_point, 5, (0, 0, 255), -1)  # Mark tracking point in red

        # Calculate the screen resolution (you may need to adjust this)
        screen_width, screen_height = pyautogui.size()

        # Map the tracking point coordinates to the screen resolution
        x_screen = int((tracking_point[0] / frame.shape[1]) * screen_width*2-800)
        y_screen = int((tracking_point[1] / frame.shape[0]) * screen_height*3-800)
        # Make sure x_screen and y_screen are within the screen bounds
        x_screen = max(0, min(x_screen, screen_width - 1))
        y_screen = max(0, min(y_screen, screen_height - 1))


        # Move the mouse cursor to the calculated position
        pyautogui.moveTo(x_screen, y_screen)

    # Display the frame with eye and tracking point markings
    cv2.imshow('Eye Tracking', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
