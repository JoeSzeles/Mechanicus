import pygame
import cv2
import numpy as np
import serial
import pyautogui


# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (480, 480)
VIDEO_SIZE = (480, 480)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (45, 126, 255)

# Create Pygame window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Green Dot Tracker")

# Initialize variables
green_x, green_y = None, None
laser_x, laser_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2  # Initial laser position
cnc_rect = pygame.Rect(laser_x - 5, laser_y - 5, 25, 25)
cnc_speed = 1.7  # Adjust the speed as needed
# Initialize the serial connection
ser = serial.Serial('COM4', 115200)  # Change 'COM4' to the appropriate COM port and baud rate
# Open the webcam
# Initialize the MIDI output port




    
cap = cv2.VideoCapture(1)

# Pygame clock for controlling frame rate
clock = pygame.time.Clock()

# Function to calculate the distance between two points
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Initialize a variable to keep track of whether the green point is currently detected
green_detected = False
red_detected = False
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Process the video frame and detect the green and red points
    ret, frame = cap.read()
    if ret:
        frame = frame[:480, :480]
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, VIDEO_SIZE)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detection of the green point (similar to your existing code)
        lower_green = np.array([35, 70, 70])
        upper_green = np.array([90, 255, 255])
        mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours_green:
            largest_contour_green = max(contours_green, key=cv2.contourArea)
            moments_green = cv2.moments(largest_contour_green)
            if moments_green["m00"] != 0:
                green_x = int(moments_green["m10"] / moments_green["m00"])
                green_y = int(moments_green["m01"] / moments_green["m00"])
                green_detected = True
                ser.write(b'M3 S25\n')  # Send the M3 command over serial
            else:
                green_x, green_y = None, None
                green_detected = False
                ser.write(b'M5 S0\n')  # Send the M3 command over serial
        else:
            green_x, green_y = None, None
            green_detected = False
            ser.write(b'M5 S0\n')  # Send the M3 command over serial
        # Detection of the red point
        lower_red = np.array([0, 150, 150])
        upper_red = np.array([10, 255, 255])
        mask_red = cv2.inRange(hsv_frame, lower_red, upper_red)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours_red:
            # Add the M3 command to turn on the laser
            
            largest_contour_red = max(contours_red, key=cv2.contourArea)
            moments_red = cv2.moments(largest_contour_red)
            if moments_red["m00"] != 0:
                red_x = int(moments_red["m10"] / moments_red["m00"])
                red_y = int(moments_red["m01"] / moments_red["m00"])
                red_detected = True
                #ser.write(b'M3 S500\n')  # Send the M3 command over serial
            else:
                red_x, red_y = None, None
                red_detected = False
                #ser.write(b'M5 S0\n')
        else:
            # Add the M5 command to turn off the laser when red point is not detected
            #ser.write(b'M5\n')  # Send the M5 command over serial
            red_x, red_y = None, None
            red_detected = False
    # Clear the screen
    #screen.fill(BLACK)

     # Draw the video frame as the background
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Rotate 90 degrees clockwise
    frame = cv2.flip(frame, 0)  # Flip vertically (mirror vertically)
    frame = cv2.resize(frame, VIDEO_SIZE)
    screen.blit(pygame.surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), (0, 0))

    # Replace the G-code logic with mouse cursor control
    if green_x is not None and green_y is not None:
        # Calculate the absolute coordinates within the window
        x_abs = laser_x + (green_x - (VIDEO_SIZE[0] / 2))
        y_abs = laser_y + (green_y - (VIDEO_SIZE[1] / 2))

        # Calculate the screen resolution (you may need to adjust this)
        screen_width, screen_height = pyautogui.size()

        # Map the coordinates from the video frame to the screen resolution
        x_screen = int((x_abs / VIDEO_SIZE[0]) * screen_width)
        y_screen = int((y_abs / VIDEO_SIZE[1]) * screen_height)

        # Move the mouse cursor to the calculated position
        pyautogui.moveTo(x_screen, y_screen)

        # Draw the blue rectangle (CNC)
        pygame.draw.rect(screen, BLUE, cnc_rect)

        # Draw the green dot in red
        pygame.draw.circle(screen, RED, (int(x_abs), int(y_abs)), 25)






    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Release the webcam
cap.release()
ser.close()
# Close the MIDI output port when the program is done

pygame.quit()


import cv2

# Load the pre-trained face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Convert the frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Iterate through detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Get the ROI (region of interest) for eyes within the face rectangle
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # Draw a rectangle around each detected eye
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # Display the frame with face and eye detections
    cv2.imshow('Eye Tracking', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
