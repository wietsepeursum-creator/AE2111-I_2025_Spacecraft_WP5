import numpy as np
import math


def new_dimensions(a_xtotal, a_ytotal, a_ztotal, n_fasteners, list_mass):
                #Define constants 
    #PREVIOUS BACKPLATE DATA
    #    PREVIOUS FORCES
    F_x = 104.54 #N "left"
    F_z = 36.65  #N "up" 
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
        
    