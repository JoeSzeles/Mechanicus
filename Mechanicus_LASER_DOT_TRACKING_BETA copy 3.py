import pygame
import cv2
import numpy as np
import serial
import mido
import pygame.midi
import threading  # Import the threading module
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
mido_out_port = mido.open_output()  # You can choose the MIDI output port you want to use


# Define MIDI channels for X and Y axes
X_AXIS_CHANNEL = 0  # Change to the desired MIDI channel for X axis
Y_AXIS_CHANNEL = 1  # Change to the desired MIDI channel for Y axis
instrument_for_x=35
instrument_for_y=91
# Function to play a MIDI note in a separate thread with a specified channel
def play_midi_note_thread(note_number, channel, velocity=100, duration=0.1):
    def play_note():
        note_on = mido.Message('note_on', note=note_number, velocity=velocity, channel=channel)
        mido_out_port.send(note_on)
        pygame.time.delay(int(duration * 300))  # Delay to control note duration
        note_off = mido.Message('note_off', note=note_number, velocity=0, channel=channel)
        mido_out_port.send(note_off)

    # Create a new thread and start it
    midi_thread = threading.Thread(target=play_note)
    midi_thread.start()

# Function to play a MIDI note for the X axis with a specified instrument
def play_midi_note_x(note_number, instrument, velocity=100, duration=0.1):
    # Send a Program Change message to change the instrument on the X axis channel
    program_change = mido.Message('program_change', program=instrument, channel=X_AXIS_CHANNEL)
    mido_out_port.send(program_change)

    # Create a new thread for playing the MIDI note with the specified channel (X axis)
    midi_thread = threading.Thread(target=play_midi_note_thread, args=(note_number, X_AXIS_CHANNEL, velocity, duration))
    midi_thread.start()  # Start the thread

# Function to play a MIDI note for the Y axis with a specified instrument
def play_midi_note_y(note_number, instrument, velocity=100, duration=0.1):
    # Send a Program Change message to change the instrument on the Y axis channel
    program_change = mido.Message('program_change', program=instrument, channel=Y_AXIS_CHANNEL)
    mido_out_port.send(program_change)

    # Create a new thread for playing the MIDI note with the specified channel (Y axis)
    midi_thread = threading.Thread(target=play_midi_note_thread, args=(note_number, Y_AXIS_CHANNEL, velocity, duration))
    midi_thread.start()  # Start the thread

    midi_thread.start()  # Start the thread
    
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
        # Calculate note numbers based on CNC machine position
        # Calculate note numbers based on CNC machine position
        x_note = int((cnc_rect.centerx / WINDOW_SIZE[0]) * 88) + 20  # Map x-axis to MIDI notes
        y_note = int(((WINDOW_SIZE[1] - cnc_rect.centery) / WINDOW_SIZE[1]) * 40) + 60  # Map y-axis to MIDI notes

        # Send Program Change messages to change instruments on each axis
        program_change_x = mido.Message('program_change', program=instrument_for_x, channel=X_AXIS_CHANNEL)
        program_change_y = mido.Message('program_change', program=instrument_for_y, channel=Y_AXIS_CHANNEL)
        mido_out_port.send(program_change_x)
        mido_out_port.send(program_change_y)

        # Create and start a new thread for each MIDI note
        threading.Thread(target=play_midi_note_thread, args=(x_note, X_AXIS_CHANNEL, 64, 0.1)).start()
        threading.Thread(target=play_midi_note_thread, args=(y_note, Y_AXIS_CHANNEL, 64, 0.1)).start()



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
    clock.tick(60)

# Release the webcam
cap.release()
ser.close()
# Close the MIDI output port when the program is done
mido_out_port.close()
pygame.quit()




gm_instruments = {
    0: "Acoustic Grand Piano",
    1: "Bright Acoustic Piano",
    2: "Electric Grand Piano",
    3: "Honky-tonk Piano",
    4: "Electric Piano 1",
    5: "Electric Piano 2",
    6: "Harpsichord",
    7: "Clavinet",
    8: "Celesta",
    9: "Glockenspiel",
    10: "Music Box",
    11: "Vibraphone",
    12: "Marimba",
    13: "Xylophone",
    14: "Tubular Bells",
    15: "Dulcimer",
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
    19: "Church Organ",
    20: "Reed Organ",
    21: "Accordion",
    22: "Harmonica",
    23: "Tango Accordion",
    24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)",
    26: "Electric Guitar (jazz)",
    27: "Electric Guitar (clean)",
    28: "Electric Guitar (muted)",
    29: "Overdriven Guitar",
    30: "Distortion Guitar",
    31: "Guitar harmonics",
    32: "Acoustic Bass",
    33: "Electric Bass (finger)",
    34: "Electric Bass (pick)",
    35: "Fretless Bass",
    36: "Slap Bass 1",
    37: "Slap Bass 2",
    38: "Synth Bass 1",
    39: "Synth Bass 2",
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    44: "Tremolo Strings",
    45: "Pizzicato Strings",
    46: "Orchestral Harp",
    47: "Timpani",
    48: "String Ensemble 1",
    49: "String Ensemble 2",
    50: "SynthStrings 1",
    51: "SynthStrings 2",
    52: "Choir Aahs",
    53: "Voice Oohs",
    54: "Synth Voice",
    55: "Orchestra Hit",
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    59: "Muted Trumpet",
    60: "French Horn",
    61: "Brass Section",
    62: "SynthBrass 1",
    63: "SynthBrass 2",
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    72: "Piccolo",
    73: "Flute",
    74: "Recorder",
    75: "Pan Flute",
    76: "Blown Bottle",
    77: "Shakuhachi",
    78: "Whistle",
    79: "Ocarina",
    80: "Lead 1 (square)",
    81: "Lead 2 (sawtooth)",
    82: "Lead 3 (calliope)",
    83: "Lead 4 (chiff)",
    84: "Lead 5 (charang)",
    85: "Lead 6 (voice)",
    86: "Lead 7 (fifths)",
    87: "Lead 8 (bass + lead)",
    88: "Pad 1 (new age)",
    89: "Pad 2 (warm)",
    90: "Pad 3 (polysynth)",
    91: "Pad 4 (choir)",
    92: "Pad 5 (bowed)",
    93: "Pad 6 (metallic)",
    94: "Pad 7 (halo)",
    95: "Pad 8 (sweep)",
    96: "FX 1 (rain)",
    97: "FX 2 (soundtrack)",
    98: "FX 3 (crystal)",
    99: "FX 4 (atmosphere)",
    100: "FX 5 (brightness)",
    101: "FX 6 (goblins)",
    102: "FX 7 (echoes)",
    103: "FX 8 (sci-fi)",
    104: "Sitar",
    105: "Banjo",
    106: "Shamisen",
    107: "Koto",
    108: "Kalimba",
    109: "Bagpipe",
    110: "Fiddle",
    111: "Shanai",
    112: "Tinkle Bell",
    113: "Agogo",
    114: "Steel Drums",
    115: "Woodblock",
    116: "Taiko Drum",
    117: "Melodic Tom",
    118: "Synth Drum",
    119: "Reverse Cymbal",
    120: "Guitar Fret Noise",
    121: "Breath Noise",
    122: "Seashore",
    123: "Bird Tweet",
    124: "Telephone Ring",
    125: "Helicopter",
    126: "Applause",
    127: "Gunshot"
}

# Print the list of GM instruments and their numbers
for number, name in gm_instruments.items():
    print(f"Instrument {number}: {name}")
