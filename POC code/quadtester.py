from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np





import serial
import time



from tkinter import *
import sys
import os




from PIL import Image





import cv2





img1 = Image.open("q1.jpg")
img2 = Image.open("q2.jpg")
img3 = Image.open("q3.jpg")
img4 = Image.open("q4.jpg")







if __name__ == '__main__':
   

    
    reference = [1, 1, 1, 1]
    data=[1,1,1,1]







def helloCallBack():
    print("TESTING!")


    #read values from arduino serial monitor.
    
    # Specify the correct serial port and baud rate
    arduino = serial.Serial(port='COM15', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
    time.sleep(2)  # Wait for Arduino to initialize


    toggle=1

    while True:
    # Read input from the user
    # Send the message to the Arduino

        beginread=arduino.readline().decode('utf-8', errors='ignore').strip()

        print(beginread)




        if(toggle==1):
            print("SENDING CALIBRATE SIGNAL")
            arduino.write(b'1\n') 
            toggle=0
            time.sleep(3)

        


        if(toggle==0):
            print("SENDING SCAN SIGNAL")
            arduino.write(b'2\n') 
        





        allfalse=1

        if(beginread=="1"):

    
        # Read response from Arduino (if any)
        

            img1.show()
            #cv2.imshow("Image", img1)
         
            allfalse=0

            iinput = input("type anything to continue to perform another scan")

              
 



        if(beginread=="2"):

    
        # Read response from Arduino (if any)
        
   
            
            img2.show()
            allfalse=0
            iinput = input("type anything to continue to perform another scan")

              
    

        if(beginread=="3"):

    
        # Read response from Arduino (if any)
        
     
            img3.show()
            allfalse=0
            iinput = input("type anything to continue to perform another scan")

              
     

        if(beginread=="4"):

    
        # Read response from Arduino (if any)
        
        
            img4.show()
            allfalse=0
            iinput = input("type anything to continue to perform another scan")
  


        if(allfalse==0):
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





