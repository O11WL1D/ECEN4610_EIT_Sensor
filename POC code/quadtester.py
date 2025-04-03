from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import pyeit.eit.bp as bp
import pyeit.eit.protocol as protocol
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.mesh import shape, distmesh, plot_mesh
from pyeit.mesh.wrapper import PyEITAnomaly_Circle

import average  #Untuk merata-rata satu data aja

import serial
import time



from tkinter import *
import sys
import os











if __name__ == '__main__':
   

    
    reference = [1, 1, 1, 1]
    data=[1,1,1,1]







def helloCallBack():
    print("TESTING!")


    #read values from arduino serial monitor.
    
    # Specify the correct serial port and baud rate
    arduino = serial.Serial(port='COM15', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
    time.sleep(2)  # Wait for Arduino to initialize



    while True:
    # Read input from the user
    # Send the message to the Arduino

        beginread=arduino.readline().decode('utf-8', errors='ignore').strip()

        print(beginread)

        print("SENDING SCAN BREAK SIGNAL")
        #arduino.write("2".encode()) 

        arduino.write(b'2\n') 

        if(beginread=="1"):

    
        # Read response from Arduino (if any)
        
            data2=arduino.readline().decode().strip()
            data3=arduino.readline().decode().strip()
            data4=arduino.readline().decode().strip()
            data5=arduino.readline().decode().strip()
        

            print("data2", data2)
            print("data3", data3)
            print("data4", data4)
            print("data5", data5)


            data[0]=float(data2)
            data[1]=float(data3)
            data[2]=float(data4)
            data[3]=float(data5)


            print("SENDING SCAN BREAK SIGNAL")
            #arduino.write("2".encode()) 

            arduino.write(b'2\n') 

        

       
       
        else:
                print(beginread)




    


# Close the serial connection
    arduino.close()



   









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

#root.after(0, helloCallBack)  # Runs after the event loop starts

root.mainloop()





