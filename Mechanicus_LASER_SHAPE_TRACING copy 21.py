import pygame
import cv2
import numpy as np
import serial
# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (600, 600)  # Size of the Pygame window
MAP_SIZE_MM = (1200, 1200)  # Size of the map in real-world millimeters
VIDEO_SIZE_MM = (400, 400)  # Size of the video feed canvas in real-world millimeters

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (45, 126, 255)

# Create Pygame window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Green Dot Tracker")

# Create scroll bars
horizontal_scroll = pygame.Surface((WINDOW_SIZE[0], 20))
vertical_scroll = pygame.Surface((20, WINDOW_SIZE[1]))
scroll_area = pygame.Surface(MAP_SIZE_MM)

# Initialize variables
green_x, green_y = None, None
laser_x, laser_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2  # Initial laser position
cnc_speed = 5  # Adjust the speed as needed
speed = 500
serial_port = 'COM4'
# Function to set the current position to 0,0
def set_current_position_to_zero():
    gcode_line = "G92 X0 Y0"
    send_gcode(gcode_line)

# Function to activate the laser
def activate_laser():
    
    send_gcode("M3 S15")
    
# Function to turn off the laser
def turn_off_laser():
  
    send_gcode("M5 S0")
    
# Function to home the CNC machine
def home():
    
    send_gcode("G28")

# Function to move the CNC to the center
def go_to_center():

    send_gcode('G1 X100 Y100 F500')
# Function to send G-code commands to control the CNC
def send_gcode(gcode_line):
    try:
        ser = serial.Serial(serial_port, 115200)
        ser.write(gcode_line.encode())
        ser.close()
    except serial.SerialException as e:
        print(f"Serial Error: {e}")
# Function to move the CNC to a specific position
def move_to_position(x, y, speed):
    x = max(0, min(x, 400))
    y = max(0, min(y, 400))
    gcode_line = f"G1 X{x} Y{y} F{speed}\n"
    send_gcode(gcode_line)
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
        frame = cv2.resize(frame, (VIDEO_SIZE_MM[0], VIDEO_SIZE_MM[1]))
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
                move_to_position(green_x,green_y)
            else:
                green_x, green_y = None, None
        else:
            green_x, green_y = None, None

    # Clear the screen
    screen.fill(BLACK)

    # Draw the map on the scroll area
    scroll_area.fill(WHITE)  # Map background is white

    # Draw the green point
    if green_x is not None and green_y is not None:
        # Calculate the absolute coordinates within the map
        x_abs = laser_x + (green_x - (VIDEO_SIZE_MM[0] / 2))
        y_abs = laser_y + (green_y - (VIDEO_SIZE_MM[1] / 2))

        # Draw the green dot in red on the map
        pygame.draw.circle(scroll_area, RED, (int(x_abs), int(y_abs)), 15)

    # Blit the map onto the scroll area
    scroll_x, scroll_y = 0, 0  # Initial scroll position

    # Update the scroll position if needed based on the green dot
    if green_x is not None and green_y is not None:
        scroll_x = max(0, min(x_abs - WINDOW_SIZE[0] // 2, MAP_SIZE_MM[0] - WINDOW_SIZE[0]))
        scroll_y = max(0, min(y_abs - WINDOW_SIZE[1] // 2, MAP_SIZE_MM[1] - WINDOW_SIZE[1]))

    screen.blit(scroll_area, (0, 0), (scroll_x, scroll_y, WINDOW_SIZE[0], WINDOW_SIZE[1]))

    # Draw horizontal scroll bar
    pygame.draw.rect(horizontal_scroll, WHITE, (0, 0, WINDOW_SIZE[0], 20))
    scroll_handle_x = (scroll_x / (MAP_SIZE_MM[0] - WINDOW_SIZE[0])) * (WINDOW_SIZE[0] - 40)
    pygame.draw.rect(horizontal_scroll, BLUE, (scroll_handle_x, 0, 40, 20))
    screen.blit(horizontal_scroll, (0, WINDOW_SIZE[1] - 20))

    # Draw vertical scroll bar
    pygame.draw.rect(vertical_scroll, WHITE, (0, 0, 20, WINDOW_SIZE[1]))
    scroll_handle_y = (scroll_y / (MAP_SIZE_MM[1] - WINDOW_SIZE[1])) * (WINDOW_SIZE[1] - 40)
    pygame.draw.rect(vertical_scroll, BLUE, (0, scroll_handle_y, 20, 40))
    screen.blit(vertical_scroll, (WINDOW_SIZE[0] - 20, 0))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

# Release the webcam
cap.release()
pygame.quit()
