import serial
import time
import math

# Define parameters
amplitude = 50  # Amplitude of the sine wave in units
period = 50     # Period of the sine wave in units
speed = 2000    # Speed of the pen in units per minute
frequency = 20  # Frequency of the sine wave in Hz
num_cycles = 5  # Number of cycles of the sine wave to plot

# Calculate the wavelength of the sine wave
wavelength = period * 2 * math.pi

# Calculate the time period of each cycle of the sine wave
time_period = 1 / frequency

# Calculate the number of points to plot per cycle
num_points = int(speed * time_period / period)

# Open serial port
ser = serial.Serial('COM7', 250000)
time.sleep(2)
ser.write(b"M105\n")  # Send a temperature reading command
response = ser.readline().decode('utf-8')  # Read a line of text from the serial
# Send G28 command to home the printer
ser.write(str.encode("G28\n"))
time.sleep(2)

# Loop through each cycle of the sine wave
for i in range(num_cycles):

    # Send G-Code to move to the starting position of the sine wave
    ser.write(str.encode("G0 X0 Y" + str(amplitude) + "\n"))
    
    # Loop through each point of the sine wave
    for j in range(num_points):
        
        # Calculate the x and y coordinates of the point
        x = j / num_points * wavelength
        y = amplitude * math.sin(x / period)
        
        # Send G-Code to move to the next point
        ser.write(str.encode("G1 X" + str(x) + " Y" + str(y) + " F" + str(speed) + "\n"))
    
    # Send G-Code to lift the pen and move to the next cycle
    ser.write(str.encode("G0 Z10\n"))
    time.sleep(1)

# Send G-Code to turn off the pen and move to the origin
ser.write(str.encode("M107\n"))
ser.write(str.encode("G0 X0 Y0\n"))
ser.write(str.encode("M84\n"))

# Close serial port
ser.close()
