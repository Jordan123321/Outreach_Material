#!/usr/bin/env python3

##Import basic libraries
import random
import math
import numpy as np

##Matplotlib is for processing images into and out of python, and graphing
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
##Imports latex labels
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)


##Sets the file extension. Here PNG is used as the only format that is compatible with matplotlib and appjar
ext='.png'

mydpi=96
padding=50
fsize=21

##This function plots coordinates from the input of the GUI
def gen_coord(width, height, Xlst, Ylst):
    ##Generate the canvas
    image =np.zeros((width, height,3), dtype=np.uint8)
    ##Call the plotting fnct.
    f, ax = plt.subplots(figsize=((width+padding)/mydpi,(height+padding)/mydpi), dpi=mydpi)
    ##Label plot and axis
    ax.set_title(r'Scatter Plot of Cell Nuclei', fontsize=1.3333*fsize)
    ax.set_xlabel(r'X direction $\rightarrow$', fontsize=fsize)
    ax.set_ylabel(r'Y direction $\rightarrow$', rotation='vertical', fontsize=fsize)
    ax.tick_params(labelsize=15)
    ##Call Scatter Plot
    ax.scatter(Xlst,Ylst, c ='k',s=5)
    ##Set image limits
    ax.set_xlim([0,width])
    ax.set_ylim([0,height])
    plt.tight_layout()
    ##Save fig
    plt.savefig("Nuclei" + ext, dpi=mydpi ,interpolation='none')
    plt.close()
    ##Print Completion message (for debugging)
    print("Coordinates Plotted")

##This function generates the voronoi diagram images
def generate_voronoi_diagram(width, height, num_cells,powr,Xlst,Ylst):

    ##Makes empty canvas
    image =np.zeros((width, height,3), dtype=np.uint8)

    ##This sets random colours for the cells (nr=red, nb=blue, ng=green)
    nr=[]
    ng=[]
    nb=[]
    for i in range(num_cells):
        nr.append(random.randrange(70,256))
        ng.append(random.randrange(70,256))
        nb.append(random.randrange(70,256))
    ##Loop through the pixels
    for y in range(height):
        for x in range(width):
            ##Sets the minimum distance to the max on the canvas 
            dmin = ((abs(width-1))**(powr) +(abs(height-1))**(powr) )**(1/(powr))
            ##Sets a negative index to the initial value of the min for debugging
            j = -1
            ##Loop through the number of nuclei
            for i in range(num_cells):
                ##Find the p-space distance between the pixel and nuclei
                d = ((abs(Xlst[i]-x))**(powr) + (abs(Ylst[i]-y))**(powr) )**(1/(powr))
                ##if new minimum distance, change the minimum distance and assign pixel to that nuclei
                if abs(d) <= abs(dmin):
                    dmin = d
                    j = i
            ##Then set the canvas to the colour of that cell
            image[x, y,0],image[x, y,1],image[x, y,2]= nr[j], ng[j], nb[j]
    ##Call the plotting routine
    f, ax = plt.subplots(figsize=((height+padding)/mydpi,(width+padding)/mydpi), dpi=mydpi)
    ##Give a title and label axis
    if powr==2:
        ax.set_title(r"Cell Split of Region ", fontsize=1.3333*fsize)
    elif powr==1:
        ax.set_title(r'Cell Split of Region Using Taxicab Geometry', fontsize=1.3333*fsize)
    else:
        ax.set_title(r'Voronoi Split of Region Using the $L^{%s} $ Space' %(str(powr)), fontsize=1.3*fsize)
    ax.tick_params(labelsize=15)
    ax.set_xlabel(r'X direction $\rightarrow$', fontsize=fsize)
    ax.set_ylabel(r' Y direction $\rightarrow$', rotation='vertical', fontsize=fsize)
    ##Plot the image
    ax.imshow(image)
    ##Plot the nuclei
    ##Call Scatter Plot
    ax.scatter(Ylst,Xlst, c ='k',s=5)
    ##Set image limits
    ax.set_xlim([0,height])
    ax.set_ylim([0,width])
    plt.tight_layout()
    ##Save and close
    plt.savefig("Diagram"+ ext, dpi=mydpi)
    plt.close()
    ##Print done message for debugging
    print('done for power: ' + str(powr))

