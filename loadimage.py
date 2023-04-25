from PIL import ImageTk, Image
import tkinter as tk
from opentext import import_button
import_button()
class ImageViewer:
    def __init__(self, root, image_filename):
        self.root = root
        self.image_filename = image_filename

        self.root.title('ImageViewer')
        self.root.geometry('400x350')

        self.canvas = tk.Canvas(self.root, width=300, height=300)
        self.canvas.place(x=10, y=10)

        self.btnView = tk.Button(text='View', command=self.view_image)
        self.btnView.place(x=20, y=265)

        self.btnClose = tk.Button(text='close', command=self.root.destroy)
        self.btnClose.place(x=65, y=265)

    def view_image(self):
        self.img = ImageTk.PhotoImage(Image.open(self.image_filename))  # Keep ref to image.
        self.canvas.create_image(20, 20, anchor=tk.NW, image=self.img)


def main(image_filename):
    root = tk.Tk()
    ImageViewer(root, image_filename)
    root.mainloop()

if __name__ == '__main__':
    main(r"C:\Users\SteveSmith\eclipse-workspace\SteveSmith-ex1\src\raw\pythonIsFun.jpg")