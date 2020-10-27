#!/usr/bin/env python3

import random
from appJar import gui
import Voral as Voral
import numpy as np
import math
import os
from multiprocessing import cpu_count


##Defines the gui
win=gui("Cell_Split")
win.setFont(16)
win.setGeometry(2560,1440)

pth=os.getcwd()+'/Scans'
lst=[f for f in os.listdir(pth) if f.endswith('gif')]

##Defines function for push button
def Push(name):
    global c_lttr
    ##Prints to the terminal what button is pressed. For debugging mostly
    print(name + ' pushed')

    if name== "Show Scan":
        win.setImage("Vor_Split", os.getcwd()+'/Scans/A'+c_lttr +'.gif')
        return None
    if name== "Show Center":
        win.setImage("Vor_Split", os.getcwd()+'/Scans/B'+c_lttr+'.gif')
        return None
    if name== "Show Split":
        win.setImage("Vor_Split", os.getcwd()+'/Scans/C'+c_lttr+'.gif')
        return None

    ##if reset is pushed
    if name == "Reset":
        ##Set the height and width to the default
        height =500
        width =1000
        ##Set the sliders to their default scales
        win.setScale("Num_of_Points", initpoints, callFunction=True)
        win.setScale("X_Dist", width, callFunction=True)
        win.setScale("Y_Dist", height, callFunction=True)
        win.setEntry("P_Sp", 2.0, callFunction=False)
        ##Function to call a random placement of the coordinates
        Coordupdate(width,height)
        ##Calls the place nuclei function
        c_lttr=random.choice(lttr)
        Push("Display Scan")
        return None




    ##If exit is pushed
    if name == "Exit":
        ##Exit is called (kind of moot I guess, given the cross in the corner)
        win.stop()
        return None


    ##Get current numbers of points
    currpoints=win.getScale("Num_of_Points")
    Xlist=[]
    Ylist=[]
    ##Fill out the the coordinate lists
    for i in range(currpoints):
        Xlist.append(int(win.getEntry('x'+str(i))))
        Ylist.append(int(win.getEntry('y'+str(i))))
    ##Get the x and y distance for the canvas
    h=win.getScale("Y_Dist")
    w=win.getScale("X_Dist")
    ##If buttton is..
    if name == "Place Nuclei":
        ##Set image to the cute cartoon
        win.setImage("Vor_Split", "Minions.gif")

        ##Run the xy scatter and set image to that
        Voral.gen_coord(w, h, Xlist, Ylist)
        win.setImage("Vor_Split", "Nuclei.png")
        #win.zoomImage("Vor_Split",2)
        return None

    ##If go is pushed
    if name == "Go":
        ##Get the power for the Lebesgue space
        powr=win.getEntry("P_Sp")
        ##Returns error if a non convex space is selected
        if powr <1:
            msg=gui
            win.infoBox("P-Value error", "P value must be above or equal to one to have any real meaning in this context")
            return None
        ##Set image to the cute cartoon
        win.setImage("Vor_Split", "Minions.gif")
        ##Run the voronoi algorithm on the selected points and set to the output
        Voral.generate_voronoi_diagram(h,w,currpoints, powr,Ylist,Xlist)
        win.setImage("Vor_Split", "Diagram.png")
        #win.zoomImage("Vor_Split",2)
        return None




##This function updates the coordinates if the Y distance slider is changed
def Y_upd(value):
    height = win.getScale(value)
    print('Height changed to ' + str(height))
    width = win.getScale("X_Dist")
    Coordupdate(width,height)

##This function updates the coordinates if the X slider is changed
def X_upd(value):
    width = win.getScale(value)
    print('Width changed to ' + str(width))
    height = win.getScale("Y_Dist")
    Coordupdate(width,height)

##This updates the values of the coordinates at various stages such as when sliders are changed
def Coordupdate(w,h):
    ##Loop for Generating x and y values based on the size of the canvas. Each entry box has a key associated with it for retrival later
    for i in range(pointmax):
        x=random.randrange(w)
        y=random.randrange(h)
        win.setEntry('x'+str(i), x, callFunction=False)
        win.setEntry('y'+str(i), y, callFunction=False)


