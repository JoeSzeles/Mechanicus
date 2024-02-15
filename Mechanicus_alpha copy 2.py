from cmath import e
import tkinter as tk
from tkinter import ttk
from tkinter import CENTER, CURRENT, Canvas, filedialog, Text
import random
from turtle import left, right
from PIL import ImageTk
import datetime
import os
from telnetlib import OUTMRK

from PIL import ImageDraw
from PIL import ImageFont,ImageEnhance, ImageFilter, ImageOps, ImageChops, ImageGrab
from click import open_file
#import cv2
from numpy import imag, int0, number
import numpy as np
from tkinter import filedialog as fd
from itertools import count, cycle
from pygame import init
from tkinter import END
from tkinter import Toplevel, Event
from tkcolorpicker import askcolor
from pyrsistent import b
import pandas as pd
from tkinter import *
from tkinter.filedialog import asksaveasfilename as saveAs
from PIL import Image, ImageDraw
import io
import subprocess
import serial
from serial import *
import time
import os
from datetime import time
import math
from scipy.interpolate import splprep, splev
from scipy import interpolate
import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re
from datetime import datetime as dt
from optimise import optimise_path, get_total_distance
from utils import *
import sys
import re

import gcodegenerator
import matplotlib.pyplot as plt
import importlib
import config3

gcode = ""
global job_id
global xt, yt

for file in os.scandir('undo'):
    if file.name.endswith(".png"):
        os.unlink(file.path)  

undo = open("undo.txt","w")
undo.write(str(1))
undo.close()


## START MAIN WINDOW###############################################################################################################################################
root=tk.Tk() #Load main app window
##root.resizable(False, False) ###NO resize of main app window


x1= str(root.winfo_screenwidth())               
y1= str(root.winfo_screenheight())  
gcode=()


#newimage2 = Image.new(mode = "RGBA", size = (750, 750),color = (0,0,0,0))
newimage2 = Image.new('RGBA', (900, 900), (0,0,0,0))
newimage2.save('temp2.png')
#newimage2.save('temp2.png')


fn4=1
print(str(fn4))
newimage2.save('undo//undo'+str(fn4)+'.png')
undo.close()
undo2 = open(r"undo.txt","w+")
undo2.write(str(fn4))
undo2.close()






#root.geometry("1100x900") ##main app window size
##root.attributes('-fullscreen',True)
root.title("MECHANICUS V.0.1 Beta. (c)Reservoir Frogs 2023")
root.configure(bg="#263d42", borderwidth=0)
root.iconphoto(True, tk.PhotoImage(file='icon/icon.png'))
root.geometry('324x900+0+0')

x4=(int(x1)/3)
y4=(int(y1)/3)
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()   

wx=int(x4)
wy=int(y4)
stp=20 #Number os undos, steps back
### config ################

from Mechanicus_Config import *
from Mechanicus_shape_detection_image_working import*

sys.setrecursionlimit(30000) # set the recursion limit to 10000


    
def saveAs():

    filename=saveAs(title="Save image as...",filetype=(("PNG images","*.png"),("JPEG images","*.jpg"),("GIF images","*.gif")))


#def Paint_Gcode():
def clearundo():
    for file in os.scandir('undo'):
        if file.name.endswith(".png"):
            os.unlink(file.path)  
def Undo():

    if linecount >0:
        undoline()
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    u=1
    fn4=fn3-u
    print(str(fn4))
    
    if fn4==-1:
        im = Image.open('temp2.png')
    else:
        im = Image.open('undo\\undo'+str(fn4)+'.png')

 
    im.save(".\\temp2.png")
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)
    

def Redo():

    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    u=1
    fn4=fn3+u
    print(str(fn4))
    
    if fn4==-1:
        im = Image.open('temp2.png')
    else:
        im = Image.open('undo\\undo'+str(fn4)+'.png')

 
    im.save(".\\temp2.png")
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)


def frog():
    randomfrog2 = str(random.randrange(1,11111))
    path3=".\\images\\"+ randomfrog2 + ".png"

    im = Image.open(path3)

    #I1.text((20, 1300), classtest, font=myFont2, fill =(r2, g2, b2))
    resizeimg= im.resize((450,450),resample=3 )
    print("C:\\nft generated\\nft frogs FULL\\nft catalouge 1\\output\\"+ randomfrog2 + ".png")
    ###  RESIZE TO HALF MAIN WINDOW SIZE SQUARE #############################################################
    preview=im.resize((750,750),resample=3 )
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    preview.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    #### resizeimg2= im.resize((450,450),resample=3 )
    preview.save(".\\temp2.png")
    preview.save(".\\temp1.png")

    file2 = open(r"temp.txt","w+")
    file2.write(str(randomfrog2))

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2

    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width6, height=height6)

    

def tag():
    

    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()

    ## IMAGE SIZE AUTO#######################################
    im = Image.open('temp2.png')
    width, height = im.size
    ratio=height/width
    width2=int(width);
    height2=int(width*ratio)
    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    im.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    ### BLUR RESET ########
    write=0.1
    file4 = open(r"fblur.txt","w+")
    file4.write(str(write))
    print(str(write))
    file4.close()

    ###########################################################
    I1 = ImageDraw.Draw(im)
    # Custom font style and font size
    myFont = ImageFont.truetype('arialbd.ttf' , int(wx/25))
    myFont2 = ImageFont.truetype('arialbd.ttf', int(wx/5))

    # Add Text to an image
    r=(random.randrange(2,250)) 
    g=(random.randrange(2,250)) 
    b=(random.randrange(2,250)) 
    r2=(random.randrange(2,250)) 
    g2=(random.randrange(2,250)) 
    b2=(random.randrange(2,250)) 
    anon= ("Anon # ") +str((random.randrange(1,90000000)))
    date = ("Date ")+ str(datetime.datetime.now())
    frognumber = " #"+ fn

    I1.text((20, width2/13-40),date, font=myFont, fill =(r, g, b))
    I1.text((20, width2/9),anon, font=myFont, fill =(r, g, b))
    I1.text((20, (width2/1.3)), frognumber, font=myFont2, fill =(r2, g2, b2))

    print("C:\\nft generated\\nft frogs FULL\\nft catalouge 1\\output\\"+ fn + ".png")
    preview=im.resize((width2,height2),resample=3 )
    preview.save(".\\temp2.png")
    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width, height=height)


def savefrog():
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    
    path4="output\\"+ fn + ".png"
    out=Image.open("temp2.png")
    out.save(path4)
    file2.close()

    
    write=0
    file2.close()
    file3 = open(r"fhue.txt","w+")
    file3.write(str(write))
    print(str(write))
    file3.close()



def pixelart():
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    pixelpath="pixel\\P"+ fn + ".png"
    im=Image.open("temp2.png")
    ## IMAGE SIZE AUTO#######################################
    im = Image.open('temp2.png')
    width, height = im.size
    ratio=height/width


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    im.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    pix=(height/120)
    if height > 750:
        pix=(height/200)

    x3=(height/pix)
    y3=((height/pix)*ratio)
    
    ###########################################################
    downscale=im.resize((int(x3),int(y3)),resample=0 )
    pixelimg=downscale.resize((width,height),resample=0 )
    
    #pixelimg.save(pixelpath)
    pixelimg.save(".\\temp2.png")
    file2.close()

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width, height=height)

    



def pixelavatar():
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    pixelpath="pixel\\P"+ fn + ".png"
    im=Image.open("temp2.png")
    ## IMAGE SIZE AUTO#######################################
    im = Image.open('temp2.png')
    width, height = im.size
    ratio=height/width


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    im.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    pix=(height/120)
    if height > 750:
        pix=(height/200)

    x3=(height/pix)
    y3=((height/pix)*ratio)
    width3=int(width/2)
    height3=int(height/2)
    ###########################################################
    downscale=im.resize((int(x3),int(y3)),resample=0 )
    pixelimg=downscale.resize((width,height),resample=0 )
    width3=int(width/2)
    height3=int(height/2)
    scaledownimg=pixelimg.resize((width3,height3),resample=0 )
    
    #pixelimg.save(pixelpath)
    scaledownimg.save(".\\temp2.png")
    file2.close()

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)

def doublesize():

    ## IMAGE SIZE AUTO#######################################
    im = Image.open('temp2.png')
    width, height = im.size
    width2=int(width*2)
    height2=int(height*2)

    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    im.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    ###########################################################
    
    pixelimg=im.resize((width2,height2),resample=0 )

    
    #pixelimg.save(pixelpath)
    pixelimg.save(".\\temp2.png")
    

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)
def halfsize():

    
   
    ## IMAGE SIZE AUTO#######################################
    im = Image.open('temp2.png')
    width, height = im.size
    width2=int(width/2)
    height2=int(height/2)

    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    im.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    ###########################################################  
    pixelimg=im.resize((width2,height2),resample=0 )
    pixelimg.save(".\\temp2.png")
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2

    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)

def thirdsize():

    ## IMAGE SIZE AUTO#######################################
    im = Image.open('temp2.png')
    width, height = im.size
    width2=int(width/3)
    height2=int(height/3)

    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    im.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    ###########################################################
    
    pixelimg=im.resize((width2,height2),resample=0 )
    #pixelimg.save(pixelpath)
    pixelimg.save(".\\temp2.png")
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2

    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)

def addbrightness():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")
    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    im3 = ImageEnhance.Brightness(out)
    pixelimg=im3.enhance(1.2)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
 
   


def redbrightness():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = ImageEnhance.Brightness(out)
    pixelimg=im3.enhance(0.85)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def addcontrast():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = ImageEnhance.Contrast(out)
    pixelimg=im3.enhance(1.2)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)


def redcontrast():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = ImageEnhance.Contrast(out)
    pixelimg=im3.enhance(0.85)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def addsat():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")

    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = ImageEnhance.Color(out)
    pixelimg=im3.enhance(1.1)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def redsat():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = ImageEnhance.Color(out)
    pixelimg=im3.enhance(0.8)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def bw():
    
     
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    out=Image.open("temp2.png")

    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = ImageEnhance.Color(out)
    im3.enhance(-1.-1).save
    pixelimg=im3.enhance(0.0)
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    
def sharpen():
    

    out=Image.open("temp2.png")

    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    im3 = out.filter(ImageFilter.SHARPEN)
    pixelimg=im3

    pixelimg.save(".\\temp2.png")

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)


