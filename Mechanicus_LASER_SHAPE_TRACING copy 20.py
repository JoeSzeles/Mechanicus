import pygame
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (400, 400)
VIDEO_SIZE = (130, 130)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create Pygame window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Green Dot Tracker")

# Initialize variables
green_x, green_y = None, None
laser_x, laser_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2  # Initial laser position
cnc_rect = pygame.Rect(laser_x - 10, laser_y - 10, 20, 20)

# Open the webcam
cap = cv2.VideoCapture(1)

# Pygame clock for controlling frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Process the video frame and detect the green object
    ret, frame = cap.read()
    if ret:
        # Crop the frame to 480x480 pixels
        frame = frame[:480, :480]
        # Rotate the frame 90 degrees counterclockwise
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        # Flip the frame vertically (mirror vertically)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, VIDEO_SIZE)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 70, 70])
        upper_green = np.array([90, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            moments = cv2.moments(largest_contour)
            if moments["m00"] != 0:
                green_x = int(moments["m10"] / moments["m00"])
                green_y = int(moments["m01"] / moments["m00"])
            else:
                green_x, green_y = None, None
        else:
            green_x, green_y = None, None

    # Clear the screen
    screen.fill(BLACK)

    # Draw the green dot
    if green_x is not None and green_y is not None:
        # Calculate the absolute coordinates within the window
        x_abs = laser_x + (green_x - (VIDEO_SIZE[0] / 2))
        y_abs = laser_y + (green_y - (VIDEO_SIZE[1] / 2))
        
        # Move the CNC rectangle to the new position
        cnc_rect.center = (x_abs, y_abs)

        # Draw the green dot in red
        pygame.draw.circle(screen, RED, (int(x_abs), int(y_abs)), 15)

    # Draw the CNC rectangle
    pygame.draw.rect(screen, BLUE, cnc_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

# Release the webcam
cap.release()
pygame.quit()
