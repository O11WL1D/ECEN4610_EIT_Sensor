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

import pandas as pd


















# Generate random positions within a unit circle
def random_position_within_circle(radius=1.0):
    angle = np.random.uniform(0, 2 * np.pi)
    r = radius * np.sqrt(np.random.uniform(0, 1))
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    return np.array([x, y])





































# Simulate RSSI readings based on object position
def simulate_rssi_readings(sensor_positions, object_position, P_ref=-40, n=2):
    """
    Simulate RSSI readings based on distance from object to sensors.

    Parameters:
    - sensor_positions: List of sensor (x, y) positions.
    - object_position: (x, y) position of the object.
    - P_ref: Reference RSSI value at 1 meter (dBm).
    - n: Path loss exponent.

    Returns:
    - RSSI values for each sensor.
    """
    rssi_readings = []
    for sensor in sensor_positions:

        print("SENSOR POSITION")
        print(sensor)

        # Calculate the distance between the object and the sensor
        distance = np.linalg.norm(sensor - object_position)
        if distance == 0:  # Avoid log(0)
            distance = 0.01  # Set a small value to approximate close proximity
        # Compute RSSI using the log-distance path loss model

        rssi = P_ref - 10 * n * np.log10(distance)
        rssi_readings.append(rssi)

    print("\n--------readings:------", rssi_readings, "\n-------------------")
    return np.array(rssi_readings)























def plot_sensors_and_object(sensor_positions, object_position, rssi_readings):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title("Simulated RSSI Readings and Object Position")
    ax.set_aspect("equal")

    # Draw the unit circle
    circle = plt.Circle((0, 0), 1, color='black', fill=False, linestyle='--')
    ax.add_artist(circle)

    # Plot sensor positions
    sensor_positions = np.array(sensor_positions)
    ax.scatter(sensor_positions[:, 0], sensor_positions[:, 1], c='red', label='Sensors')

    # Annotate sensor positions with RSSI values
    for i, (x, y) in enumerate(sensor_positions):
        ax.annotate(f'{rssi_readings[i]:.1f} dBm', xy=(x, y), textcoords="offset points", xytext=(5, 5), color='blue')





    # Plot object position
    ax.scatter(object_position[0], object_position[1], c='green', label='Object', s=100)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.legend()
    plt.grid(True)
    plt.show()
    





















class EIT_reconstruct:
    def __init__(self, data, reference=None, use_ref=0, n_el=4, use_shape=2, object_position=None):
        self.n_el = n_el  # Number of electrodes
        self.use_shape = use_shape
        self.data = data
        self.reference = reference
        self.use_ref = use_ref
        self.object_position = object_position  # Store object position in the instance





    def Reconstruct(self):
        """ 0. Build Mesh """
        if self.use_shape == 1:
            mesh_obj = mesh.layer_circle(self.n_el, n_fan=15, n_layer=20)
        elif self.use_shape == 2:
            mesh_obj = mesh.create(self.n_el, h0=0.04)
        elif self.use_shape == 3:
            def _fd(pts):
                """ Shape function """
                return shape.circle(pts, pc=[0, 0], r=1.0)

            def _fh(pts):
                """ Distance function """
                r2 = np.sum(pts**2, axis=1)
                return 0.2 * (2.0 - r2)

            # Build fix points
            print("build fix points electrode count")
            print(self.n_el)
            #num electodes is 4 here. 

            p_fix = shape.fix_points_circle(ppl=self.n_el)
            el_pos = np.arange(self.n_el)









            # Build triangle mesh
            mesh_obj = mesh.create(fd=_fd, fh=_fh, p_fix=p_fix, h0=0.024)




        el_pos = mesh_obj.el_pos





        """ 1. FEM Forward Simulations """
        protocol_obj = protocol.create(self.n_el, dist_exc=1, step_meas=1, parser_meas="std")
        print("Mesh done...")




        """ 2. Naive Inverse Solver Using Back-Projection """
        eit = bp.BP(mesh_obj, protocol_obj)
        eit.setup(weight="simple")




        """ 3. Input Data """
        if self.use_ref == 1:
            referenceData = np.array(self.reference)
        elif self.use_ref == 0:
            referenceData = average.ave(data=self.data, n_elec=self.n_el)

        print("Input Data Done...")


        """ 4. Inverse Problem """
        node_ds = 192.0 * eit.solve(self.data, referenceData, normalize=True)



        # Extract node, element, alpha
        pts = mesh_obj.node
        tri = mesh_obj.element




        """ 5. Plot Results """
        print("Plotting result...")
        fig, ax1 = plt.subplots(1, 1, constrained_layout=True, figsize=(6, 6))




        # Reconstructed conductivity map
        ax1.set_title(r"Reconstituted $\Delta$ Conductivities")
        ax1.axis("equal")
        ax1.tripcolor(
            pts[:, 0],
            pts[:, 1],
            tri,
            np.real(node_ds),
            shading="flat",
            alpha=1,
            cmap=plt.cm.twilight_shifted,
            norm=colors.CenteredNorm(),
        )


        # Annotate electrodes
        x, y = pts[:, 0], pts[:, 1]
        for i, e in enumerate(el_pos):
            ax1.annotate(str(i + 1), xy=(x[e], y[e]), color="blue")

        fig.colorbar(ax1.tripcolor(
            pts[:, 0],
            pts[:, 1],
            tri,
            np.real(node_ds),
            shading="flat",
            alpha=1,
            cmap=plt.cm.twilight_shifted,
            norm=colors.CenteredNorm(),
        ))





         # Plot electrodes as red dots
        ax1.scatter(pts[el_pos, 0], pts[el_pos, 1], color="red", label="Electrodes")




        # Plot object position as a green dot
        if self.object_position is not None:
            ax1.scatter(
                self.object_position[0],
                self.object_position[1],
                color="green",
                label="Object Position",
                s=100,
            )
        ax1.legend()
        plt.show()































