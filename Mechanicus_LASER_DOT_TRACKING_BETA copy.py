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
cnc_rect = pygame.Rect(laser_x - 5, laser_y - 5, 25, 25)
cnc_speed = 1.7  # Adjust the speed as needed
# Initialize the serial connection
ser = serial.Serial('COM4', 115200)  # Change 'COM4' to the appropriate COM port and baud rate
# Open the webcam
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
                ser.write(b'M3 S150\n')  # Send the M3 command over serial
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
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate 90 degrees clockwise
    frame = cv2.flip(frame, 0)  # Flip vertically (mirror vertically)
    frame = cv2.resize(frame, VIDEO_SIZE)
    screen.blit(pygame.surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), (0, 0))

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
            if dist <= 60:
                # Stop the CNC rectangle's movement
                cnc_speed = 0  # Set the speed to zero 
            else:
            # Reset the CNC speed when there's no green dot detected
                cnc_speed = 3  # Adjust the speed as needed
            #LASER HEAD POSITION CONTROL
            realspeed= cnc_speed * 7000
            XG= cnc_rect.centerx
            YG=cnc_rect.centery
            # Format G-code-like line
            gcode_line = f"G1 X{YG} Y{XG} F{realspeed}\n"
            print (gcode_line)
            # Send the G-code-like line over serial
            ser.write(gcode_line.encode())  # Send the data over serial
            # Draw the blue rectangle (CNC)
            pygame.draw.rect(screen, BLUE, cnc_rect)

        # Draw the green dot in red
        pygame.draw.circle(screen, RED, (int(x_abs), int(y_abs)), 25)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(30)

# Release the webcam
cap.release()
ser.close()
pygame.quit()
