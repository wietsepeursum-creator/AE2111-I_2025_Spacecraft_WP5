import numpy as np
import math


def new_dimensions(a_xtotal, a_ytotal, a_ztotal, n_fasteners, list_mass):
                #Define constants
    #PREVIOUS BACKPLATE DATA
    #    PREVIOUS FORCES
    F_x = 209.07 #N "left"
    F_z = 73.3  #N "up" 
    F_y = 195.98  #N "out"
    #  PREVIOUS DIMENSIONS
    W = 15.2 #mm
    D = 2 #mm
    H = 36 #mm
    T = 3 #mm

    #Iterate for the nimber of panels
    for i in range(len(list_mass)):
        #Calculate new forces
        F_xnew = (a_xtotal*list_mass[i]/n_fasteners)
        F_ynew = (a_ytotal*list_mass[i]/n_fasteners)
        F_znew = (a_ztotal*list_mass[i]/n_fasteners)
        #Calculate force ratios
        X_ratio = F_xnew/ F_x
        Y_ratio = F_ynew/ F_y
        Z_ratio = F_znew/ F_z
        #Check which ratio is the largest, this will be the ratio used
        
    
