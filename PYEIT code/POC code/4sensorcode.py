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

















class EIT_reconstruct:
    def __init__ (self, data, reference = None, use_ref = 0, n_el = 4, use_shape = 2):
        self.n_el = n_el  # nb of electrodes
        self.use_shape = use_shape
        self.data = data
        self.reference = reference
        self.use_ref = use_ref
    
    def Reconstruct(self):

        """ 0. build mesh """
        if self.use_shape == 1:
            # Mesh shape is specified with fd parameter in the instantiation, e.g : fd=thorax
            # mesh_obj = mesh.create(n_el, h0=0.1, fd=thorax)
            mesh_obj = mesh.layer_circle(self.n_el, n_fan=15, n_layer=20)
            # n_fan dan n_layer diutak-atik buat jumlah mesh
        elif self.use_shape == 2:
            """Bulat biasa"""
            mesh_obj = mesh.create(self.n_el, h0=0.04)
            #h0 -> menentukan jumlah mesh
        elif self.use_shape == 3 :
            """unit circle mesh - Bulat dengan distmesh kyk eidors"""
            """ #Note: Buat make ini awal2 harus ngutak-ngatik di plot_mesh.py dulu, dan __init__.py nya"""
            def _fd(pts):
                """shape function"""
                return shape.circle(pts, pc=[0, 0], r=1.0)

            def _fh(pts):
                """distance function"""
                r2 = np.sum(pts**2, axis=1)
                return 0.2 * (2.0 - r2)

            # build fix points, may be used as the position for electrodes
            p_fix = shape.fix_points_circle(ppl=self.n_el)
            # firs num nodes are the positions for electrodes
            el_pos = np.arange(self.n_el)

            # build triangle
            #p, t = distmesh.build(_fd, _fh, pfix=p_fix, h0=0.05)
            mesh_obj = mesh.create(fd=_fd, fh=_fh, p_fix=p_fix, h0=0.024)
            #plot_distmesh(p, t, el_pos)

        el_pos = mesh_obj.el_pos


        """ 1. FEM forward simulations """
        # setup EIT scan conditions
        # adjacent stimulation (dist_exc=1), adjacent measures (step_meas=1)
        protocol_obj = protocol.create(self.n_el, dist_exc=1, step_meas=1, parser_meas="std")
        print("Mesh done...")


        """ 2. naive inverse solver using back-projection """
        eit = bp.BP(mesh_obj, protocol_obj)
        eit.setup(weight="simple")  #Lebih bagus pake ini


        """ 3. Input Data """
        if self.use_ref == 1:     #Use existing reference data
            referenceData = np.array(self.reference)
            

        elif self.use_ref == 0:   #Create reference data from data
            referenceData = average.ave(data=self.data, n_elec=self.n_el)

        print("Input Data Done...")


        """ 4. Inverse Problem """
        node_ds = 192.0 * eit.solve(self.data, referenceData, normalize=True)

        # extract node, element, alpha
        pts = mesh_obj.node
        tri = mesh_obj.element

        """ Plot Hasil """
        print("Plotting result...")
        #Draw the number of electrode
        def dot_num(x, y, axn, n):
            elect = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
            for i in range(len(n)):
                el2 = el_pos[i]
                el = elect[i]
                xi = x[el2, 0]
                yi = y[el2, 1]
                offset = 0.06
                if round(xi,3) > 0:
                    xt = xi+offset-0.04       
                elif round(xi,3) < 0:
                    xt = xi-offset
                else:
                    xt = xi
                
                if round(yi,3) > 0:
                    yt = yi+offset-0.04
                elif round(yi,3) < 0:
                    yt = yi-offset
                else:
                    yt = yi

                axn.annotate(el, xy=(xt,yt))
        # draw
        fig, axes = plt.subplots(1, 1, constrained_layout=True, figsize=(6, 6))

        # reconstructed
        ax1 = axes
        ax1.set_title(r"Reconstituted $\Delta$ Conductivities")
        ax1.axis("equal")
        ax1.plot(pts[el_pos, 0], pts[el_pos, 1],"ro")
        im = ax1.tripcolor(
            pts[:, 0],
            pts[:, 1],
            tri,
            np.real(node_ds),
            #edgecolor="k", #Buat nampilin bentuk mesh
            shading="flat",
            alpha=1,
            cmap=plt.cm.twilight_shifted,    #For colormap -> https://matplotlib.org/stable/gallery/color/colormap_reference.html
            norm = colors.CenteredNorm() #Biar colormap nya gk geser2
            
            #Kalo mau warnanya di kontrasin ->
            #norm = colors.BoundaryNorm(boundaries=np.linspace(-13, 13, 6), ncolors=256, extend='both'),
            #cmap = 'RdBu_r'
        )
        #dot_num(pts, pts, ax1, pts[el_pos, 1])
        x, y = pts[:, 0], pts[:, 1]
        for i, e in enumerate(mesh_obj.el_pos):
            ax1.annotate(str(i + 1), xy=(x[e], y[e]), color="b")

        # 'tricontour' interpolates values on nodes, for example
        # ax.tricontour(pts[:, 0], pts[:, 1], tri, np.real(node_ds),
        # shading='flat', alpha=1.0, linewidths=1,
        # cmap=plt.cm.RdBu)
        fig.colorbar(im)
        #fig.colorbar(im, ax=axes.ravel().tolist())
        #mng = plt.get_current_fig_manager()
        #mng.full_screen_toggle()

        #plt.show()  #Jangan lupa di Full screen dulu baru di close kalo mau disave image nya fullscreen
        return plt.show()
        #fig.savefig('ReferensiRATARATA.png', dpi=96, bbox_inches='tight')

if __name__ == '__main__':
   








    
    file = open('data.txt', 'r')
    data = file.read()
    
    
    n=12
    n=n+1
    

    
    
    head=0
    tail=n

    print("START SEQENTIAL DATA READ")
    temparray=[]

    for x in range(4):
        print(x)
        print(data[head:tail])
        temparray.append(data[head:tail])
        #print("head :" + str(head))
        #print("tail : "+ str(tail))
        head=tail
        tail=tail+n



    
    reference = [1, 1, 1, 1]
    data=[1,1,1,1]


    for x in range(4):
        data[x]=(float  )(temparray[x][0:6]);
    

    #data = np.array(temparray)

    print("DATA ARRAY!")
    print(data)




    print("datalen")
    print(len(data))
    #data = [0.55] * len(data)  # Replace with 0.55






def helloCallBack():
    print("TESTING!")


    #read values from arduino serial monitor.



    reconstruct = EIT_reconstruct(data=data, reference=reference, use_ref=1, n_el=4)
    reconstruct.Reconstruct()










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