def blur():
    
    file3 = open(r"fblur.txt","r")
    fn=float(file3.read())
    bl=fn+0.1
    write=float(fn)+0.1
    file3.close()
    file4 = open(r"fblur.txt","w+")
    file4.write(str(write))
    print(str(write))
    file4.close()

    # ADD FILTER ####################
    out=Image.open("temp2.png")
    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = out.filter(ImageFilter.GaussianBlur(radius=bl))
    pixelimg=im3
    
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    
    ## UPDATE SCREEN#######
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def deatil():
    
    file3 = open(r"fblur.txt","r")
    fn=float(file3.read())
    bl=fn+0.1
    write=float(fn)+0.1
    file3.close()
    file4 = open(r"fblur.txt","w+")
    file4.write(str(write))
    print(str(write))
    file4.close()

    # ADD FILTER ####################
    out=Image.open("temp2.png")


    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    im3 = out.filter(ImageFilter.DETAIL)
    pixelimg=im3
    
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    
    ## UPDATE SCREEN#######
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def invert():
    

    out=Image.open("temp2.png")
    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    pixelimg=im3
    
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)


def reset():

        
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    
    out=Image.open("temp1.png")
        
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    pixelimg=im3
    pixelimg=out

   # pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    ### HUE reset ########
    write=0
    file3 = open(r"fhue.txt","w+")
    file3.write(str(write))
    print(str(write))
    file3.close()
    ### BLUR RESET ########
    write=0.1
    file4 = open(r"fblur.txt","w+")
    file4.write(str(write))
    print(str(write))
    file4.close()


    for file in os.scandir('undo'):
        if file.name.endswith(".png"):
            os.unlink(file.path)       
 

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)

def app_exit():
    for file in os.scandir('undo'):
        if file.name.endswith(".png"):
            os.unlink(file.path)  

    out=Image.open("appbg2.png")
    pixelimg=out
   # pixelimg.save(bw)
    pixelimg.save(".\\temp1.png")
    pixelimg.save(".\\temp2.png")

    ### HUE reset ########

    write=0
    file3 = open(r"fhue.txt","w+")
    file3.write(str(write))
    print(str(write))
    file3.close()
    ### BLUR RESET ########
    write=0.1
    file4 = open(r"fblur.txt","w+")
    file4.write(str(write))
    print(str(write))
    file4.close()

        
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(1))
    undo2.close()

    out=out.convert('RGB')
    im3=ImageOps.invert(out)
    im3=im3.convert('RGBA')
    pixelimg=im3

    
    root.destroy()



############# HUE RANDOM ###########################################################

def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')


def shift_hue(arr,hout):
    hsv=rgb_to_hsv(arr)
    hsv[...,0]=hout
    rgb=hsv_to_rgb(hsv)
    return rgb


def randomhue():

    file2 = open(r"temp.txt","r")
    fn=file2.read()
    

    img = Image.open('temp2.png')

    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    pixelimg=im3

    arr = np.array(img)


    hue = ((random.uniform(1, 360))-(random.uniform(1, 360)))/360.0
    new_img = Image.fromarray(shift_hue(arr,hue), 'RGBA')
    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def redhue():

    file2 = open(r"fhue.txt","r")
    fn=float(file2.read())
    
    img = Image.open('temp2.png')
        
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGB')
    im3=ImageOps.invert(img)
    im3=im3.convert('RGBA')
    

    arr = np.array(img)


    hue=fn-0.1
    write=float(fn)-0.02
    file2.close()
    file3 = open(r"fhue.txt","w+")
    file3.write(str(write))
    print(str(write))
    file3.close()
    
    new_img = Image.fromarray(shift_hue(arr,hue), 'RGB')
    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def addhue():

    file2 = open(r"fhue.txt","r")
    fn=float(file2.read())
    img = Image.open('temp2.png')
            
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGB')
    im3=ImageOps.invert(img)
    im3=im3.convert('RGBA')
    
    arr = np.array(img)
    hue=fn+0.1
    write=float(fn)+0.02
    file2.close()
    file3 = open(r"fhue.txt","w+")
    file3.write(str(write))
    print(str(write))
    file2.close()
    
    new_img = Image.fromarray(shift_hue(arr,hue), 'RGB')
    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def edge():

    file2 = open(r"fhue.txt","r")
    fn=float(file2.read())

    img = Image.open('temp2.png')
        
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGB')
    im3=im3 = ImageOps.invert(img)
    im3=im3.convert('RGBA')
    
    new_img = img.filter(ImageFilter.EDGE_ENHANCE)
    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
#Inputbox ###


def croptb():


    img5 = Image.open('temp2.png')
    width5, height5 = img5.size

            
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img5.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img5=img5.convert('RGB')
    im3=im3 = ImageOps.invert(img5)
    im3=im3.convert('RGBA')
    

    img5=img5.convert("RGBA")
    
    #top and left: These parameters represent the top left coordinates i.e (x,y) = (left, top).
    #bottom and right: These parameters represent the bottom right coordinates i.e. (x,y) = (right, bottom).
    
    ## ((x_min,y_min,x_max,y_max))#####
    x2=0
    y2=10
   

    #new_img = img5.resize((x, y, x + width5 , y + height5))
    new_img = img5.crop((x2, y2, width5-x2 , height5-y2))

    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)


def croplr():


    img5 = Image.open('temp2.png')
    width5, height5 = img5.size
 
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img5.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img5=img5.convert('RGB')
    im3=im3 = ImageOps.invert(img5)
    im3=im3.convert('RGBA')
    
    img5=img5.convert("RGBA")
    
    #top and left: These parameters represent the top left coordinates i.e (x,y) = (left, top).
    #bottom and right: These parameters represent the bottom right coordinates i.e. (x,y) = (right, bottom).
    
    ## ((x_min,y_min,x_max,y_max))#####
    x2=10
    y2=0
   

    #new_img = img5.resize((x, y, x + width5 , y + height5))
    new_img = img5.crop((x2, y2, width5-x2 , height5-y2))

    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)

def cropbox():


    img5 = Image.open('temp2.png')
    width5, height5 = img5.size
       
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img5.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img5=img5.convert('RGB')
    im3=im3 = ImageOps.invert(img5)
    im3=im3.convert('RGBA')
    
    img5=img5.convert("RGBA")
    
    #top and left: These parameters represent the top left coordinates i.e (x,y) = (left, top).
    #bottom and right: These parameters represent the bottom right coordinates i.e. (x,y) = (right, bottom). 
    ## ((x_min,y_min,x_max,y_max))#####

    if width5 >= height5:
            x3=(width5-height5)/2
            y3=0
            right1=x3+height5
            bottom1=height5

    if width5 < height5:
            y3=(height5-width5)/2
            x3=0

            right1=width5
            bottom1=y3+width5

    #new_img = img5.resize((x, y, x + width5 , y + height5))
    new_img = img5.crop((x3, y3, right1, bottom1))

    rgb_im=new_img.convert("RGBA")
    rgb_im.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)


def loadFrognum():
   
    inp = inputtxt.get(1.0, "end-1c")

    bw=".\\images\\"+ inp + ".png"
    out=Image.open(bw)
            
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    
    pixelimg=out.resize((wx,wx),resample=3 )
    pixelimg.save(".\\temp2.png")
 
    file2 = open(r"temp.txt","w+")
    file2.write(str(inp))
    file2.close()


    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = img3.size
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)


def open_img():
    # Select the Imagename  from a folder


    imp1 = openfilename()
    imp2=os.path.basename(imp1)
    
    bw=str(imp2 )
    out=Image.open(imp1)
    out2 = out.convert("RGBA") 

    file2 = open(r"temp.txt","w+")
    file2.write(str(imp2))
    file2.close()

    width2, height2 = out.size
    


    out.save(".\\temp2.png")
    out.save(".\\temp1.png")
    print(str(width2 + height2))
 
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    with Image.open('temp2.png') as img7:
        width8, height8 = img7.size
    print(str(width6)+'x'+ str(width6))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width8, height=height8)

def openfilename():
 
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title ='"pen')
    return filename

def openlayer():
 
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    layername = filedialog.askopenfilename(title ='"pen')
    return layername



def color32():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    
    out=Image.open("temp2.png")
            
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    
    im3 = out.convert('P', palette=Image.ADAPTIVE, colors=32)
    pixelimg=im3.convert("RGBA")
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()


    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)



def color16():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    
    out=Image.open("temp2.png")
                
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    
    im3 = out.convert('P', palette=Image.ADAPTIVE, colors=16)
    pixelimg=im3.convert("RGBA")
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def color4():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()
    
    out=Image.open("temp2.png")
                
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    
    im3 = out.convert('P', palette=Image.ADAPTIVE, colors=4)
    pixelimg=im3.convert("RGBA")
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()

    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def color2():
    
    file2 = open(r"temp.txt","r")
    fn=file2.read()
    file2.close()

    out=Image.open("temp2.png")
                
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    out.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    out=out.convert('RGB')
    im3=im3 = ImageOps.invert(out)
    im3=im3.convert('RGBA')
    
    im3 = out.convert('P', palette=Image.ADAPTIVE, colors=2)
    pixelimg=im3.convert("RGBA")
    #pixelimg.save(bw)
    pixelimg.save(".\\temp2.png")
    file2.close()


    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

###### MERGE FILE ##################################################################################################
def mergel():
    
    filename = ('temp2.png')
    filename2 =openfilename()
    
    with Image.open('temp2.png') as img:
        width, height = img.size
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    foreground=foreground.resize((width,height),resample=3)
    foreground = foreground.convert("RGBA")
    background.paste(foreground, (0, 0), foreground) 
    background.save('temp2.png')
    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def mergel100():
    
    filename = ('temp2.png')
    filename2 =openlayer()

   # with Image.open('temp2.png') as img:
   # width, height = img.size
    inp = layerscale.get(1.0, "end-1c")
    inp2=int(inp)
    with Image.open(filename2) as img:
        width, height = img.size

    x=int(width)
    y=int(height)
    ratio=height/width
    width2=((inp2/100)*x)*ratio
    height2=((inp2/100)*y)
    print(width2,height2)

    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    
    foreground=foreground.resize((int(width2),int(height2)),resample=3)
    foreground = foreground.convert("RGBA")
    
    background.paste(foreground, (0, 0), foreground) 
    background.save('temp2.png')
    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)


def blendlayer():
    
    filename = ('temp2.png')
    filename2 =openlayer()
    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)

    with Image.open('temp2.png') as img:
        width, height = img.size
                    
    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
 
    background = Image.open(filename) 
    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    foreground=foreground.convert('RGBA')  #you can make sure your pic is in the right mode by check foreground.mode
    data=foreground.getdata()  #you'll get a list of tuples
    newData=[]
    for a in data:
        a=a[:3] #you'll get your tuple shorten to RGB
        a=a+(inp2,) #change the 100 to any transparency number you like between (0,255)
        newData.append(a)
    foreground.putdata(newData) #you'll get your new foreground ready
    foreground=foreground.resize((width,height),resample=3)
    foreground = foreground.convert("RGBA")
    foreground.copy()

    background.paste(foreground, (0, 0), foreground) 
    background=background.convert("RGBA")
    background.save('temp3.png')
    im5=background
    def addlayer():
        background = im5
        background=background.convert("RGBA")
        foreground = Image.open(filename2)
        foreground=foreground.resize((width,height),resample=3)
        foreground = foreground.convert("RGBA")
        background.paste(foreground, (0, 0), foreground) 
        background.save('temp2.png')
    addlayer()

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def alphalayer():
    
    filename = ('temp2.png')
    filename2 =openlayer()
    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)

    with Image.open('temp2.png') as img:
        width, height = img.size
                    

 
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    
    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    
    foreground=foreground.resize((width,height),resample=3)
    foreground = foreground.convert("RGBA")
    foreground.copy()
    foreground.putalpha(inp2)
    background.paste(foreground, (0, 0), foreground) 
    background.save('temp2.png')

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)


