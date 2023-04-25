import serial
import time
import pygame
max_speed = 6000
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
ser.write(str.encode(f"G1 Z8\n"))
ser.write(b"M400\n")  # Wait for command to finish before sending new one
# Main game loop
while True:
    # Clear the screen
    screen.fill((0, 0, 0))
    max_acceleration = 1000 # Set maximum acceleration of printer head in mm/s^2
    last_pos = None
    last_time = time.monotonic()
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.write(str.encode("G28\n"))
            # Close serial port and Pygame window
            ser.close()
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ser.write(str.encode("G1 Z5\n"))
                ser.write(b"M400\n")  # Wait for command to finish before sending new one
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Draw a circle at the mouse position when clicked
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, (255, 0, 0), pos, 10)
            pygame.display.update()
        elif event.type == pygame.MOUSEMOTION:
            
            # Limit acceleration of mouse movement
            if is_drawing:
                pos = pygame.mouse.get_pos()
                if prev_pos:
                    dt = time.monotonic() - last_time
                    speed = pygame.math.Vector2(pos - prev_pos).length() / dt
                    if last_pos:
                        acceleration = (speed - pygame.math.Vector2(prev_pos - last_pos).length() / (last_time - time.monotonic())) / dt
                        if acceleration > max_acceleration:
                            pos = last_pos + (pos - last_pos) * max_acceleration / acceleration
                    last_pos = prev_pos
                    last_time = time.monotonic()
                    pygame.draw.line(screen, (255, 0, 0), prev_pos, pos, 10, 5)  # changed line thickness to 2
                    pygame.draw.circle(screen, (255, 0, 0), pos, 5)
                prev_pos = pos
        elif event.type == pygame.MOUSEBUTTONUP:
            is_drawing = False
            prev_pos = None
            ser.write(str.encode("G1 Z8\n"))
            ser.write(b"M400\n")  # Wait for command to finish before sending new one
    # Send G1 command to move the printer head to the mouse position
    max_speed = 10000 # Set maximum speed of printer head in mm/min
    ...
    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        x = int(pos[0] * 300 / 900)  # Convert mouse x-coordinate to printer x-coordinate
        y = int((900 - pos[1]) * 300 / 900)  # Convert mouse y-coordinate to printer y-coordinate, with mirroring reversed
        # Limit speed to maximum speed of printer head
        speed =  max_speed
        if pygame.mouse.get_pressed()[0]:
            ser.write(str.encode("G1 Z5\n"))
        else:
            ser.write(str.encode("G1 Z8\n"))
        ser.write(str.encode(f"G1 X{x} Y{y} F{speed}\n"))
        ser.write(b"M400\n")  # Wait for command to finish before sending new one
        time.sleep(0.1)

    # Update the Pygame window
    pygame.display.update()

