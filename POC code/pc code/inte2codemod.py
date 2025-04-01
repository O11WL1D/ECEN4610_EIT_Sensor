from __future__ import absolute_import, division, print_function

import matplotlib.pyplot as plt
import numpy as np
import pyeit.eit.jac as jac
import pyeit.mesh as mesh
from pyeit.eit.fem import EITForward
from pyeit.eit.interp2d import sim2pts
from pyeit.mesh.shape import thorax
import pyeit.eit.protocol as protocol
from pyeit.mesh.wrapper import PyEITAnomaly_Circle
from pyeit.eit.protocol import create
from tkinter import *
from PIL import ImageTk, Image
from matplotlib import colors

import average
import random
import serial
import time

#########################################################################################################################################################################################################
####################################################################################### Local Variables #################################################################################################
#########################################################################################################################################################################################################
calibrationReadings = np.array([])
rssiReadings = np.array([])
numElectrodes = 4

#########################################################################################################################################################################################################
########################################################################################### Calibrate ###################################################################################################
#########################################################################################################################################################################################################
def Calibrate(numElectrodes=numElectrodes):
    global calibrationReadings
    # Specify the correct serial port and baud rate
    arduino = serial.Serial(port='COM15', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
    time.sleep(2)  # Wait for Arduino to initialize

    numLoops = (numElectrodes - 2) * numElectrodes
    print(str(numLoops))
    while True:
        beginRead = arduino.readline().decode().strip()
        print("beginreadval: ", beginRead)
        if(beginRead == "1"):
            for iteration in range(numLoops):
                data = arduino.readline().decode().strip()
                print("data: ", data)
                calibrationReadings = np.append(calibrationReadings, int(float(data)))
        
            
        if(len(calibrationReadings) == numLoops):
            break

    arduino.close()

#########################################################################################################################################################################################################
############################################################################################# Image #####################################################################################################
#########################################################################################################################################################################################################

def repeater(numElectrodes=numElectrodes):
    while(True):
        time.sleep(1)
        Imaging(numElectrodes)
    
    

def Imaging(numElectrodes=numElectrodes):
    # Specify the correct serial port and baud rate
    global  rssiReadings
    rssiReadings=[]
    arduino = serial.Serial(port='COM15', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
    time.sleep(2)  # Wait for Arduino to initialize

    numLoops = (numElectrodes - 2) * numElectrodes
    print("num loops val:")
    print(numLoops)

    print("rssi value")
    print(rssiReadings)

    while True:

       

        beginRead = arduino.readline().decode().strip()
        print("beginreadval: ", beginRead)
        if(beginRead == "1"):
           for iteration in range(numLoops):
                #print(str(data))
                data = arduino.readline().decode().strip()
                print("data: ", data)
                rssiReadings = np.append(rssiReadings, int(float(data)))
        
        if(len(rssiReadings) == numLoops):
            break


    arduino.close()

    # 0. Build mesh & protocol (circle of where EIT occurs)
    meshObj = mesh.create(numElectrodes, h0=0.1)
    protocolObj = protocol.create(numElectrodes, dist_exc=0, step_meas=1, parser_meas="rotate_meas")

    # Extract node information
    pts = meshObj.node
    tri = meshObj.element
    x, y = pts[:, 0], pts[:, 1]

    # 1. Solve the inverse problem
    eit = jac.JAC(meshObj, protocolObj)
    eit.setup(p=0.2, lamb=0.001, method="kotre", perm=None, jac_normalized=True)
    solveInv = eit.solve(rssiReadings, calibrationReadings, normalize=True)
    physicalPts = sim2pts(pts, tri, np.real(solveInv))

    # 2. Plot EIT reconstruction
    fig, ax1 = plt.subplots(1, 1, constrained_layout=True, figsize=(6, 6))

    # Reconstructed conductivity map
    ax1.set_title(r"Reconstituted $\Delta$ Conductivities")
    ax1.axis("equal")
    ax1.tripcolor(
        pts[:, 0],
        pts[:, 1],
        tri,
        np.real(solveInv),
        shading="flat",
        alpha=1,
        cmap=plt.cm.twilight_shifted,
        norm=colors.CenteredNorm(),
    )

    # Annotate electrodes
    x, y = pts[:, 0], pts[:, 1]
    for i, e in enumerate(meshObj.el_pos):
        ax1.annotate(str(i + 1), xy=(x[e], y[e]), color="blue")

    fig.colorbar(ax1.tripcolor(
        pts[:, 0],
        pts[:, 1],
        tri,
        np.real(solveInv),
        shading="flat",
        alpha=1,
        cmap=plt.cm.twilight_shifted,
        norm=colors.CenteredNorm(),
    ))

    # Plot electrodes as red dots
    ax1.scatter(pts[meshObj.el_pos, 0], pts[meshObj.el_pos, 1], color="red", label="Electrodes")

    # Plot object position as a green dot
    '''ax1.scatter(
        anomalyPosition[0],
        anomalyPosition[1],s
        color="green",
        label="Object Position",
        s=100,
    )'''

    ax1.legend()
    plt.draw()  # Ensures the figure is drawn immediately
    plt.pause(1)  # Show for 5 seconds
    plt.close()




#########################################################################################################################################################################################################
############################################################################################## GUI ######################################################################################################
#########################################################################################################################################################################################################

root = Tk()
root.title('WELCOME TO PYEIT')

# Create and pack the button properly
button = Button(root, text='Calibrate', width=25, command=Calibrate)
button.pack(pady=10)  # Add some padding for better UI
button = Button(root, text='Image', width=25, command=repeater)
button.pack(pady=10)  # Add some padding for better UI

# Create canvas
canvas = Canvas(root, width=1000, height=500)
canvas.pack()

# Load image
# img = ImageTk.PhotoImage(Image.open("gui.jpg"))
# root.img = img  # Keep reference to prevent garbage collection
# canvas.create_image(20, 20, anchor=NW, image=img)

#root.after(0, helloCallBack)  # Runs after the event loop starts

root.mainloop()
