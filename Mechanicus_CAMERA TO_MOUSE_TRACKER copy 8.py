import cv2
import numpy as np
import pyautogui

# Load the pre-trained face cascade classifier from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

# Constants for mouse movement speed (increase for faster movement)
MOUSE_SPEED_X = 2000
MOUSE_SPEED_Y = 2000

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        continue

    # Flip the frame horizontally to un-mirror it
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Check if a face is detected
    if len(faces) > 0:
        # Assuming there's only one face detected
        (x, y, w, h) = faces[0]

        # Calculate the center of the detected face
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Calculate the mouse cursor movement based on face position
        mouse_dx = (face_center_x - frame.shape[1] // 2) / frame.shape[1] * MOUSE_SPEED_X
        mouse_dy = (face_center_y - frame.shape[0] // 2) / frame.shape[0] * MOUSE_SPEED_Y

        # Get the current mouse cursor position
        current_x, current_y = pyautogui.position()

        # Calculate the new mouse cursor position
        new_x = current_x + mouse_dx
        new_y = current_y + mouse_dy

        # Move the mouse cursor to the new position
        pyautogui.moveTo(new_x, new_y)

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with face detection and tracking markings
    cv2.imshow('Head Tracking', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
