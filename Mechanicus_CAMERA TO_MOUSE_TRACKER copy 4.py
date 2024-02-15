import cv2
import numpy as np
import pyautogui
import os
import cv2

# Get the base directory of the cv2 module
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))

# Define the path to your nose detection cascade XML file
nose_cascade_path = os.path.join(cv2_base_dir, 'haarcascade_mcs_nose.xml')

# Check if the file exists
if os.path.exists(nose_cascade_path):
    # Use the nose_cascade_path for nose detection
    nose_cascade = cv2.CascadeClassifier(nose_cascade_path)
else:
    print("The 'haarcascade_mcs_nose.xml' file does not exist in the OpenCV directory.")

# Load the pre-trained face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize variables for cursor position
current_cursor_position = pyautogui.position()
target_cursor_position = current_cursor_position
crop_x = 100  # X-coordinate of the top-left corner of the crop region
crop_y = 50   # Y-coordinate of the top-left corner of the crop region
crop_width = 400  # Width of the crop region
crop_height = 300  # Height of the crop region
# Define interpolation factor (adjust as needed)
interpolation_factor = 0.8
# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        continue

    # Mirror the frame horizontally
    frame = cv2.flip(frame, 1)

    ## Crop the frame to use only 60% of its height and width from the center
    #height, width, _ = frame.shape
    #crop_width = int(0.45 * width)
    #crop_height = int(0.45 * height)
    #x_start = (width - crop_width) // 2
    #y_start = (height - crop_height) // 2
    #frame = frame[y_start:y_start + crop_height, x_start:x_start + crop_width]

    # Convert the frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Iterate through detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Get the center of the detected face
        face_center_x = x + w // 2
        face_center_y = y + h // 2

        # Calculate the screen resolution (you may need to adjust this)
        screen_width, screen_height = pyautogui.size()

        # Map the face center coordinates to the screen resolution
        x_screen = int((face_center_x / frame.shape[1]) * screen_width)
        y_screen = int((face_center_y / frame.shape[0]) * screen_height)
        
        # Make sure x_screen and y_screen are within the screen bounds
        x_screen = max(0, min(x_screen, screen_width - 1))
        y_screen = max(0, min(y_screen, screen_height - 1))

        # Smooth the cursor movement using linear interpolation
        target_cursor_position = (
            int(current_cursor_position[0] + (x_screen - current_cursor_position[0]) * interpolation_factor),
            int(current_cursor_position[1] + (y_screen - current_cursor_position[1]) * interpolation_factor-100)
        )

        # Move the mouse cursor to the interpolated position
        pyautogui.moveTo(*target_cursor_position)


        # Uncomment the following lines if you want to add eye detection and draw rectangles around eyes
        # roi_gray = gray[y:y + h, x:x + w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #     cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

    # Display the frame with face and eye detections
    cv2.imshow('Face Tracking', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()