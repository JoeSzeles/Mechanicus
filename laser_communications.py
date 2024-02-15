import serial
import time
import tkinter as tk

class LaserCommunication:
    def __init__(self):
        self.serial_port = None
        self.relative_mode = False

    def turn_laser_on(self, laser_power=400):
        self.send_command('M3')  # Turn on the laser
        self.send_command(f'G1 S{laser_power}')  # Set laser power to the specified value

    def turn_laser_off(self):
        self.send_command('M5')  # Turn off the laser

    def send_command(self, gcode_command):
        if self.relative_mode:
            gcode_command = "G91\n" + gcode_command + "\nG90\n"  # Wrap the command with relative mode codes
        
        self.serial_port.write(gcode_command.encode() + b'\n')
        self.serial_port.flush()

    def setup_serial(self, port, baud_rate):
        self.serial_port = serial.Serial(port, baud_rate)

    def send_gcode(self, x, y, laser_power=400):
        gcode_command = f'G1 X{x} Y{y} S{laser_power}'  # Include laser power (S) in the G-code
        self.send_command(gcode_command)

# Create an instance of the LaserCommunication class
laser_comm = LaserCommunication()

# Define the serial port and baud rate
serial_port = "COM4"  # Replace with your actual serial port
baud_rate = 115200

# Initialize the serial connection
laser_comm.setup_serial(serial_port, baud_rate)

# Define pulse duration for 1 and 0 (in seconds)
pulse_duration_1 = 0.2  # Example: 0.1 seconds for binary '1'
pulse_duration_0 = 0.1  # Example: 0.05 seconds for binary '0'

# Function to send binary-encoded text as G-code-encoded pulses
def send_text():
    text_to_send = text_input.get()
    
    print("Sending text:", text_to_send)  # Print the text being sent

    # Turn on the laser at power level S400 for 1 second
    laser_comm.turn_laser_on()
    time.sleep(1)
    laser_comm.turn_laser_off()

    for char in text_to_send:
        binary_char = bin(ord(char))[2:].zfill(8)  # Convert char to 8-bit binary string
        print("Sending character:", char, "Encoded as binary:", binary_char)  # Print the character and its binary encoding
        
        for bit in binary_char:
            if bit == '1':
                laser_comm.turn_laser_on()
                time.sleep(pulse_duration_1)
                laser_comm.turn_laser_off()
            else:
                laser_comm.turn_laser_on()
                time.sleep(pulse_duration_0)
                laser_comm.turn_laser_off()
    
    time.sleep(0.5)  # Pause between characters

# Create the GUI
root = tk.Tk()
root.title("Laser Communication")

# Text Input
text_input = tk.Entry(root, width=30)
text_input.pack()

# Send Button
send_button = tk.Button(root, text="Send", command=send_text)
send_button.pack()

# Main loop
root.mainloop()

# Close the serial connection when the GUI is closed
laser_comm.serial_port.close()
