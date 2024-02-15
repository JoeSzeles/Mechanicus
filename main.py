import datetime
import os
import random 
import datetime
import tkinter
from tkinter.tix import IMAGE
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageTk
from tkinter import Canvas
from tkinter import PhotoImage
from tkinter import Label

from tkinter import Tk
from tkinter import NW
from randomfrog import im 




#classtest= Cuboid.density
#I1.text((20, 1300), classtest, font=myFont2, fill =(r2, g2, b2))




ws = Tk()
ws.title('PythonGuides')
ws.geometry('750x750')
root=tkinter

canvas = Canvas(
    ws,
    width = 750 ,
    height = 750
    )      
canvas.pack()      
canvas.create_image(
    10,
    10, 
    anchor=NW, 
    image=im
    )     



ws.mainloop()






