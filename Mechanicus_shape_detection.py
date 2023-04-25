import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import time

# Create a window with a label for showing the image

root = tk.Tk()
root.geometry("1280x960")
label = tk.Label(root)
label.pack()

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Apply Canny edge detection
    thr = np.zeros_like(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray)
    cv2.blur(frame, (1, 1), frame)
    thr = cv2.Canny(gray, 50, 190, None, 3, True)

    # Find contours and draw them on the frame
    contours, hierarchy = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    center = [None]*len(contours)
    radius = [None]*len(contours)
    hull = [None]*len(contours)

    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 1, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        center[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
        hull[i] = cv2.convexHull(c, False)

        if len(contours_poly[i]) > 15:
            cv2.drawContours(frame, contours_poly, i, (0, 255, 0), 2, 8, hierarchy, 0, (0, 0))
        else:
            cv2.drawContours(frame, contours_poly, i, (0, 0, 255), 2, 8, hierarchy, 0, (0, 0))

    # Convert the frame to a PIL Image and update the label
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)
    label.config(image=img)
    label.image = img

    # Wait for 0.5 seconds before updating again
    root.update()
    time.sleep(0.02)

    # Release the webcam and destroy the window when done
    root.mainloop()
 