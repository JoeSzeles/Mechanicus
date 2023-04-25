    with Image.open('temp2.png') as img6:
        width6, height6 = img6.size
    print(str(width6)+'x'+ str(width6))

    cv.postscript(file="temp.eps")
  
    TARGET_BOUNDS = (width6, height6)
    pic = Image.open('temp.eps')
    pic.load(scale=10)
    ratio = min(TARGET_BOUNDS[0] / pic.size[0],
            TARGET_BOUNDS[0] / pic.size[0])
    new_size = (int((pic.size[0] * ratio)), int((pic.size[1] * ratio)))
    pic = pic.resize((width6+4, height6+4), Image.ANTIALIAS)
    #pic = pic.resize(new_size, Image.ANTIALIAS)
    #new_img = img5.resize((x, y, x + width5 , y + height5))
    pic.save('temp3.png')
    clear()
    im7 = Image.open('temp3.png')
    width7, height7 = im7.size
    im7.crop((0, 0, width7-4 , height7-4))
    im7.save('temp3.png')
    im8 = ImageTk.PhotoImage(Image.open('temp3.png'))
    label.configure(image=im8)
    label.image=im8
    cv.itemconfigure(drawimg, image = im8)
    cv.configure(width=width, height=height)


    def bucket(e):
    global linecount
    global lastx, lasty
    global hexstr
    global bsize
    x, y = e.x, e.y
    cv.create_line((lastx, lasty, x, y),fill=hexstr,width=bsize,capstyle=ROUND, smooth=TRUE, splinesteps=120, tags=('all_lines' , "'"+str(linecount)+"'"))
    draw.line((lastx, lasty, x, y), fill='green', width=4)
    print('create line'+"'"+str(linecount)+"'")
   
    lastx, lasty = x, y
    def key_released2(e):
        global linecount
        print(str(x)+'x'+str(y)+'y')
        print("'"+str(linecount)+"'")
        linecount= linecount+1
        print('linecount'+str(linecount))

    cv.bind('<ButtonRelease-3>',key_released2 )



    def bucket(e):
    global linecount
    global lastx, lasty
    global hexstr
    global bsize
    global RGBF
    x, y = e.x, e.y
    print('Paint Bucket'+"'"+str(linecount)+"'")
   
    lastx, lasty = x, y
    def key_released2(e):
        global linecount
        global RGBF
        print(str(x)+'x'+str(y)+'y')
        imgA=Image.open('temp2.png')
        imgA.convert("RGB") 
        position=(x,y)
        ImageDraw.floodfill(imgA,position, value = (0,0,0,0),thresh=50)
        imgA.save('temp2.png')
        img= ImageTk.PhotoImage(Image.open("temp2.png"))
        label.configure(image=img)
        label.image=img
        cv.itemconfigure(drawimg, image = img)

    cv.bind('<ButtonRelease-3>',key_released2 )