def multiplylayer():
    
    filename = ('temp2.png')
    filename2 =openlayer()
    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)

    with Image.open('temp2.png') as img:
        width, height = img.size
                        
 
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()


    background=background.convert("RGB")
    foreground = Image.open(filename2)
    foreground=foreground.resize((width,height),resample=3)
    foreground = foreground.convert("RGB")
    background=ImageChops.multiply(background,foreground)
    background=background.convert("RGBA")
    background.save('temp2.png')
    
    ### Update View
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def differencelayer():
    
    filename = ('temp2.png')
    filename2 =openlayer()
    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)

    with Image.open('temp2.png') as img:
        width, height = img.size
                        
 
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGB")
    foreground = Image.open(filename2)
    foreground=foreground.resize((width,height),resample=3)
    foreground = foreground.convert("RGBA")
    foreground.copy()
    foreground.putalpha(inp2)
    foreground = foreground.convert("RGB")
    background=ImageChops.difference(background,foreground)
    background=background.convert("RGBA")
    background.save('temp2.png')
    
    ### Update View
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def ColorChroma():
    filename = ('temp2.png')
    filename2 =openlayer()

    inpr = r.get(1.0, "end-1c")
    inpr2=int(inpr)
    inpg = g.get(1.0, "end-1c")
    inpg2=int(inpg)
    inpb = b1.get(1.0, "end-1c")
    inpb2=int(inpb)
    
    with Image.open('temp2.png') as img:
        width, height = img.size
                    
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    foreground = foreground.convert("RGBA")
    foreground=foreground.resize((width,height),resample=3)
 
    pixdata = foreground.load()

    width2, height2 = foreground.size
    for y in range(height2):
        for x in range(width2):
            if pixdata[x, y] == (inpr2, inpg2, inpb2, 255):
                pixdata[x, y] = (inpr2, inpg2, inpb2, 0)
         
    #foreground.putalpha(inp2)
    background.paste(foreground, (0, 0), foreground) 
    background=background.convert("RGBA")
    background.save('temp2.png')
    
    ### Update View
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    
def PickChroma():
    filename = ('temp2.png')
    filename2 =openlayer()  
    with Image.open('temp2.png') as img:
        width, height = img.size
   
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    foreground = foreground.convert("RGBA")
    foreground=foreground.resize((width,height),resample=3)
    askcol=askcolor(title = "Tkinter Color Chooser")
    rgb=(askcol[0])
    pixdata = foreground.load()
    width2, height2 = foreground.size
    for y in range(height2):
        for x in range(width2):
            if pixdata[x, y] == (rgb, 255):
                pixdata[x, y] = (rgb, 0)
         
    #foreground.putalpha(inp2)
    background.paste(foreground, (0, 0), foreground) 
    background=background.convert("RGBA")
    background.save('temp2.png')
    
    ### Update View
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def customsize():

    inpx = xscale.get(1.0, "end-1c")
    inpy = yscale.get(1.0, "end-1c")
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')

 
    x=int(inpx)
    y=int(inpy)
    width2=int(inpx)
    height2=int(inpy)
    print(width2,height2)

    ###########################################################
    
    pixelimg=img.resize((width2,height2),resample=4 )
    #pixelimg.save(pixelpath)
    pixelimg.save(".\\temp2.png")
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)


def extend_top():

    with Image.open('temp2.png') as img:
        width2, height2 = img.size
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')
    print(width2,height2)
    ext=20
    
    background = Image.new(mode = "RGBA", size = (width2, height2+ext),color = (255,255,255,255))
    cv.configure(width=width2, height=height2+ext)

    foreground=img
    foreground.convert('RGBA')

    background.paste(foreground, (0, ext), foreground) 
    background.save("temp2.png")
    
    with Image.open('temp2.png') as imgn:
        width4, height4 = img.size

    imgn=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=imgn)
    label.image=imgn
    cv.itemconfigure(drawimg, image = imgn)
    cv.configure(width=width4, height=height4+ext)
    

def extend_bottom():

    with Image.open('temp2.png') as img:
        width2, height2 = img.size
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')
    print(width2,height2)
    ext=20
    
    background = Image.new(mode = "RGBA", size = (width2, height2+ext),color = (255,255,255,255))
    

    foreground=img
    foreground.convert('RGBA')

    background.paste(foreground, (0, 0), foreground) 
    background.save("temp2.png")
    
    with Image.open('temp2.png') as imgn:
        width4, height4 = img.size

    imgn=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=imgn)
    label.image=imgn
    cv.itemconfigure(drawimg, image = imgn)
    cv.configure(width=width4, height=height4+ext)
   
def extend_right():

    with Image.open('temp2.png') as img:
        width2, height2 = img.size
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')
    print(width2,height2)
    ext=20
    
    background = Image.new(mode = "RGBA", size = (width2+ext, height2),color = (255,255,255,255))
    

    foreground=img
    foreground.convert('RGBA')

    background.paste(foreground, (0, 0), foreground) 
    background.save("temp2.png")
    
    with Image.open('temp2.png') as imgn:
        width4, height4 = img.size

    imgn=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=imgn)
    label.image=imgn
    cv.itemconfigure(drawimg, image = imgn)
    cv.configure(width=width4+ext, height=height4)

def extend_left():

    with Image.open('temp2.png') as img:
        width2, height2 = img.size
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')
    print(width2,height2)
    ext=20
    
    background = Image.new(mode = "RGBA", size = (width2+ext, height2),color = (255,255,255,255))
    

    foreground=img
    foreground.convert('RGBA')

    background.paste(foreground, (ext, 0), foreground) 
    background.save("temp2.png")
    
    with Image.open('temp2.png') as imgn:
        width4, height4 = img.size

    imgn=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=imgn)
    label.image=imgn
    cv.itemconfigure(drawimg, image = imgn)
    cv.configure(width=width4+ext, height=height4)

def extend_frame():

    with Image.open('temp2.png') as img:
        width2, height2 = img.size
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')
    print(width2,height2)
    ext=20
    
    background = Image.new(mode = "RGBA", size = (width2+ext, height2+ext),color = (255,255,255,255))
    

    foreground=img
    foreground.convert('RGBA')

    background.paste(foreground, (int(ext/2), int(ext/2)), foreground) 
    background.save("temp2.png")
    
    with Image.open('temp2.png') as imgn:
        width4, height4 = img.size

    imgn=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=imgn)
    label.image=imgn
    cv.itemconfigure(drawimg, image = imgn)
    cv.configure(width=width4+ext, height=height4+ext)

def image_shrink():

    with Image.open('temp2.png') as img:
        width2, height2 = img.size
    img=Image.open('temp2.png')

                    
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    img.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    img=img.convert('RGBA')
    print(width2,height2)
    ext=20

    E=img.resize((width2-ext,height2-ext), resample=1)
    E.save("temp2.png")
    

    imgn=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=imgn)
    label.image=imgn
    cv.itemconfigure(drawimg, image = imgn)
    with Image.open('temp2.png') as img:
        width9, height9 = img.size
    print(width9,height9)
    cv.configure(width=width9, height=height9)
    cv.configure(width=width9, height=height9)
    

def colortint():

    askcol=askcolor(title = "Tkinter Color Chooser")
    rgb=(askcol[0])
    filename = ('temp2.png')
    print(str(rgb))
    inpr = r.get(1.0, "end-1c")
    inpr2=int(inpr)
    inpg = g.get(1.0, "end-1c")
    inpg2=int(inpg)
    inpb = b1.get(1.0, "end-1c")
    inpb2=int(inpb)
    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)
    with Image.open('temp2.png') as img:
        width, height = img.size
 
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGBA")
    foreground = Image.new(mode = "RGB", size = (width, height),color = (rgb))
    foreground=foreground.convert("RGBA")
    foreground.copy()
    foreground.putalpha(inp2)
    background.paste(foreground, (0, 0), foreground) 
    background.save('temp2.png')
    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def Orange():

    filename = ('temp2.png')
    background = Image.open(filename)
                        
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    background.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    background=background.convert('RGB')
    im3=im3 = ImageOps.invert(background)
    im3=im3.convert('RGBA')
 
    background=background.convert("RGBA")
    foreground = Image.new(mode = "RGBA", size = (width, height),color = (4,2,1,1))
    foreground=foreground.convert("RGBA")
    foreground.copy()
    background.paste(foreground, (0, 0), foreground) 
    
    im3 = ImageEnhance.Color(background)
    pixelimg=im3.enhance(1.1)
    pixelimg.save('temp2.png')

    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def blue():

    filename = ('temp2.png')
    with Image.open('temp2.png') as img:
        width, height = img.size
    
    background = Image.open(filename)
                        
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    background.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    background=background.convert('RGB')
    im3=im3 = ImageOps.invert(background)
    im3=im3.convert('RGBA')
 
    background=background.convert("RGB")
    foreground = Image.new(mode = "RGB", size = (width, height),color = (1,200,255))
    
    foreground=foreground.resize((width,height),resample=3)
    foreground = foreground.convert("RGB")
    
    background=ImageChops.multiply(background,foreground)
    background=background.convert("RGBA")
    background.save('temp2.png')

    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def imageChroma():
    filename = ('temp2.png')
    filename2 =openlayer()

    with Image.open('temp2.png') as img:
        width, height = img.size
 
 
    
    background = Image.open(filename)

    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()

    background=background.convert("RGBA")
    foreground = Image.open(filename2)
    foreground = foreground.convert("RGBA")
    foreground=foreground.resize((width,height),resample=3)
    askcol=askcolor(title = "Tkinter Color Chooser")
    rgb=(askcol[0])
    pixdata = foreground.load()
    width2, height2 = foreground.size
    for y in range(height2):
        for x in range(width2):
            if pixdata[x, y] == (rgb, 255):
                pixdata[x, y] = (rgb, 0)
         
    #foreground.putalpha(inp2)
    background.paste(foreground, (0, 0), foreground) 
    background=background.convert("RGBA")
    background.save('temp2.png')
    
    ### Update View
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)


def newimage():

    askcol=askcolor(title = "Tkinter Color Chooser")
    rgb=(askcol[0])
    width2=750
    height2=750
    newimage = Image.new(mode = "RGBA", size = (width2, height2),color = rgb)
    newimage.save('temp2.png')
    clearundo()
    clear()
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=width2, height=height2)

