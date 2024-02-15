import pygame
import cv2
import numpy as np
import serial

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
cnc_rect = pygame.Rect(laser_x - 10, laser_y - 10, 20, 20)
cnc_speed = 5  # Adjust the speed as needed

# Initialize the serial connection
ser = serial.Serial('COM4', 115200)  # Change 'COM4' to the appropriate COM port and baud rate

# Open the webcam
cap = cv2.VideoCapture(1)

# Pygame clock for controlling frame rate
clock = pygame.time.Clock()

# Function to calculate the distance between two points
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Process the video frame and detect the green object
    ret, frame = cap.read()
    if ret:
        frame = frame[:480, :480]
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
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

        # Calculate the distance between the CNC rectangle and the green dot
        dist = distance((cnc_rect.centerx, cnc_rect.centery), (x_abs, y_abs))

        if dist > 0:
            # Calculate the unit vector towards the green dot
            dx = (x_abs - cnc_rect.centerx) / dist
            dy = (y_abs - cnc_rect.centery) / dist

            # Move the CNC rectangle towards the green dot
            cnc_rect.move_ip(dx * cnc_speed, dy * cnc_speed)

            # Ensure the CNC rectangle stays within the window
            cnc_rect.left = max(0, min(cnc_rect.left, WINDOW_SIZE[0] - cnc_rect.width))
            cnc_rect.top = max(0, min(cnc_rect.top, WINDOW_SIZE[1] - cnc_rect.height))
            
            realspeed= cnc_speed * 200
            XG= cnc_rect.centerx/3
            YG=cnc_rect.centery/3
            # Format G-code-like line
            gcode_line = f"G1 X{XG} Y{YG} F{realspeed}\n"
            print (gcode_line)
            # Send the G-code-like line over serial
            ser.write(gcode_line.encode())  # Send the data over serial

            # Draw the blue rectangle (CNC)
            pygame.draw.rect(screen, BLUE, cnc_rect)

        # Draw the green dot in red
        pygame.draw.circle(screen, RED, (int(x_abs), int(y_abs)), 45)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

# Release the webcam and close the serial connection
cap.release()
ser.close()
pygame.quit()
