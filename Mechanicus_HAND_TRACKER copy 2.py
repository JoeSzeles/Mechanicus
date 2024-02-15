import cv2
import numpy as np
import time
import serial
import threading
import sys 


class CNCControlApp:
    def __init__(self):
        # Initialize default values for the green point and current quadrant
        self.green_x = None
        self.green_y = None
        self.current_quadrant = "center"  # Initialize as "center"

        # Check the connection when the app starts
        if not self.check_connection():
            print("Connection Error", "Unable to establish a connection to the CNC machine.")
            self.root.destroy()  # Close the app if there's no connection
        if self.check_connection():
            print("established a connection to the CNC machine.")
            
        # Perform a 10 mm move left and right for testing
        self.send_gcode("G91")  # Switch to relative mode
        print("G91")
        self.send_gcode("G1 X10 Y10 F500")  # Move right by 10 mm
        time.sleep(0.1)  # Wait for 2 seconds


        # Start the coordinate update loop
        threading.Thread(target=self.run).start()
        

    def check_connection(self):
        # Try to establish a connection with the CNC machine
        try:
            ser = serial.Serial("COM3", 115200)
            ser.close()
            return True
        except serial.SerialException as e:
            print(f"Serial Error: {e}")
            sys.exit(1)  # Terminate the script if there's no connection
        
    def detect_green_point(self, frame):
        lower_green = np.array([35, 70, 70])
        upper_green = np.array([90, 255, 255])

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            moments = cv2.moments(largest_contour)
            if moments["m00"] != 0:
                self.green_x = int(moments["m10"] / moments["m00"])
                self.green_y = int(moments["m01"] / moments["m00"])
            else:
                self.green_x = None
                self.green_y = None
        else:
            self.green_x = None
            self.green_y = None

    def track_hand(self):
        if self.green_x is not None and self.green_y is not None:
            video_width, video_height = 480, 480  # Adjust these values based on your camera resolution
            cnc_width, cnc_height = 400, 400  # in millimeters
            
            step_size = 20.0
            speed = 500  # F500 G-code speed

            # Determine the current quadrant based on the position of the green point
            if self.green_x < video_width / 2:
                if self.green_y < video_height / 2:
                    self.current_quadrant = "top_left"
                else:
                    self.current_quadrant = "bottom_left"
            else:
                if self.green_y < video_height / 2:
                    self.current_quadrant = "top_right"
                else:
                    self.current_quadrant = "bottom_right"

            # Calculate the movement steps based on the quadrant
            if self.current_quadrant == "top_left":
                x_step = -step_size
                y_step = step_size
            elif self.current_quadrant == "top_right":
                x_step = step_size
                y_step = step_size
            elif self.current_quadrant == "bottom_left":
                x_step = -step_size
                y_step = -step_size
            elif self.current_quadrant == "bottom_right":
                x_step = step_size
                y_step = -step_size
            else:
                x_step = 0
                y_step = 0  # Center quadrant, no movement

            # Generate and send G-code command
            gcode_command = f"G1 X{x_step} Y{y_step} F{speed}"
            print("Generated G-code command:", gcode_command)  # Print the generated G-code
            self.send_gcode(gcode_command)

    # Function to send G-code commands to control the CNC
    def send_gcode(self, gcode_command):
        try:
            ser = serial.Serial('COM4', 115200)
            ser.write(gcode_command.encode())
            ser.close()
        except serial.SerialException as e:
            print(f"Serial Error: {e}")

    def run(self):
        video_capture = cv2.VideoCapture(1)  # Change the argument to specify the video source (0 for webcam)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Detect the green point
            self.detect_green_point(frame)

            
            # Track the hand and generate G-code
            self.track_hand()

            # Display the frame with the green point
            cv2.circle(frame, (self.green_x, self.green_y), 5, (0, 255, 0), -1)
            cv2.imshow("Green Point Tracking", frame)

            # Stop CNC motion when no green point is detected
            if self.green_x is None or self.green_y is None:
                #print("No green point detected. Stopping CNC motion.")
                self.send_gcode("G1 X0 Y0 F0")  # Send an emergency stop command

            # Exit the loop when the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = CNCControlApp()
