from tkinter import *
import sys
import os



def helloCallBack():
    print("TESTING!")



from PIL import ImageTk, Image

root = Tk()
root.title('WELCOME TO PYEIT!!!!!')

# Create and pack the button properly
button = Button(root, text='Begin scan', width=25, command=helloCallBack)
button.pack(pady=10)  # Add some padding for better UI

# Create canvas
canvas = Canvas(root, width=1000, height=500)
canvas.pack()

# Load image
img = ImageTk.PhotoImage(Image.open("gui.jpg"))
root.img = img  # Keep reference to prevent garbage collection
canvas.create_image(20, 20, anchor=NW, image=img)

root.mainloop()




