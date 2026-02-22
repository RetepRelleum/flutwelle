import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm
import numpy as np
from .Layer import DammL,IntL
from .Raster import Raster
from qgis.core import *
from matplotlib import colormaps

class Querschnitt3D:
    def __init__(self,gname,path):
        self.raster=Raster(path)
        self.gname=gname
        self.inten=IntL(path)
        damm=DammL(self.gname)
        sel=damm.getSelected()
        
        if len(sel)>0:
                laenge =sel[0]['laenge']
                geom=sel[0].geometry().constGet()
                v=geom.vertices()
                pm=QgsPoint()
                for p in v:
                    pm=p
                    break
                plt.style.use('_mpl-gallery')
                # Make data
                X1 = np.arange(pm.x()-50, pm.x()+50, 1)
                Y1 = np.arange(pm.y()-50, pm.y()+50, 1)
                X, Y = np.meshgrid(X1, Y1)
                Z=X.copy()
                for x in range(100):
                    for y in range( 100):
                        z=self.raster.getValue(QgsPoint(X[x][y],Y[x][y]))
                        Z[x][y]=z 
          
                f=damm.damm.getFeatures()    
                la=[]
                ra=[]
                for x in range(8):    
                    p1,p2=self.inten.getPlPr(laenge-40+x*10)
                    la.append(p1)
                    ra.append(p2)
                v=[]
                v2=[]
                for p in la:
                    v.append([p.x(),p.y(),p.z()])
                    v2.append([p.x(),p.y(),p.m()])
                ra.reverse()
                for p in ra:
                    v.append([p.x(),p.y(),p.z()])
                    v2.append([p.x(),p.y(),p.m()])
               
                quadrat = [v]
                quadrat2 = [v2]

                # Plot the surface
                fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                ax.plot_surface(X, Y, Z,alpha=0.3,color='green',label='Gelaende',edgecolors='gray',linewidth=0.5)
                p3dc = Poly3DCollection(quadrat, alpha=0.6, facecolors =['blue'], edgecolors=['blue'],label='Quote Abfluss')
                ax.add_collection3d(p3dc)
                p3dc2 = Poly3DCollection(quadrat2, alpha=0.6,facecolors =['red'], edgecolors=['red'],label='Energielinienhoehe')
                ax.add_collection3d(p3dc2)
                plt.show()
               