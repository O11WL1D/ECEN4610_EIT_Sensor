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

import average  # For averaging a single dataset

class EIT_reconstruct:
    def __init__ (self, data, reference = None, use_ref = 0, n_el = 4, use_shape = 3):
        self.n_el = n_el  # number of electrodes
        self.use_shape = use_shape
        self.data = data
        self.reference = reference
        self.use_ref = use_ref
    
    def Reconstruct(self):

        """ 0. Build mesh """
        if self.use_shape == 1:
            # Mesh shape is specified with fd parameter in the instantiation, e.g., fd=thorax
            # mesh_obj = mesh.create(n_el, h0=0.1, fd=thorax)
            mesh_obj = mesh.layer_circle(self.n_el, n_fan=15, n_layer=20)
            # n_fan and n_layer are adjusted to define the number of mesh elements
        elif self.use_shape == 2:
            """Regular circle"""
            mesh_obj = mesh.create(self.n_el, h0=0.04)
            # h0 -> determines the number of mesh elements
        elif self.use_shape == 3:
            """Unit circle mesh - Circular shape with distmesh similar to EIDORS"""
            """ #Note: Initially, you need to tweak plot_mesh.py and __init__.py to use this"""
            def _fd(pts):
                """Shape function"""
                return shape.circle(pts, pc=[0, 0], r=1.0)

            def _fh(pts):
                """Distance function"""
                r2 = np.sum(pts**2, axis=1)
                return 0.2 * (2.0 - r2)

            # Build fixed points, which may be used as positions for electrodes
            p_fix = shape.fix_points_circle(ppl=self.n_el)
            # The first num nodes are the positions for electrodes
            el_pos = np.arange(self.n_el)

            # Build triangle
            # p, t = distmesh.build(_fd, _fh, pfix=p_fix, h0=0.05)
            mesh_obj = mesh.create(fd=_fd, fh=_fh, p_fix=p_fix, h0=0.024)
            # plot_distmesh(p, t, el_pos)

        el_pos = mesh_obj.el_pos


        """ 1. FEM forward simulations """
        # Setup EIT scan conditions
        # Adjacent stimulation (dist_exc=1), adjacent measurements (step_meas=1)
        protocol_obj = protocol.create(self.n_el, dist_exc=1, step_meas=1, parser_meas="std")
        print("Mesh done...")


        """ 2. Naive inverse solver using back-projection """
        eit = bp.BP(mesh_obj, protocol_obj)
        eit.setup(weight="simple")  # It works better using this


        """ 3. Input Data """
        if self.use_ref == 1:     # Use existing reference data
            referenceData = np.array(self.reference)
            
        elif self.use_ref == 0:   # Create reference data from input data
            referenceData = average.ave(data=self.data, n_elec=self.n_el)

        print("Input Data Done...")


        """ 4. Inverse Problem """
        node_ds = 192.0 * eit.solve(self.data, referenceData, normalize=True)

        # Extract node, element, and alpha
        pts = mesh_obj.node
        tri = mesh_obj.element

        """ Plot Results """
        print("Plotting result...")
        # Draw the number of electrodes
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
        # Draw
        fig, axes = plt.subplots(1, 1, constrained_layout=True, figsize=(6, 6))

        # Reconstructed
        ax1 = axes
        ax1.set_title(r"Reconstituted $\Delta$ Conductivities")
        ax1.axis("equal")
        ax1.plot(pts[el_pos, 0], pts[el_pos, 1],"ro")
        im = ax1.tripcolor(
            pts[:, 0],
            pts[:, 1],
            tri,
            np.real(node_ds),
            # edgecolor="k", # To display mesh structure
            shading="flat",
            alpha=1,
            cmap=plt.cm.twilight_shifted,    # For colormap -> https://matplotlib.org/stable/gallery/color/colormap_reference.html
            norm = colors.CenteredNorm() # To prevent the colormap from shifting
            
            # If you want to increase contrast of the colormap ->
            # norm = colors.BoundaryNorm(boundaries=np.linspace(-13, 13, 6), ncolors=256, extend='both'),
            # cmap = 'RdBu_r'
        )
        # dot_num(pts, pts, ax1, pts[el_pos, 1])
        x, y = pts[:, 0], pts[:, 1]
        for i, e in enumerate(mesh_obj.el_pos):
            ax1.annotate(str(i + 1), xy=(x[e], y[e]), color="b")

        # 'tricontour' interpolates values on nodes, for example
        # ax.tricontour(pts[:, 0], pts[:, 1], tri, np.real(node_ds),
        # shading='flat', alpha=1.0, linewidths=1,
        # cmap=plt.cm.RdBu)
        fig.colorbar(im)
        # fig.colorbar(im, ax=axes.ravel().tolist())
        # mng = plt.get_current_fig_manager()
        # mng.full_screen_toggle()

        # plt.show()  # Don't forget to go full screen before closing if you want to save the image as fullscreen
        return plt.show()
        # fig.savefig('ReferensiRATARATA.png', dpi=96, bbox_inches='tight')