def newempty():

    
    newimage = Image.new(mode = "RGBA", size = (750, 750),color = (255,255,255,0))
    newimage.save('temp2.png')
    clearundo()
    clear()
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=750 ,height=750)
    

def readcsv():
    data=pd.read_csv(r'rgb.csv',sep=',')
    print(str(data))
def writecsv():
    data=pd.DataFrame[r,g,b1]
    data.to_csv('rgb.csv',sep=',')
    print(str(data))



def colorgrab_win():

    pic = ImageGrab.grab()
    Grabbutton = tk.Button(root, text="Blue",bd=2,height=2, width=14, fg="white", bg="#0075d0" )
    Grabbutton.place(x=0, y=380)
    def color():
        x, y = win.winfo_pointerx(), win.winfo_pointery()
        r, g, b = pic.getpixel((x, y))
        rgb=pic.getpixel((x, y))
        hue = f"#{r:02x}{g:02x}{b:02x}"
        Grabbutton.config( text = rgb)
        Grabbutton["background"] = hue


        r1 = open(r"r.txt","w+")
        rw=r1.write(str(r))
        print(rw)

        g1 = open(r"g.txt","w+")
        gw=g1.write(str(g))
        print(gw)

        b1 = open(r"b.txt","w+")
        bw=b1.write(str(b))
        print(bw)

        #with open('rgb.csv', mode='w') as csvfile:
         #   fieldnames = [r,g,b]
         #   writer= csv.DictWriter(csvfile, fieldnames=fieldnames)
          #  writer.writeheader()
           # #writer.writerow({r,g,b})

        #undo2.write(str(rgb))
        #undo2.write(str(r)+','+str(g)+','+ str(b))
        #np.savetxt('rgb.csv', (int(r), int(g), int(b)), delimiter=',')
        #undo2.write(r,g,b)
        undo2.close()

    Grabbutton["command"] = color
    Grabbutton.focus_force()
    
def grab_tint():

    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)

    r = open("r.txt","r")
    r1=r.read()
    g = open("g.txt","r")
    g1=g.read()
    b = open("b.txt","r")
    b1=b.read()

    filename = ('temp2.png')
    inp = alpha.get(1.0, "end-1c")
    inp2=int(inp)
    with Image.open('temp2.png') as img:
        width, height = img.size

    background = Image.open(filename)
    undoimg=background
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    undoimg.save('undo//undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    print(str(r1)+str(g1)+str(b1))
    background=background.convert("RGBA")
    foreground = Image.new(mode = "RGB", size = (width, height),color = (int(r1),int(g1),int(b1)))
    foreground=foreground.convert("RGBA")
    foreground.copy()
    foreground.putalpha(inp2)
    background.paste(foreground, (0, 0), foreground) 
    background.save('temp2.png')
    

    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)

def update_screen():
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    imgE=Image.open("temp2.png")
    widthE, heightE = imgE.size
    cv.configure(height=widthE, width=heightE)
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    

def update_window(img_thr):
    img2=ImageTk.PhotoImage(img_thr)
    imgE=Image.open(img_thr)
    widthE, heightE = imgE.size
    cv.configure(height=widthE, width=heightE)
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image = img2)
    
############# WIN IMAGE WINDOW TOOLS 
def resizeIMG():


    
    update_screen()



###Paint_Gcode TOOLS
####################################
import re

def savedrawing():
    print("saving drawing")
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x,bed_max_y
    bed_height =  bed_max_y
    bed_width= bed_max_x
 
    with Image.open('temp2.png') as img7:
        width6, height6 = img7.size
    cv.configure(width=width6, height=height6)
    cv.postscript(file="temp.eps")
    
    # Read the EPS file and extract the coordinates
    coords = []
    with open("temp.eps") as f:
        for line in f:
            if re.match(r'^\d+(\.\d+)? \d+(\.\d+)? moveto$', line):
                x, y = line.split()[:2]
                coords.append((float(x), float(y)))
            elif re.match(r'^\d+(\.\d+)? \d+(\.\d+)? lineto$', line):
                x, y = line.split()[:2]
                coords.append((float(x), float(y)))
    
    # Create a new G-code file
    with open('drawing.gcode', 'w') as f:
        # Write the initial G-code commands to home the printer and set the bed temperature
        f.write('G28\n')  # Home all axes
        
        # Process each line on the canvas and generate the corresponding G-code command
        for i in range(0, len(coords), 2):
            x1, y1 = coords[i]
            x2, y2 = coords[i+1]
            from config3 import scaleF
            # Scale the coordinates to fit the bed size
            x1_scaled = (x1 / width6) * bed_width*scaleF
            y1_scaled = bed_height - ((y1 / height6) * bed_height)*scaleF
            x2_scaled = (x2 / width6) * bed_width*scaleF
            y2_scaled = bed_height - ((y2 / height6) * bed_height)*scaleF
            
            # Write the G-code commands for the line
            f.write('G1 X{:.2f} Y{:.2f} Z5 F3000\n'.format(x1_scaled, y1_scaled))
            f.write('M400\n')  # Wait for the printer to finish moving
            f.write('G1 X{:.2f} Y{:.2f} F3000\n'.format(x2_scaled, y2_scaled))
            f.write('M400\n')  # Wait for the printer to finish moving
        
        # Write the final G-code command to turn off the printer
        f.write('M104 S0\n')  # Turn off extruder
        f.write('M140 S0\n')  # Turn off bed
        f.write('G28 X0 Y0\n')  # Home X and Y axes
        f.write('M84\n')  # Disable motors
    
    with Image.open('temp2.png') as img7:
        width6, height6 = img7.size
    cv.configure(width=width6, height=height6)
    cv.postscript(file="temp.eps")
    pic = Image.open('temp.eps')
    pic.load(scale=4)



    print(str(width6)+'x'+ str(width6))

    pic2 = pic.resize((width6+4, height6+4), Image.ANTIALIAS)
    #pic = pic.resize(new_size, Image.ANTIALIAS)
    #new_img = img5.resize((x, y, x + width5 , y + height5))
    pic2.save('temp3.png')
    img8=Image.open("temp3.png")
    width7, height7= img8.size
    cv.configure(width=width6+4, height=height6+4)
    pic3 = img8.crop((0, 0, width6, height6))
    pic3.save('temp2.png')
 
    # Update the canvas and image widget
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    cv.configure(width=width6+4, height=height6+4)
    label.configure(image=img2)
    label.image=img2
    cv.itemconfigure(drawimg, image=img2)


    

    




def drawline():
    
    templine=draw.postscript(file='linetemp.eps')

def activate_Paint_Gcode(e):
    global linecount
    global lastx, lasty
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    cv.bind('<B1-Motion>', lambda event: Paint_Gcode(event, gcode))
    lastx, lasty = cv.canvasx(e.x), cv.canvasy(e.y)
      #cv.canvasx(e.x), cv.canvasy(e.y)
      


def activate_bucket(e):
    global lastx, lasty
    cv.bind('<Button-3>', bucket)
    lastx, lasty = cv.canvasx(e.x), cv.canvasy(e.y)


def activate_text(e):
    global lastx, lasty
    cv.bind('<Button-3>', place_text)
    lastx, lasty = cv.canvasx(e.x), cv.canvasy(e.y)


def activate_image(e):
    global lastx, lasty
    cv.bind('<Button-3>', place_image)
    lastx, lasty = cv.canvasx(e.x), cv.canvasy(e.y)
    





def Paint_Gcodeline(e):
    global lastx, lasty
    x, y = e.x, e.y
    cv.create_line((lastx, lasty, x, y), width=3,tags='tag1')
    draw.line((lastx, lasty, x, y), fill='red', width=1)
    lastx, lasty = x, y
def clear():
    cv.delete('all_lines')

def undoline():
    global linecount
    undoline=linecount-1
    print('delete'+"'"+str(undoline)+"'")
    cv.delete("'"+str(undoline)+"'")
    linecount=linecount-1

def exitt():
    exit()

def Paint_Gcodecolor():
    global hexstr
    (triple, hexstr) = askcolor()
    if hexstr:
        print(str(hexstr))
    cv.itemconfigure(draw, fill=hexstr)
    Paint_Gcodebutton.config( text = 'Pick Color')
    Paint_Gcodebutton["background"] = hexstr


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb
    hex1= rgb_to_hex((rgb1))
    
    
def Oil_Paint_Gcode(e, gcode):
    global linecount
    global hexstr
    global bsize
    global lastx, lasty
    global stroke_length
    
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x,bed_max_y
    bed_height =  bed_max_y
    bed_width= bed_max_x
    
    img2 = ImageTk.PhotoImage(Image.open("temp2.png"))
    cv.bind('<B1-Motion>', lambda event: Paint_Gcode(event, gcode))
    bsize = brush.get(1.0, "end-1c")
    x, y = e.x, e.y
    bed_x = x * (bed_width / canvas_width)
    bed_y = (canvas_height - y) * (bed_height / canvas_height)
    if lastx is not None and lasty is not None:
        cv.create_line(lastx, lasty, x, y, fill=hexstr, width=int(bsize), capstyle=ROUND, smooth=TRUE, splinesteps=120, tags=('all_lines', f"'{linecount}'"))
        draw.line((lastx, lasty, x, y), fill='green', width=4)
        print(f"create line '{linecount}' from ({lastx},{lasty}) to ({x},{y}) with brush size {bsize} and color {hexstr}")
        gcode_line = f"G1 X{bed_x:.2f} Y{bed_y:.2f} Z5 F{3000}\n"  # generate the G-code command
        print(f"G-code command: {gcode_line}")
        send_gcode(gcode_line)  # send the G-code command to the printer
        stroke_length += ((bed_x - last_bed_x)**2 + (bed_y - last_bed_y)**2)**0.5 # calculate the length of the stroke
        last_bed_x, last_bed_y = bed_x, bed_y # update the last bed coordinates
        if stroke_length >= 30: # refill the brush when it reaches a length of 30mm
            Gbrush_refill(None)
            stroke_length = 0 # reset the stroke length
        
        linecount += 1
    else:
        last_bed_x, last_bed_y = bed_x, bed_y # set the last bed coordinates
    
    lastx, lasty = x, y

    def key_released(e):
    
        send_gcode("G1 Z10") 
        cv.bind('<ButtonRelease-1>', key_released)
        global linecount
        print(f"end line '{linecount}' at ({lastx},{lasty})")
        linecount += 1

    cv.bind('<ButtonRelease-1>', key_released)
    
