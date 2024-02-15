import cv2
import numpy as np
import pyautogui

# Load the pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

# Set initial variables for mouse control
initial_mouse_x, initial_mouse_y = pyautogui.position()
current_mouse_x, current_mouse_y = initial_mouse_x, initial_mouse_y
acceleration = 1.6  # You can adjust this value to control the acceleration

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Rotate the frame 90 degrees clockwise
    frame = cv2.flip(frame, 1)  # Flip vertically (mirror vertically)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        delta_x = face_center_x - initial_mouse_x+222
        delta_y = face_center_y - initial_mouse_y+222

        # Apply acceleration to mouse movement
        delta_x *= acceleration
        delta_y *= acceleration

        # Update the current mouse position
        current_mouse_x += delta_x
        current_mouse_y += delta_y

        # Move the mouse cursor
        pyautogui.moveTo(current_mouse_x, current_mouse_y)

        initial_mouse_x, initial_mouse_y = current_mouse_x, current_mouse_y

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

    cv2.imshow('Facial Feature Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
