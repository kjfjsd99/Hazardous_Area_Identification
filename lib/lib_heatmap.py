import matplotlib.pyplot as plt
import numpy as np
import math
import os

# =============================================================================
def densityHeatmap(outputPath,fileName,person_transform,rectangle_transform,width_transform,height_transform,saveJPG=True,saveSVG=False):
    x=[]
    y=[]
    xr=[]
    yr=[]
    
    fig = plt.figure(figsize=(10,10)) #size bar
    plt.xlim(0,width_transform)
    plt.ylim(0,height_transform)
    
    #POINT DATASET (Persons)
    for (i,coordinate) in enumerate(person_transform):
        x.append(coordinate[0])
        y.append(coordinate[1])
    
    #POINT RECTANGLE: 0-->1-->2-->3-->0
    #(0)--(1)
    # |    |
    #(3)--(2)
    for (i,coordinate) in enumerate(rectangle_transform):
        xr.append(coordinate[0])
        yr.append(coordinate[1])
    xr.append(rectangle_transform[0][0])
    yr.append(rectangle_transform[0][1])

    #DEFINE GRID SIZE AND RADIUS(h)
    grid_size=1
    h=80
    
    #GETTING X,Y MIN AND MAX
    x_min=min(x)
    x_max=max(x)
    y_min=min(y)
    y_max=max(y)
    
    #CONSTRUCT GRID
    x_grid=np.arange(x_min-h,x_max+h,grid_size)
    y_grid=np.arange(y_min-h,y_max+h,grid_size)
    x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)
    
    #GRID CENTER POINT
    xc=x_mesh+(grid_size/2)
    yc=y_mesh+(grid_size/2)

    #FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
    def kde_quartic(d,h):
        dn=d/h
        P=(15/16)*(1-dn**2)**2
        return P

    #PROCESSING
    intensity_list=[]
    for j in range(len(xc)):
        intensity_row=[]
        for k in range(len(xc[0])):
            kde_value_list=[]
            for i in range(len(x)):
                #CALCULATE DISTANCE
                d=math.sqrt((xc[j][k]-x[i])**2+(yc[j][k]-y[i])**2) 
                if d<=h:
                    p=kde_quartic(d,h)
                else:
                    p=0
                kde_value_list.append(p)
            #SUM ALL INTENSITY VALUE
            p_total=sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)

    #HEATMAP OUTPUT    
    intensity=np.array(intensity_list)
    plt.pcolormesh(x_mesh,y_mesh,intensity,cmap="Reds")
    plt.plot(x, y, 'yo--', linewidth=0, markersize=20) #Plot y versus x as lines and/or markers 
    plt.plot(xr, yr, 'ro-', linewidth=1, markersize=0) #Plot y versus x as lines and/or markers 
    #plt.colorbar()
    plt.gca().invert_yaxis() #change origin
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False#label bottom = hide
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = False      #label top = hide
    plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False    #label left = hide
    plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = False  #label right = hide
    plt.show()
    
    if saveJPG:
        imgJPG = os.path.sep.join([outputPath, fileName+"_heatmap.jpg"])
        fig.savefig(imgJPG)
    if saveSVG:
        imgSVG = os.path.sep.join([outputPath, fileName+"_heatmap_SVG.svg"])
        fig.savefig(imgSVG)
