import cv2
import pygame
import numpy as np
import os
import math

# Initialize Pygame
pygame.init()

# Pygame window setup
screen_width = 5000
screen_height = 2500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cursor Tracking and Collision")

# Define colors
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Define masses
red_mass = 1000  # Mass of the red dot (black hole)
blue_mass = 10    # Mass of the blue dot (planet)

# Initialize cursor position
cursor_pos = [screen_width // 2, screen_height // 2]

# Load the pre-trained face cascade classifier
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize variables for cursor position
interpolation_factor = 0.1

# Initialize the video capture
cap = cv2.VideoCapture(1)  # Use the appropriate video source (0 for the default camera)

# Initialize red and blue ball positions (relative to Pygame window)
red_ball_radius = 30
red_ball_pos = [screen_width // 2, screen_height // 2]
blue_ball_radius = 10
blue_ball_pos = [red_ball_radius * 2, screen_height - red_ball_radius * 2]
blue_ball_speed = 0.1  # Initial speed of the blue dot
blue_ball_acceleration = 0.5  # Acceleration factor (adjust as needed)

# Gravitational constant (adjust as needed)
G = 0.6

# ...

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Update cursor position based on face tracking
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        x_screen = int((face_center_x / frame.shape[1]) * screen_width)
        y_screen = int((face_center_y / frame.shape[0]) * screen_height)
        x_screen = max(0, min(x_screen, screen_width - 1))
        y_screen = max(0, min(y_screen, screen_height - 1))
        cursor_pos = (
            int(cursor_pos[0] + (x_screen - cursor_pos[0]) * interpolation_factor),
            int(cursor_pos[1] + (y_screen - cursor_pos[1]) * interpolation_factor)
        )

    # Calculate the vector from blue ball to red ball (relative to Pygame window)
    dx = cursor_pos[0]*20 - blue_ball_pos[0]  # Change this line
    dy = cursor_pos[1]*40 - blue_ball_pos[1]  # Change this line
    distance = max(np.sqrt(dx**2 + dy**2), 1)  # Prevent division by zero

    # Calculate gravitational force
    force = G * (red_mass * blue_mass) / (distance ** 2)
    acceleration_x = force * dx / blue_mass
    acceleration_y = force * dy / blue_mass

    # Update blue ball velocity and position (relative to Pygame window)
    blue_ball_speed += blue_ball_acceleration
    blue_ball_pos[0] += blue_ball_speed * acceleration_x
    blue_ball_pos[1] += blue_ball_speed * acceleration_y

    # Calculate the displacement from the cursor position for the red ball
    dx_red = cursor_pos[0] - red_ball_pos[0]
    dy_red = cursor_pos[1] - red_ball_pos[1]

    # Define speed ratios for horizontal and vertical movement for the red ball
    horizontal_speed_ratio_red = 1.5
    vertical_speed_ratio_red = 1.5

    # Calculate the new position for the red dot
    new_x_red = red_ball_pos[0] + dx_red * horizontal_speed_ratio_red
    new_y_red = red_ball_pos[1] + dy_red * vertical_speed_ratio_red

    # Ensure the new position stays within the window boundaries
    new_x_red = max(red_ball_radius, min(new_x_red, screen_width - red_ball_radius))
    new_y_red = max(red_ball_radius, min(new_y_red, screen_height - red_ball_radius))

    # Update the red ball position
    red_ball_pos = [new_x_red, new_y_red]

    # Fill the screen with a white background
    screen.fill(white)

    # Draw the red and blue balls
    pygame.draw.circle(screen, red, red_ball_pos, red_ball_radius)  # Update red ball position
    pygame.draw.circle(screen, blue, (int(blue_ball_pos[0]), int(blue_ball_pos[1])), blue_ball_radius)

    pygame.display.flip()

# Quit Pygame and release video capture
pygame.quit()
cap.release()