if __name__ == '__main__':
 # Generate random sensor positions
    sensor_positions = [random_position_within_circle() for _ in range(4)]
    print("Sensor Positions:", sensor_positions)

    # Place the object randomly within the circle
    object_position = random_position_within_circle()


    object_position=[0,0]

    print("Object Position:", object_position)



    # Simulate RSSI readings
    rssi_readings = simulate_rssi_readings(sensor_positions, object_position, P_ref=-40, n=2)

    print("Simulated RSSI Readings (dBm):", rssi_readings)



    #data = pd.read_csv('data.txt', delimiter='\t')
    #print(data)
    #print(data[0])

    #print("Data item 0 " + data[0])


    file = open('data.txt', 'r')
    data = file.read()
    
    #print(data)
    #print(data[0:6])
    #print(data[6])
    
    #-----------------------------------------------------------INPUT DATA SIZE HERE: 
    #this code will now feature the following assumptions:
    #n=number decimal size (this assumes negative sign and decimal point are considered a number and included in this count.)
    #n=size of datapoint+1    

    n=12
    n=n+1
    
    #print(data[0:n])
    #t=float(data[0:n])
    #print("float convo test "+ str(t))

    
    head=0
    tail=n

    print("START SEQENTIAL DATA READ")
    temparray=[]

    for x in range(12):
        print(x)
        print(data[head:tail])
        temparray.append(data[head:tail])
        #print("head :" + str(head))
        #print("tail : "+ str(tail))
        head=tail
        tail=tail+n




    #print(data[6])
    #print(data[7])



    
    #rssi_readings=np.array(data)

 



    rssi_readings=np.array(temparray)


    # Visualize the setup
    # plot_sensors_and_object(sensor_positions, object_position, rssi_readings)


    data = np.zeros(4)  # Placeholder for 16 electrodes
    for i, (pos, conductivity) in enumerate(zip(sensor_positions, rssi_readings)):
        data[i] = conductivity

    reference = np.mean(data) * np.ones_like(data)

    reference = [1.809055, 0.8100247, 0.3967621, 0.3232599, 0.2467575, 0.2371947, 0.2000686, 0.2242568, 0.2328821, 0.3315101, 0.4357633, 0.7938993, 1.722053]
    data = [1.650988, 0.8212751, 0.4367009, 0.3624485, 0.2718833, 0.2516327, 0.2049438, 0.2233193, 0.2266944, 0.3198848, 0.4170127, 0.7592107, 1.647988] 



    reconstruct = EIT_reconstruct(data=data, reference=reference, use_ref=1, n_el=4, object_position=object_position)
    reconstruct.Reconstruct()




#error message :Mesh done...
#C:\Users\dudkr\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\pyeit\eit\fem.py:117: UserWarning: The mesh use 16 electrodes, and the protocol use only 4 electrodes
#  self._check_mesh_protocol_compatibility(mesh, protocol)
#Input Data Done...
