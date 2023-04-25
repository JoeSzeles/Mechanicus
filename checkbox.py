import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def Imagevector():
    def open_image():
        # open file dialog to select image file
        filename = filedialog.askopenfilename(title="Select Image File", 
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        if filename:
            # open and display selected image
            img = Image.open(filename)
            img = img.resize((300, 300)) # resize image to fit window
            img_tk = ImageTk.PhotoImage(img)
            panel.config(image=img_tk)
            panel.image = img_tk # keep reference to prevent garbage collection
    
    # create main window
    root = tk.Tk()
    root.title("Imagevector")

    # create checkbox to enable image selection
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, text="Select Image", variable=checkbox_var)
    checkbox.pack()

    # create panel to display selected image
    panel = tk.Label(root)
    panel.pack()

    # bind checkbox to open_image function
    checkbox.config(command=open_image)

    # run main loop
    root.mainloop()

# run the Imagevector function to start the app
Imagevector()