def activate_gcode():
      
    # Open serial port
    ser = serial.Serial('COM7', 250000)
    

    # Send G-code commands to the plotter
    gcode_commands = [
        "G21\n",   # Set units to millimeters
        "G90\n",   # Set absolute positioning
        "M82\n",   # Set extruder to absolute mode
        "M107\n",  # Turn off fan
        "G28\n",   # Home all axes
        "G92 E0\n",  # Reset extruder position
        "G1 Z2.0 F3000\n",  # Move the platform down a bit to start
        "G1 X0.0 Y0.0 F9000\n",  # Move the platform to the origin
        "G1 E30\n",  # Extrude 30mm of filament
        "G92 E0\n",  # Reset extruder position again
        "G1 F1400\n",  # Set movement speed
        "G1 Z40 F300 "
    ]
    for command in gcode_commands:
        ser.write(str.encode(command))
        with open('gcode_test.gcode', 'a') as f:
            f.write(command)

    # Set the feedrate
    ser.write(str.encode("G01 F8000\n"))


def Paint_Gcode(e, gcode):
    global linecount
    global hexstr
    global bsize
    global lastx, lasty
    
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    bed_width = 300
    bed_height = 300
    
    img2 = ImageTk.PhotoImage(Image.open("temp2.png"))
    cv.bind('<B1-Motion>', lambda event: Paint_Gcode(event, gcode))
    bsize = brush.get(1.0, "end-1c")
    x, y = e.x, e.y
    bed_x = x * (bed_width / canvas_width)
    bed_y = (canvas_height - y) * (bed_height / canvas_height)
    if lastx is not None and lasty is not None:
        cv.create_line(lastx, lasty, x, y, fill=hexstr, width=int(bsize), capstyle=ROUND, smooth=TRUE, splinesteps=120, tags=('all_lines', f"'{linecount}'"))
        draw.line((lastx, lasty, x, y), fill='green', width=4)
        print(f"create line '{linecount}' from ({lastx},{lasty}) to ({x},{y}) with brush size {bsize} and color {hexstr}")
        gcode_line = f"G1 X{bed_x:.2f} Y{bed_y:.2f} Z11.8 F{3000}\n"  # generate the G-code command #### Draw height
        print(f"G-code command: {gcode_line}")
        send_gcode(gcode_line)  # send the G-code command to the printer
        
        
        linecount += 1
    lastx, lasty = x, y
    
    def key_released(e):
    
        send_gcode("G1 Z20") ###TRAVEL HEIGHT 
        cv.bind('<ButtonRelease-1>', key_released)
        global linecount
        print(f"end line '{linecount}' at ({lastx},{lasty})")
        linecount += 1



    cv.bind('<ButtonRelease-1>', key_released)


   
def send_gcode(gcode_line):
    # Open serial port
    ser = serial.Serial('COM7', 250000)

    # Write the G-code command to the file
    with open('gcode_test4.gcode', 'a') as f:
        f.write(gcode_line)
 
    
    # go to travel height
    ser.write(gcode_line.encode()) 
    
def Gbrush_refill(event):
    # Get current mouse position
    x, y = event.x, event.y
    
    # Move the print head to Z10, stop, then go to (10, 10)
    gcode_line = "G1 Z10 F1000\n"
    send_gcode(gcode_line)

    send_gcode("G1 X10 Y10 F1000\n")
    time.sleep(0.001)
    # Move the print head to Z5, wait for 1 second, then move to Z10
    send_gcode("G1 Z3 F1000\n")

    send_gcode("G1 Z10 F1000\n")
  

    # Convert coordinates to bed size
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x,bed_max_y
    bed_width= bed_max_x
    bed_height =  bed_max_y
    bed_x = x * (bed_width / canvas_width)
    bed_y = (canvas_height - y) * (bed_height / canvas_height)

    # Move the print head back to the original position and send G-code command
    gcode_line = f"G1 X{bed_x:.2f} Y{bed_y:.2f} Z5 F{3000}\n"
    send_gcode(gcode_line)



def convert_and_print():
    # Load the image
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x,bed_max_y
    bed_size_x = bed_max_x 
    bed_size_y = bed_max_y
    feedrate=8000
    print_height=5
    line_start = None  # Coordinates of the start of the current line
    line_end = None  # Coordinates of the end of the current line

    # Load the image
    img = Image.open('temp2.png').convert('L')

    # Get the image dimensions in pixels
    img_width, img_height = img.size
    print('Image dimensions:', img_width, 'x', img_height)
    # Calculate the scaling factor
    # Calculate the scaling factors
    scaling_factor_x = bed_size_x / img_width
    scaling_factor_y = bed_size_y / img_height

    # Use the larger scaling factor to fill the bed in either X or Y direction
    scaling_factor = max(scaling_factor_x, scaling_factor_y)
    # Calculate the scaled dimensions
    scaled_width = int(img_width * scaling_factor)
    scaled_height = int(img_height * scaling_factor)
    print('Image dimensions:', scaled_width, 'x', scaled_height)

    # Scale the image
    img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    # Convert the image to G-code
    gcode_str = ''  # Initialize G-code string
    gcode_str += 'G21 ; Set units to millimeters\n'  # Set units to millimeters
    gcode_str += 'G90 ; Set absolute positioning\n'  # Set absolute positioning
    gcode_str += 'G28 ; Home all axes\n'  # Home all axes
    gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)  # Move up 5mm
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)  # Move to bottom left corner
    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)  # Move down to print

    # Initialize starting position and line state
    x_pos = 0
    y_pos = 0
    line_state = False

    is_printing = False  # A flag to keep track of whether the print head is currently down
    last_pos = None  # The last position where the print head was down
    for y in range(img.size[1]):
        x_pos = bed_size_x   # Scale the X-coordinate
        y_pos = bed_size_y - y   # Invert and scale the Y-coordinate
        gcode_str += 'G1 Y{:.3f} F{} ; Move to next row\n'.format(y_pos, feedrate)
        for x in range(img.size[0]):
            pixel_value = img.getpixel((x, y))
            if pixel_value > 50:  # Check if the pixel value is greater than 128 (white)
                if is_printing:
                    # If the print head is currently down, lift it up
                    gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                    gcode_str += 'G1 Z7 F{} ; Lift print head\n'.format(feedrate)
                    is_printing = False
            else:  # Pixel is black
                if not is_printing:
                    # If the print head is currently up, move to the start position of the new line
                    x_pos = x  # Scale the X-coordinate
                    gcode_str += 'G1 X{:.3f} F{} ; Move to print\n'.format(x_pos, feedrate)
                    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                    last_pos = (x_pos, y_pos)
                    is_printing = True
                else:
                    # If the print head is already down, continue the line
                    x_pos = x  # Scale the X-coordinate
                    if (x_pos - last_pos[0]) ** 2 + (y_pos - last_pos[1]) ** 2 >= 0.5 ** 2:
                        # If the next pixel is more than 0.5mm away from the current position, lift the print head and move to the new position
                        gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                        gcode_str += 'G1 X{:.3f} Y{:.3f} F{} ; Move to new line\n'.format(x_pos, y_pos, feedrate)
                        gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                        last_pos = (x_pos, y_pos)
                    else:
                        # If the next pixel is less than 0.5mm away from the current position, just continue the line
                        gcode_str += 'G1 X{:.3f} F{} ; Continue line\n'.format(x_pos, feedrate)
                        last_pos = (x_pos, y_pos)
    # If the last pixel of the image is not white, lift the print head
    if is_printing:
        gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
        gcode_str += 'G1 Z7 F{} ; Lift print head\n'.format(feedrate)

    # Finish the G-code
    gcode_str += 'G1 Z7 F{} ; Move up 5mm\n'.format(feedrate)
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
    gcode_str += 'M84 ; Turn off motors\n'

    # Save the G-code to    
    # Save the G-code to a file
    gcode_file= filedialog.asksaveasfilename(defaultextension='.gcode', filetypes=[('G-code files', '*.gcode')])
    with open(gcode_file, 'w') as f:
        f.write(gcode_str)
    
    print('G-code saved to:', gcode_file)
    plot_gcode('gcode_output7.gcode')



def plot_gcode(gcode_file):
    x_coords = []
    y_coords = []
    with open(gcode_file, 'r') as f:
        for line in f:
            if line.startswith('G1 '):
                if 'X' in line and 'Y' in line:
                    x_coords.append(float(line.split('X')[1].split()[0]))
                    y_coords.append(float(line.split('Y')[1].split()[0]))
    print(x_coords)
    print(y_coords)
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.plot(x_coords, y_coords)
    plt.show()


def smooth_print():
    # Load the image
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    
    from config3 import bed_max_x,bed_max_y
    bed_size_x = bed_max_x 
    bed_size_y = bed_max_y
    feedrate=8000
    print_height=5
    line_start = None  # Coordinates of the start of the current line
    line_end = None  # Coordinates of the end of the current line

    # Load the image
    img = Image.open('temp2.png').convert('L')

    # Get the image dimensions in pixels
    img_width, img_height = img.size
    print('Image dimensions:', img_width, 'x', img_height)
    # Calculate the scaling factor
    # Calculate the scaling factors
    scaling_factor_x = bed_size_x / img_width
    scaling_factor_y = bed_size_y / img_height

    # Use the larger scaling factor to fill the bed in either X or Y direction
    scaling_factor = max(scaling_factor_x, scaling_factor_y)
    # Calculate the scaled dimensions
    scaled_width = int(img_width * scaling_factor)
    scaled_height = int(img_height * scaling_factor)
    print('Image dimensions:', scaled_width, 'x', scaled_height)

    # Scale the image
    img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    # Convert the image to G-code
    gcode_str = ''  # Initialize G-code string
    gcode_str += 'G21 ; Set units to millimeters\n'  # Set units to millimeters
    gcode_str += 'G90 ; Set absolute positioning\n'  # Set absolute positioning
    gcode_str += 'G28 ; Home all axes\n'  # Home all axes
    gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)  # Move up 5mm
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)  # Move to bottom left corner
    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)  # Move down to print



    is_printing = False  # A flag to keep track of whether the print head is currently down
    last_pos = None  # The last position where the print head was down
    zigzag_direction = 1  # The direction of the zigzag motion (1 for right, -1 for left)
    for y in range(img.size[1]):
        x_pos = bed_size_x   # Scale the X-coordinate
        y_pos = bed_size_y - y   # Invert and scale the Y-coordinate
        gcode_str += 'G1 Y{:.3f} F{} ; Move to next row\n'.format(y_pos, feedrate)
        for x in range(img.size[0]):
            pixel_value = img.getpixel((x, y))
            if pixel_value > 128:  # Check if the pixel value is greater than 128 (white)
                if is_printing:
                    # If the print head is currently down, lift it up
                    gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                    gcode_str += 'G1 Z8 F{} ; Lift print head\n'.format(feedrate)
                    is_printing = False
            else:  # Pixel is black
                if not is_printing:
                    # If the print head is currently up, move to the start position of the new line
                    x_pos = x  # Scale the X-coordinate
                    gcode_str += 'G1 X{:.3f} F{} ; Move to print\n'.format(x_pos, feedrate)
                    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                    last_pos = (x_pos, y_pos)
                    is_printing = True
                else:
                    # If the print head is already down, continue the line
                    x_pos = x + zigzag_direction * 3  # Scale the X-coordinate and add zigzag motion
                    y_pos = y_pos + 3  # Add zigzag motion in the Y-axis
                    if (x_pos - last_pos[0]) ** 2 + (y_pos - last_pos[1]) ** 2 >= 0.5 ** 2:
                        # If the next pixel is more than 0.5mm away from the current position, lift the print head and move to the new position
                        gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                        gcode_str += 'G1 X{:.3f} Y{:.3f} F{} ; Move to new line\n'.format(x_pos, y_pos, feedrate)
                        gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                        last_pos = (x_pos, y_pos)
                        zigzag_direction = -zigzag_direction  # Reverse the direction of the zigzag motion
                    else:
                        # If the next pixel is less than 0.5mm away from the current position, just continue the line
                        gcode_str += 'G1 X{:.3f} Y{:.3f} F{} ; Continue line\n'.format(x_pos, y_pos, feedrate)
                        last_pos = (x_pos, y_pos)
                # If the last pixel of the image is not white, lift the print head
                if is_printing:
                    gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                    gcode_str += 'G1 Z8 F{} ; Lift print head\n'.format(feedrate)

        # Finish the G-code
        gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)
        gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
        gcode_str += 'M84 ; Turn off motors\n'
    
    # Save the G-code to    
    # Save the G-code to a file
    gcode_file= 'gcode_output3'  + '.gcode'
    with open(gcode_file, 'w') as f:
        f.write(gcode_str)
    
    print('G-code saved to:', gcode_file)
    plot_gcode('gcode_output3.gcode')
    
