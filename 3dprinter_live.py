import serial
import time
import pygame
max_speed = 200000
# Open serial port
ser = serial.Serial('COM7', 250000)
time.sleep(2)
ser.write(b"M105\n")  # Send a temperature reading command
response = ser.readline().decode('utf-8')  # Read a line of text from the serial
# Send G28 command to home the printer
ser.write(str.encode("G28\n"))
time.sleep(2)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Mouse Movements")

# Set up variables for drawing
prev_pos = None
is_drawing = False

# Main game loop
while True:
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close serial port and Pygame window
            ser.close()
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Draw a circle at the mouse position when clicked
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, (255, 0, 0), pos, 10)
            pygame.display.update()
        elif event.type == pygame.MOUSEMOTION:
            # Draw a red dotted line to show mouse movements
            if is_drawing:
                pos = pygame.mouse.get_pos()
                if prev_pos:
                    pygame.draw.line(screen, (255, 0, 0), prev_pos, pos, 5)
                    pygame.display.update()
                prev_pos = pos
        elif event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False
            prev_pos = None

    # Send G1 command to move the printer head to the mouse position
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        x = int(pos[0] * 300 / 800)  # Convert mouse x-coordinate to printer x-coordinate
        y = int((600 - pos[1]) * 300 / 600)  # Convert mouse y-coordinate to printer y-coordinate
        ser.write(str.encode(f"G1 X{x} Y{y} F{max_speed}\n"))
        time.sleep(0.01)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the Pygame window
    pygame.display.update()


