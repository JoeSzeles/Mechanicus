import cv2
import numpy as np
import pyautogui

# Load the pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

# Set the desired crop size (absolute values)
crop_width = 320
crop_height = 320

# Define the screen resolution
screen_width = 1920
screen_height = 1080

# Initialize variables for mouse control
current_mouse_x, current_mouse_y = pyautogui.position()
target_mouse_x, target_mouse_y = current_mouse_x, current_mouse_y
interpolation_factor = 0.8  # You can adjust this value to control the interpolation smoothness

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

        # Calculate the difference between the face center and the desired mouse position
        delta_x = face_center_x - crop_width // 2
        delta_y = face_center_y - crop_height // 2

        # Scale the delta values to fit the screen resolution
        scaled_delta_x = int(delta_x * (screen_width / crop_width))
        scaled_delta_y = int(delta_y * (screen_height / crop_height))

        # Update the target mouse position as scaled absolute values
        target_mouse_x = scaled_delta_x
        target_mouse_y = scaled_delta_y

        # Interpolate the current and target mouse positions for smooth movement
        current_mouse_x += int((target_mouse_x - current_mouse_x) * interpolation_factor)
        current_mouse_y += int((target_mouse_y - current_mouse_y) * interpolation_factor)

        # Move the mouse cursor to the new position
        pyautogui.moveTo(current_mouse_x, current_mouse_y)

        # Crop the frame to the desired size (320x320) centered on the face
        cropped_frame = frame[
            max(0, face_center_y - crop_height // 2):min(frame.shape[0], face_center_y + crop_height // 2),
            max(0, face_center_x - crop_width // 2):min(frame.shape[1], face_center_x + crop_width // 2)
        ]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

    # Display the cropped frame with facial feature detection and smoothed mouse tracking
    cv2.imshow('Facial Feature Tracking', cropped_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
