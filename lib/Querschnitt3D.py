import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm
import numpy as np
from .Layer import DammL,IntL
from .Raster import Raster
from qgis.core import *
from matplotlib import colormaps
from qgis.utils import iface
from qgis.gui import QgsVertexMarker
from qgis.PyQt.QtGui import QColor


class Querschnitt3D:
    def __init__(self,laenge,la,qb,path):
        laenge=round(laenge/10)*10
        self.raster=Raster(path)
        self.inten=IntL(path)
        p1,p2=self.inten.getPlPr(laenge)
        p3,p4=self.inten.getPlPr(laenge-10)
        p5,p6=self.inten.getPlPr(laenge-20)
        lx=p1.distance(p2)
        dx_=(p1.x()-p2.x())/lx
        dy_=(p1.y()-p2.y())/lx

        px=QgsPoint(p1.x()+dx_*la,p1.y()+dy_*la,0)

        llx=int((lx+2*la))
        X1 = np.arange(0, llx, 0.5)
        Y1 = np.arange(0, llx, 0.5)
        X, Y = np.meshgrid(X1, Y1)
        Z=X.copy()
        for x in X1:
            for y in Y1:
                x_=px.x()-dx_*x+y*dy_
                y_=px.y()-dy_*x-y*dx_
                if y<20:
                    pk=QgsPoint(x_,y_)
                    z_=self.raster.getValue(QgsPoint(x_,y_))
                  #  self.setMarker( pk,2)
                else:
                    z_=np.nan
                Z[int(x*2)][int(y*2)]=z_
        Y1 = np.array([0, llx/2, llx])
        X1 = np.array([0, 10, 20])
        Xq, Yq= np.meshgrid(X1, Y1) 
        Zq = self.CreateZ(p1.z(), p3.z(), p5.z(), Xq)   
        Ze = self.CreateZ(p1.m(), p3.m(), p5.m(), Xq)    
        Zb=  self.CreateZ(qb, qb, qb, Xq)     
        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(X, Y, Z,alpha=0.3,color='green',label='Gelaende',linewidth=0.5)
        ax.plot_surface(Xq, Yq, Zq,alpha=0.3,color='blue',label='Quote Abfluss',linewidth=0.5)
        ax.plot_surface(Xq, Yq, Ze,alpha=0.3,color='red',label='Energielinienhoehe',linewidth=0.5)
        if qb>0:
            ax.plot_surface(Xq, Yq, Zb,alpha=0.3,color='black',label='Bruecke',linewidth=0.5)
        plt.show()

    def CreateZ(self, p1, p3, p5, Xq):
        Zq=Xq.copy()
        Zq[0][0]=p1
        Zq[0][1]=p3   
        Zq[0][2]=p5
        Zq[1][0]=p1
        Zq[1][1]=p3   
        Zq[1][2]=p5    
        Zq[2][0]=p1
        Zq[2][1]=p3   
        Zq[2][2]=p5
        return Zq



    def setMarker(self, pk,col):
        pnt=QgsPointXY(pk.x(),pk.y())
        canvas = iface.mapCanvas()
        m = QgsVertexMarker(canvas)
        m.setCenter(pnt)
        m.setColor(QColor('Black'))
        m.setIconType(QgsVertexMarker.ICON_CIRCLE)
        m.setIconSize(4)
        m.setPenWidth(1)
        if col==1:
            m.setFillColor(QColor(0, 200, 0))
        if col==2:
            m.setFillColor(QColor(0, 0, 200))        
        if col==3:
            m.setFillColor(QColor(200, 0, 0))
        if col==4:
            m.setFillColor(QColor(0, 200, 200))   
"""
        X, Y = np.meshgrid(X1, Y1)
        for x in range(int(llx)):
            for y in range( int(llx)):
                X[x][y]=px.x()-dx/2*x
                Y[x][y]=px.y()-dy/2*y
"""             






"""
        plt.style.use('_mpl-gallery')
        # Make data
       
        X, Y = np.meshgrid(X1, Y1)
        Z=X.copy()
        for x in range(100):
            for y in range( 100):
                z=self.raster.getValue(QgsPoint(X[x][y],Y[x][y]))
                Z[x][y]=z   

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
"""