def zigzag_print():
    # Load the image
    canvas_width = cv.winfo_width()
    canvas_height = cv.winfo_height()
    from config3 import bed_max_x,bed_max_y
    bed_size_x = bed_max_x 
    bed_size_y = bed_max_y
    feedrate=8000
    print_height=5
    line_start = None  # Coordinates of the start of the current line
    line_end = None  # Coordinates of the end of the current line

    # Load the image
    img = Image.open('temp2.png').convert('L')

    # Get the image dimensions in pixels
    img_width, img_height = img.size
    print('Image dimensions:', img_width, 'x', img_height)
    # Calculate the scaling factor
    # Calculate the scaling factors
    scaling_factor_x = bed_size_x / img_width
    scaling_factor_y = bed_size_y / img_height

    # Use the larger scaling factor to fill the bed in either X or Y direction
    scaling_factor = max(scaling_factor_x, scaling_factor_y)
    # Calculate the scaled dimensions
    scaled_width = int(img_width * scaling_factor)
    scaled_height = int(img_height * scaling_factor)
    print('Image dimensions:', scaled_width, 'x', scaled_height)

    # Scale the image
    img = img.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    # Convert the image to G-code
    gcode_str = ''  # Initialize G-code string
    gcode_str += 'G21 ; Set units to millimeters\n'  # Set units to millimeters
    gcode_str += 'G90 ; Set absolute positioning\n'  # Set absolute positioning
    gcode_str += 'G28 ; Home all axes\n'  # Home all axes
    gcode_str += 'G1 Z6 F{} ; Move up 5mm\n'.format(feedrate)  # Move up 5mm
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)  # Move to bottom left corner
    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)  # Move down to print



    is_printing = False  # A flag to keep track of whether the print head is currently down
    last_pos = None  # The last position where the print head was down
    zigzag_direction = 1  # The direction of the zigzag motion (1 for up, -1 for down)
    for y in range(img.size[1]):
        x_pos = bed_size_x   # Scale the X-coordinate
        y_pos = bed_size_y - y   # Invert and scale the Y-coordinate
        gcode_str += 'G1 Y{:.3f} F{} ; Move to next row\n'.format(y_pos, feedrate)
        for x in range(img.size[0]):
            pixel_value = img.getpixel((x, y))
            if pixel_value > 128:  # Check if the pixel value is greater than 128 (white)
                if is_printing:
                    # If the print head is currently down, lift it up
                    gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                    gcode_str += 'G1 Z6 F{} ; Lift print head\n'.format(feedrate)
                    is_printing = False
            else:  # Pixel is black
                if not is_printing:
                    # If the print head is currently up, move to the start position of the new line
                    x_pos = x  # Scale the X-coordinate
                    gcode_str += 'G1 X{:.3f} F{} ; Move to print\n'.format(x_pos, feedrate)
                    gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                    last_pos = (x_pos, y_pos)
                    is_printing = True
                else:
                    # If the print head is already down, continue the line
                    y_pos = y_pos + zigzag_direction * 3  # Scale the Y-coordinate and add zigzag motion
                    x_pos = x  # Scale the X-coordinate
                    if (x_pos - last_pos[0]) ** 2 + (y_pos - last_pos[1]) ** 2 >= 0.5 ** 2:
                        # If the next pixel is more than 0.5mm away from the current position, lift the print head and move to the new position
                        gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                        gcode_str += 'G1 X{:.3f} Y{:.3f} F{} ; Move to new line\n'.format(x_pos, y_pos, feedrate)
                        gcode_str += 'G1 Z5 F{} ; Move down to print\n'.format(feedrate)
                        last_pos = (x_pos, y_pos)
                        zigzag_direction = -zigzag_direction  # Reverse the direction of the zigzag motion
                    else:
                        # If the next pixel is less than 0.5mm away from the current position, just continue the line
                        gcode_str += 'G1 X{:.3f} Y{:.3f} F{} ; Continue line\n'.format(x_pos, y_pos, feedrate)
                        last_pos = (x_pos, y_pos)

                        
                        
                        
                        
            # If the last pixel of the image is not white, lift the print head
            if is_printing:
                gcode_str += 'G1 Z{} F{} ; Move up\n'.format(print_height, feedrate)
                gcode_str += 'G1 Z6 F{} ; Lift print head\n'.format(feedrate)
    
    # Finish the G-code
    gcode_str += 'G1 Z10 F{} ; Move up 5mm\n'.format(feedrate)
    gcode_str += 'G1 X0 Y0 F{} ; Move to bottom left corner\n'.format(feedrate)
    gcode_str += 'M84 ; Turn off motors\n'
    
    # Save the G-code to    
    # Save the G-code to a file
    gcode_file= 'gcode_output6'  + '.gcode'
    with open(gcode_file, 'w') as f:
        f.write(gcode_str)
    
    print('G-code saved to:', gcode_file)
    plot_gcode('gcode_output6.gcode')        


def select_svg_file():
    # Create a pop-up window to select the SVG file

    root = tk.Tk()
    root.withdraw()
    importlib.reload(config3)
    svg_path = filedialog.askopenfilename(filetypes=[('SVG files', '*.svg')])
    root.destroy()

    # Pass the SVG file path to the load_svg() function
    load_svg(svg_path, cv)



def load_svg(svg_path, cv):
    # Set the path to the output GCode file
    gcode_path = filedialog.asksaveasfilename(defaultextension='.gcode', filetypes=[('G-code files', '*.gcode')])
    if not gcode_path:
        return
    global linecount
    
    # Convert the SVG file to GCode
    from config3 import Refill 
    import gcodegenerator_brush_refill
    
    if Refill == True:
        gcodegenerator_brush_refill.generate_gcode(svg_path, gcode_path)
    else:
        gcodegenerator.generate_gcode(svg_path, gcode_path) 
    # Print a success message
    print('GCode generated and saved to %s' % gcode_path)

    DEFAULT_DPI = 300


    # Extract X and Y coordinates from GCode file
    x_coords = []
    y_coords = []

    with open(gcode_path, 'r') as f:
        for line in f:
            if 'X' in line and 'Y' in line:
                match = re.findall(r'X([\d.]+).*Y([\d.]+).*Z([\d.]+)', line)
                if match:
                    x_coords.append(float(match[0][0]))
                    y_coords.append(float(match[0][1]))

    # Calculate the scaling factor based on the image width and height and default DPI
    image_width = max(x_coords)
    image_height = max(y_coords)
    if image_width == 0 or image_height == 0:
        scale_factor = 1
    else:
        scale_factor = (300 / DEFAULT_DPI) * (900 / max(image_width, image_height))


    # Scale the X and Y coordinates to fit on a 900 x 900 bed size
    scaled_x_coords = [x * scale_factor for x in x_coords]
    max_y = max(y_coords)
    scaled_y_coords = [(max_y - y) * scale_factor for y in y_coords]



    # Draw the rest of the lines on the canvas using the scaled X and Y coordinates
    for i in range(1, len(scaled_x_coords)):
        cv.create_line(scaled_x_coords[i-1], scaled_y_coords[i-1], scaled_x_coords[i], scaled_y_coords[i], fill='blue', width=1, capstyle=ROUND, smooth=TRUE, splinesteps=120, tags=('all_lines', f"'{linecount}'"))
        draw.line((scaled_x_coords[i-1], scaled_y_coords[i-1], scaled_x_coords[i], scaled_y_coords[i]), fill='blue', width=1)
        print(f"create line '{linecount}' from ({scaled_x_coords[i-1]},{scaled_y_coords[i-1]}) to ({scaled_x_coords[i]},{scaled_y_coords[i]}) with brush size 2 and color blue")
        linecount += 1




    # Update the image on the canvas
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    img3=Image.open("temp2.png")
    width2, height2 = scaled_x_coords,scaled_y_coords
    label.configure(image=img2)
    label.image=img2 
    cv.itemconfigure(drawimg, image = img2)
    cv.configure(width=900, height=900)
    cv.configure(bg="#000000")

def print_gcode_paths():
    print("generating G-code...")
    import time
    # Set the path and file name for the output G-code file
    gcode_path = 'temp.gcode'
    if not gcode_path:
        return

    # Prompt the user to select a G-code file
    gcode_file_path = filedialog.askopenfilename(filetypes=[('G-code files', '*.gcode')])
    if not gcode_file_path:
        return

    # Load the G-code file
    with open(gcode_file_path, 'r') as f:
        gcode_lines = f.readlines()

    # Send G-code line-by-line
    for line in gcode_lines:
        send_gcode(line)






            

                