##This function is called every time the number of points is changed on the slider
def P_upd(value):
    ##This retrieves the value of the slider for the number of points in the slider
    spl=win.getScale(value)
    ##Outputs to the terminal the number of points (for debugging)
    print('Number of points changed to ' + str(spl))
    for i in range(pointmax):
        ##Blacks out unused fields
        if i < spl:
            win.showEntry('x'+str(i))
            win.showLabel('xin'+str(i))
            win.showLabel('yin'+str(i))
            win.showEntry('y'+str(i))
            win.setEntryBg('y'+str(i), "white")
            win.setEntryBg('x'+str(i), "white")
        else:
            win.setEntryBg('y'+str(i), "black")
            win.setEntryBg('x'+str(i), "black")
            win.hideEntry('x'+str(i))
            win.hideLabel('xin'+str(i))
            win.hideEntry('y'+str(i))
            win.hideLabel('yin'+str(i))
    #Push("Place Nuclei")



##Hard codes in the max points, initial number of points and initial size of the canvas
pointmax=30
initpoints=15
height =500
width =1000
lttr=['A','B','C','D','E','F']
c_lttr=random.choice(lttr)
##Starts frame, containing the inputs
win.startPanedFrame("Points/Settings",0,0)

##Add Scales for number of points, size of canvas and Lebesgue space value
win.setSticky("w")
win.addScale("Num_of_Points",0,3)
win.addNumericEntry("P_Sp",1,3)
win.addScale("X_Dist",2,3)
win.addScale("Y_Dist",3,3)
win.setEntryWidth('P_Sp',4)
win.setScaleWidth("Num_of_Points",20)
win.setScaleWidth("X_Dist",20)
win.setScaleWidth("Y_Dist",20)
win.setScaleLength("Num_of_Points",40)
win.setScaleLength("X_Dist",40)
win.setScaleLength("Y_Dist",40)




##Add Labels for the scales
win.setSticky("e")
win.addLabel("P_Spa", "P Value=",1,2)

win.addLabel("NP", "# of Points:",0,2)
win.addLabel("XD", "Plot Width=",2,2)
win.addLabel("YD", "Plot Height=",3,2)
win.setLabelWidth('P_Spa',10)
win.setLabelWidth('NP',10)
win.setLabelWidth('XD',10)
win.setLabelWidth('YD',10)
win.setSticky("w")


##Edits visual settings of sliders
win.showScaleValue("Num_of_Points", show=True)
win.showScaleValue("X_Dist", show=True)
win.showScaleValue("Y_Dist", show=True)

##Sets some initial values
win.setEntry("P_Sp", 2.0, callFunction=False)
win.setScaleRange("Num_of_Points", 2, pointmax)
win.setScaleRange("X_Dist", 800, 2000, curr=width)
win.setScaleRange("Y_Dist", 300, 1200, curr=height)

##Assigns functions to sliders
win.setScaleChangeFunction("X_Dist", X_upd)
win.setScaleChangeFunction("Y_Dist", Y_upd)
win.setScaleChangeFunction("Num_of_Points", P_upd)



##Buttons for Running programme/reseting and exiting
win.addButtons(["Place Nuclei","Go"], Push,0,1)
win.addButtons([["Reset","Show Scan"],[ "Show Center", "Show Split"]], Push,1,1)
win.addButton("Exit", Push,2,1)

##Configure buttons
win.setButtonBg("Go","green")
win.setButtonBg("Place Nuclei","green")
win.setButtonBg("Reset","yellow")
win.setButtonBg("Show Scan","yellow")
win.setButtonBg("Show Center","yellow")
win.setButtonBg("Show Split","yellow")
win.setButtonBg("Exit","red")


##For the hardcoded max coordinates, add entries for filling out those coordinates, and label them
for i in range(pointmax):
    win.setSticky("e")
    win.addLabel('xin'+str(i),"x=",i+4,0)
    win.addLabel('yin'+str(i),"y=",i+4,2)
    win.setSticky("w")
    win.addNumericEntry('x'+str(i),i+4,1)
    win.addNumericEntry('y'+str(i),i+4,3)
    win.setLabelWidth('xin'+str(i),2)
    win.setLabelWidth('yin'+str(i),2)
    win.setEntryWidth('x'+str(i),4)
    win.setEntryWidth('y'+str(i),4)


win.setSticky("nesw")
##Call the coordupdate function to fill them out
Coordupdate(width, height)

##Enter a new frame for the output
win.startPanedFrame("Output",0,1,1,2)
win.setSticky("nesw")
##Add the image to the output
win.addImage("Vor_Split", "Diagram.png")
win.setStretch('both')
#win.zoomImage("Vor_Split",2)

##Exit this frame
win.stopPanedFrame()
##Exit this part of the GUI
win.stopPanedFrame()


##Set the number of points to the initial points and call the function to identify the unused coordinates and paint it black
win.setScale("Num_of_Points", initpoints, callFunction=True)
Push("Show Scan")
print("Number of cores is: " + str(cpu_count()))
##Start the GUI
win.go()
