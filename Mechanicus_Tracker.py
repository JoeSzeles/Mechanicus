import tkinter as tk
import serial
import time
xt = 100
yt = 100
dot= None
def Tracker():
    # Create a Tkinter window with a canvas
    root = tk.Tk()
    canvas = tk.Canvas(root, width=200, height=200, bg='white')
    canvas.pack()
    def update_position():
        global xt, yt
        job_id = 1
        # Define the position of the red dot
        # Connect to the printer serial port
        with serial.Serial('COM7', 250000, timeout=1) as ser:
            # Send a command to get the current position
            ser.write(b'M114\n')
            time.sleep(0.1)
            # Read the response
            response = ser.read_until(b'\nok', 2000).decode().strip()
            time.sleep(0.1)
            # Parse the response to get the current position
            for line in response.split('\n'):
                if line.startswith('x:'):
                    xt = int(float(line[2:].split(' ')[0]) * 10)
                if line.startswith('y:'):
                    yt = int(float(line[2:].split(' ')[0]) * 10)
        # Print the values of xt and yt for debugging purposes
        print(f"xt={xt}, yt={yt}")
        # Update the position of the red dot
        canvas.coords(dot, xt-2, yt-2, xt+2, yt+2)
        # Schedule the next update in 200ms
        root.after_cancel(job_id)
        job_id = root.after(200, update_position)
        
        # Draw a red dot on the canvas
    dot = canvas.create_oval(xt-2, yt-2, xt+2, yt+2, fill='red')
    
    # Start updating the position of the red dot
    global job_id
    job_id = root.after(200, update_position)
    
    # Start the Tkinter event loop
    root.mainloop()







    


    




    
    
    