def open_gcode_file():
    # Open a file dialog to select the gcode file
    file_path = filedialog.askopenfilename(filetypes=[('G-code files', '*.gcode')])
    if not file_path:
        return

    # Load the gcode file and extract the paths
    paths = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('G1'):
                coords = line.split()[1:]
                if coords[0][1:] and coords[1][1:]:
                    x, y = float(coords[0][1:]), float(coords[1][1:])
                    paths.append((x, y))

    # Find the maximum x and y coordinates to determine the size of the image
    max_x, max_y = max(paths, key=lambda p: p[0])[0], max(paths, key=lambda p: p[1])[1]

    # Set the scale factor to adjust the size of the image
    scale_factor = 5

    # Create a new PIL Image and draw the paths
    img = Image.new('RGB', (int(max_x * scale_factor) + 1, int(max_y * scale_factor) + 1), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    scaled_paths = [(x * scale_factor, y * scale_factor) for x, y in paths]
    draw.line(scaled_paths, fill='black', width=1)

    # Display the image
    img.show()

########## GENERATE GCODE ######################












#### PAINT TOOL ACTIVE############
def Paint(e):
    global linecount
    global lastx, lasty
    global hexstr
    global bsize
    bsize = brush.get(1.0, "end-1c")
    x, y = cv.canvasx(e.x), cv.canvasy(e.y)
    cv.create_line((lastx, lasty, x, y),fill=hexstr,width=int(bsize),capstyle=ROUND, smooth=TRUE, splinesteps=120, tags=('all_lines' , "'"+str(linecount)+"'"))
    draw.line((lastx, lasty, x, y), fill='green', width=4)
    print('create line'+"'"+str(linecount)+"'")
    lastx, lasty = x, y
    def key_released(e):
        global linecount
        print(str(x)+'x'+str(y)+'y')
        print("'"+str(linecount)+"'")
        linecount= linecount+1
        print('linecount'+str(linecount))

    cv.bind('<ButtonRelease-3>',key_released )
def activate_paint(e):
    global linecount
    global lastx, lasty
    
    
    img2=ImageTk.PhotoImage(Image.open("temp2.png"))
    cv.bind('<B3-Motion>', Paint)
    lastx, lasty = cv.canvasx(e.x), cv.canvasy(e.y)
      #cv.canvasx(e.x), cv.canvasy(e.y)



def bucket(e):
    
    global lastx, lasty
    global hexstr
    global bsize
    global rgb
    trs = ftres.get(1.0, "end-1c")
    x, y = cv.canvasx(e.x), cv.canvasy(e.y)
 
   
    lastx, lasty = x, y
    print(str(x)+'x'+str(y)+'y')
    imgA=Image.open('temp2.png')

    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    imgA.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()


    imgA.convert("RGB") 
    position=(x,y)
    [r,g,b1]=rgb
    alpha=255
    rgb2=r,g,b1,alpha
    print('picked fill color= '+str(rgb2))
    ImageDraw.floodfill(imgA,position, value=rgb2,thresh=int(trs))
    print('treshold= '+str(trs))
    imgA.save('temp2.png')
    img= ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img)
    label.image=img
    cv.itemconfigure(drawimg, image = img)


def place_text(e):
    
    global lastx, lasty
    global hexstr
    global bsize
    global rgb
    textbox = text_edit.get(0.3,END)
    pastetext=("'"+textbox+"'")
    txts = txtsize.get(1.0, "end-1c")
    x, y = cv.canvasx(e.x), cv.canvasy(e.y)
    lastx, lasty = x, y
    print(str(x)+'x'+str(y)+'y')
    imgA=Image.open('temp2.png')
    ###UNDO#############
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    imgA.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    ###############################

    imgA.convert("RGBA") 
    position=(x,y)
    [r,g,b1]=rgb
    alpha=255
    rgb2=r,g,b1,alpha
    print('text color= '+str(rgb2))

    I3 = ImageDraw.Draw(imgA)
    # Custom font style and font size
    myFont = ImageFont.truetype('\\font\\impact.ttf' , int(txts))
    print(textbox)
    I3.text((x, y-10),textbox, font=myFont, fill =(rgb2))

    print('textsize= '+str(txtsize))
    imgA.save('temp2.png')
    img= ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img)
    label.image=img
    cv.itemconfigure(drawimg, image = img)


def Fillcolor():
    global rgb
    
    (rgb,hexstrfill) = askcolor() 
    if rgb:
        print(('rgb=')+str(rgb))
    #cv.itemconfigure(draw, fill=hexstr)
    Fillbutton.config( text = 'FILL Color')
    Fillbutton["background"] = hexstrfill

def place_image2(e):
    
    global lastx, lasty
    global hexstr
    global bsize
    global rgb
    textbox = text_edit.get(0.3,END)
    pastetext=("'"+textbox+"'")
    txts = txtsize.get(1.0, "end-1c")
    x, y = cv.canvasx(e.x), cv.canvasy(e.y)
    lastx, lasty = x, y
    print(str(x)+'x'+str(y)+'y')
    imgA=Image.open('temp2.png')
    ###UNDO#############
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    imgA.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    ###############################

    imgA.convert("RGB") 
    position=(x,y)
    [r,g,b1]=rgb
    alpha=255
    rgb2=r,g,b1,alpha
    print('text color= '+str(rgb2))

    I3 = ImageDraw.Draw(imgA)
    # Custom font style and font size
    myFont = ImageFont.truetype('arialbd.ttf' , int(txts))
    print(textbox)
    I3.text((x, y-10),textbox, font=myFont, fill =(rgb2))

    print('textsize= '+str(txtsize))
    imgA.save('temp2.png')
    img= ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img)
    label.image=img
    cv.itemconfigure(drawimg, image = img)


def place_image(e):
    
    global lastx, lasty
    global hexstr
    global bsize
    global rgb
    
    textbox = text_edit.get(0.3,END)
    x, y = cv.canvasx(e.x), cv.canvasy(e.y)
    lastx, lasty = x, y
    print(str(x)+'x'+str(y)+'y')
    imgA=Image.open('temp2.png')
    ###UNDO#############
    undo = open("undo.txt","r")
    fn2=undo.read()
    fn3=int(fn2)
    fn4=fn3+1
    print(str(fn4))
    imgA.save('undo\\undo'+str(fn4)+'.png')
    undo.close()
    undo2 = open(r"undo.txt","w+")
    undo2.write(str(fn4))
    undo2.close()
    ###############################

    imgA.convert("RGB") 
    [r,g,b1]=rgb
    alpha=255
    rgb2=r,g,b1,alpha
    print('text color= '+str(rgb2))
    plimg = (Image.open(openfilename()))
 

    background = Image.open('temp2.png')
    foreground = plimg
    foreground = foreground.convert("RGBA")
    background.paste(foreground, (int(lastx), int(lasty)), foreground) 
    background.save('temp2.png')
    img= ImageTk.PhotoImage(Image.open("temp2.png"))
    label.configure(image=img)
    label.image=img
    cv.itemconfigure(drawimg, image = img)
    





def Configwindow():
   
    Config()
    
def Imagevectorbutton():
    
    Imagevector()

    
#appwindow.pack(pady=0) 
with Image.open('temp2.png') as img:
    width6, height6 = img.size
#START WINDOW###################################################################################################
win = tk.Toplevel(root,height=0 , width=0, bg="#263d42",cursor="circle", borderwidth=0)
win.geometry(str(width6)+'x'+str(height6)+'+'+'324+0')
win.attributes('-alpha', 1)
#win.wm_attributes("-transparentcolor", 'black')



bg=ImageTk.PhotoImage(Image.open("icon//bg3.png")) 
label2 = tk.Label(win,text= "Hello World", image = bg,anchor= CENTER) 
label2.place(x=0,y=0)

container = ttk.Frame(win, borderwidth=0)
img1 = ImageTk.PhotoImage(Image.open("temp2.png")) 
label = tk.Label(win,text= "Hello World", image = img1,anchor= CENTER)
label.image=img1
label.place(x=0,y=-5000)


lastx, lasty = None, None
linecount=0
hexstr=("#000000")
bsize=5
seed = (0, 0)
rgb=[255,255,255]


header1=Frame(win, height=53, width=x4*10,borderwidth=0)
header1.pack(side="top")
header1.config(bg="#263d42")

with Image.open('temp2.png') as img7:
    width8, height8 = img7.size

######### DRAW WINDOW
main=tk.Canvas(win, height=1700, width=1900, borderwidth=0)
cv = tk.Canvas(win ,bg='white', borderwidth=0)
image1 = Image.new('RGBA', (width8, height8), (0,0,0,0))
draw = ImageDraw.Draw(image1)
img3=ImageTk.PhotoImage(Image.open("temp2.png"))
drawimg=cv.create_image(0,0,image=img3, anchor="nw")



cv.pack()


#cvsave = Canvas(win, width=width6, height=height6, bg='white')
#cvsave.create_image(0,0,image=draw, anchor="nw", tag="sv")
#cvsave.pack(expand=NO)
##### WIN LABELS
shrink= Button(win,text="Shrink",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=image_shrink,borderwidth=1)
shrink.place(x=988,y=20)


Extend_frame= Button(win,text="+FRAME",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=extend_frame,borderwidth=1)
Extend_frame.place(x=988,y=0)


Extend_left= Button(win,text="Ext.Left",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=extend_left,borderwidth=1)
Extend_left.place(x=909,y=20)


Extend_right= Button(win,text="Ext.Right",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=extend_right,borderwidth=1)
Extend_right.place(x=909,y=0)


Extend_Bot= Button(win,text="Ext. Bottom",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=extend_bottom,borderwidth=1)
Extend_Bot.place(x=830,y=20)


Extend_Top= Button(win,text="Extent Top",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=extend_top,borderwidth=1)
Extend_Top.place(x=830,y=0)


##### WIN BUTTONS
placebutton= Button(win,text="Place IMG",bd=2,height=1, width=10, fg="white", bg="#263d42" , command=place_image,borderwidth=1)
placebutton.place(x=750,y=0)
placebutton.bind('<1>', activate_image,e)



text_edit = Text(win, width=20, height=3, wrap=CHAR,bd=2, bg="#263d42", fg="white")
text_edit.place(x=545,y=0)

Textbutton= Button(win,text="Text",bd=2,height=1, width=5, fg="white", bg="#263d42" , command=place_text)
Textbutton.place(x=710,y=20)
Textbutton.bind('<1>',activate_text,e)

txtsize = tk.Text(win,height =1,width = 5) 
txtsize.insert(END, '50')
txtsize.place(x=710, y=0)








save2= Button(win,text="BAKE LINES",bd=2,height=2, width=14, fg="white", bg="#263d42",  command=savedrawing)
save2.place(x=0,y=0)
Paint_Gcodebutton= Button(win,text="Paint_Gcode Color",bd=2,height=2, width=14, fg="white", bg=hexstr , command=Paint_Gcodecolor)
Paint_Gcodebutton.place(x=216,y=0)

### Paint_Gcode Bucket settings
Fillbutton= Button(win,text="Fill Color",bd=2,height=2, width=14, fg="white", bg=hexstr , command=Fillcolor)
Fillbutton.place(x=355,y=0)

Bucketbutton= Button(win,text="Fill",bd=2,height=2, width=7, fg="white", bg="#263d42" , command=bucket)
Bucketbutton.place(x=463,y=0)
Bucketbutton.bind('<1>',activate_bucket,e)





ftres = tk.Text(win,height =1,width = 3) 
ftres.insert(END, '70')
ftres.place(x=517, y=0)
text = Label(win, text="TRH",height=1, width=3,fg="#B2C3C7",bg="#263d42")
text.place(x=517,y=20)


###RESET
reset1=Button(win,text='Clear Lines',bd=2,height=2, width=14, fg="white", bg="#263d42" ,command=clear)
reset1.place(x=108,y=0)

### Pain Brush settings


brush = tk.Text(win,height =1,width = 3) 
brush.insert(END, '5')
brush.place(x=326, y=0)
text = Label(win, text="PX",height=1, width=3,fg="#B2C3C7",bg="#263d42")
text.place(x=326,y=20)

menubar = Menu(win)
menubar.add_command(label="SAVE", command=savefrog)
menubar.add_command(label="Exit", command=root.quit)
win.config(menu=menubar)



win.grid() 
win.bind('<1>',activate_Paint_Gcode,e)
win.bind('<3>',activate_paint,e)
# Bind the Gbrush_refill function to the 2 key
win.bind('2', Gbrush_refill)

#win.bind('<1>', lambda event: activate_live_Paint_Gcode(event, gcode))



####################################



##### READ MOUSE RGB #####################################################    
## END READ RGB MOUSE #######################################

menubar = Menu(root)
menubar.add_command(label="SAVE", command=savefrog)
menubar.add_command(label="Exit", command=root.quit)
root.config(menu=menubar)
####INPUT

inputtxt = tk.Text(root,height = 1,width = 8) 
inputtxt.insert(END, '10000')
inputtxt.place(x=0, y=660)

layerscale = tk.Text(root,height =1,width = 7) 
layerscale.insert(END, '100')
layerscale.place(x=0, y=280)

xscale = tk.Text(root,height =1,width = 5) 
xscale.insert(END, '1000')
xscale.place(x=0, y=520)

yscale = tk.Text(root,height =1,width = 5) 
yscale.insert(END, '1000')
yscale.place(x=58, y=520)


r= tk.Text(root,height =1,width = 4,) 
r.insert(END, '255')
r.place(x=216, y=280)

g = tk.Text(root,height =1,width = 4) 
g.insert(END, '255')
g.place(x=254, y=280)

b1 = tk.Text(root,height =1,width = 4) 
b1.insert(END, '255')
b1.place(x=292, y=280)


alpha = tk.Text(root,height =2,width = 6) 
alpha.insert(END, '128')
alpha.place(x=108, y=280)




#### BUTTONS ####################################################################################################################################################
loadimagebt= tk.Button(root, text="Paint_Gcode",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=activate_Paint_Gcode).place(x=216, y=0)
loadimagebt= tk.Button(root, text="Grab Tint",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=grab_tint).place(x=0, y=460)
loadimagebt= tk.Button(root, text="Grab Color",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=colorgrab_win).place(x=0, y=420)
loadimagebt= tk.Button(root, text="Blue",bd=2,height=2, width=14, fg="white", bg="#0075d0" , command=blue).place(x=108, y=420)
loadimagebt= tk.Button(root, text="Orange",bd=2,height=2, width=14, fg="white", bg="#df8800" , command=Orange).place(x=216, y=420)
loadimagebt= tk.Button(root, text="PickChroma",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=PickChroma).place(x=216, y=380)
loadimagebt= tk.Button(root, text="RGB Chroma",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=ColorChroma).place(x=216, y=340)
loadimagebt= tk.Button(root, text="Difference Layer",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=differencelayer).place(x=108, y=380)
loadimagebt= tk.Button(root, text="R G B Tint",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=colortint).place(x=216, y=300)
loadimageb= tk.Button(root, text="multiply Layer",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=multiplylayer).place(x=108, y=340)
loadimageb= tk.Button(root, text="Import alpha Layer",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=alphalayer).place(x=108, y=300)

loadimageb= tk.Button(root, text="Resize XY",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=customsize).place(x=0, y=540)
loadimageb= tk.Button(root, text="Import Layer",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=mergel100).place(x=0, y=300)
loadimageb= tk.Button(root, text="auto-size Layer",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=mergel).place(x=0, y=340)

loadimageb= tk.Button(root, text="Crop to box",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=cropbox).place(x=0, y=620)
loadimageb= tk.Button(root, text="Crop N-S",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=croptb).place(x=108, y=620)
loadimageb= tk.Button(root, text="Crop W-E",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=croplr).place(x=216, y=620)

loadimageb= tk.Button(root, text="+ Brightness",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=addbrightness).place(x=216, y=160)
loadimageb= tk.Button(root, text="- Brightness",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=redbrightness).place(x=216, y=200)
loadimageb= tk.Button(root, text="Edges ",bd=2,height=2, width=7, fg="white", bg="#263d42" , command=edge).place(x=108, y=240)
sharenb= tk.Button(root, text="Sharpen",bd=2,height=2, width=7, fg="white", bg="#263d42" , command=sharpen).place(x=158, y=240)
loadimageb= tk.Button(root, text="Detail",bd=2,height=2, width=7, fg="white", bg="#263d42" , command=deatil).place(x=270, y=240)
loadimageb= tk.Button(root, text="BLUR",bd=2,height=2, width=7, fg="white", bg="#263d42" , command=blur).place(x=216, y=240)
loadimageb= tk.Button(root, text="Load FROG #",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=loadFrognum).place(x=56, y=660)
loadimageb= tk.Button(root, text="- Hue",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=redhue).place(x=0, y=120)
loadimageb= tk.Button(root, text="+ Hue",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=addhue).place(x=0, y=80)
loadimageb= tk.Button(root, text="++ Saturation",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=addsat).place(x=216, y=80)
loadimageb= tk.Button(root, text="-- Sat",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=redsat).place(x=216, y=120)
loadimageb= tk.Button(root, text="16 colors",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=color16).place(x=0, y=160)
loadimageb= tk.Button(root, text="32 colors",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=color32).place(x=108, y=160)
loadimageb= tk.Button(root, text="4 colors",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=color4).place(x=0, y=200)
loadimageb= tk.Button(root, text="2 colors",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=color2).place(x=108, y=200)
loadimageb= tk.Button(root, text="2 X SIZE cubic",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=doublesize).place(x=108, y=540)
loadimageb= tk.Button(root, text="1/2 SIZE cubic",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=halfsize).place(x=216, y=540)
loadimageb= tk.Button(root, text="1/3 SIZE cubic",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=thirdsize).place(x=0, y=580)

blackandwhiteb= tk.Button(root, text="Black and White",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=bw).place(x=0, y=240)
saturationb= tk.Button(root, text=" + Contrast",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=addcontrast).place(x=108, y=80)
saturationb= tk.Button(root, text=" - Contrast",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=redcontrast).place(x=108, y=120)
sharenb= tk.Button(root, text="Sharpen",bd=2,height=2, width=14, fg="white", bg="#263d42" , command=sharpen).place(x=0, y=40)
# exit_button = tk.Button(root, text="Exit", height=2, width=14, fg="white", bg="#263d42" , command=root.destroy).place(x=216, y=400)
openfile= tk.Button(root, text="TAG",height=2, width=14, fg="white", bg="#263d42" ,command=tag ).place(x=216, y=660)
openfile= tk.Button(root, text="PIXEL ART",height=2, width=14, fg="white", bg="#263d42" ,command=pixelart ).place(x=108, y=580)
openfile= tk.Button(root, text="PIXEL AVATAR",height=2, width=14, fg="white", bg="#263d42" ,command=pixelavatar ).place(x=216, y=580)
randomhueb = tk.Button(root, text="Invert", height=2, width=14, fg="white", bg="#263d42" , command=invert).place(x=108, y=40)

resetb= tk.Button(root, text="Reset", height=2, width=6, fg="white", bg="#263d42" , command=reset).place(x=164, y=660)
savefile= tk.Button(root, text="Save", height=2, width=7, fg="white", bg="#263d42" , command=savefrog ).place(x=0, y=700)

config_button = tk.Button(root, text="Config", height=2, width=7, fg="white", bg="red" , command=Configwindow).place(x=0, y=740)
tracker_button = tk.Button(root, text="Imagevector", height=2, width=14, fg="white", bg="red" , command=Imagevectorbutton).place(x=59, y=740)


randomhueb = tk.Button(root, text="New File", height=2, width=7, fg="white", bg="#263d42" , command=newimage).place(x=162, y=700)
randomhueb = tk.Button(root, text="Blank", height=2, width=7, fg="white", bg="#263d42" , command=newempty).place(x=106, y=700)
randomhueb = tk.Button(root, text="Open", height=2, width=7, fg="white", bg="#263d42" , command=open_img).place(x=54, y=700)

loadimagebt= tk.Button(root, text="Undo",bd=2,height=2, width=14, fg="white", bg="#b90d00" , command=Undo).place(x=0, y=0)
loadimagebt= tk.Button(root, text="Redo",bd=2,height=2, width=14, fg="white", bg="#0075d0" , command=Redo).place(x=108, y=0)
loadimagebt= tk.Button(root, text="IMG to GCODE",bd=2,height=2, width=14, fg="white", bg="red" , command=convert_and_print).place(x=0, y=820)
loadimagebt= tk.Button(root, text="PaintBrush GCODE",bd=2,height=2, width=14, fg="white", bg="red" , command=smooth_print).place(x=108, y=820)
randomfrogb= tk.Button(root, text="CNC-->HOME",bd=2,height=2, width=14, fg="white", bg="red" , command=activate_gcode)########################
randomfrogb.place(x=216, y=700)
loadimagebt= tk.Button(root, text="ZIGZAG GCODE",bd=2,height=2, width=14, fg="white", bg="red" , command=zigzag_print).place(x=216, y=820)
loadimagebt= tk.Button(root, text="SVG to GCODE",bd=2,height=2, width=14, fg="white", bg="red" , command=select_svg_file).place(x=216, y=780)
loadimagebt= tk.Button(root, text="Print GCODE Paths",bd=2,height=2, width=14, fg="white", bg="red" , command=print_gcode_paths).place(x=108, y=780)
# Create a button in your tkinter app window that calls the select_svg_file() function when clicked
button = tk.Button(root, text='Select SVG file', command=select_svg_file)
button.pack()
loadimagebt= tk.Button(root, text="View GCODE",bd=2,height=2, width=14, fg="white", bg="red" , command=open_gcode_file).place(x=0, y=780)
#root.bind('<Motion>',callback)



root.bind("<Return>", frog)
root.bind("&lt;Control-s>", lambda evt: savedrawing())
root.bind("&lt;Control-z>", lambda evt: Undo())
root.bind("&lt;Control-z>", lambda evt: Redo())

root.mainloop()





