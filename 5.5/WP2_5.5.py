import numpy as np
import math

a_xtotal = 
a_ytotal = 
a_ztotal = 




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

    

    #Iterate for the number of panels
    for i in range(len(list_mass)):
        #Calculate new forces
        F_xnew = (a_xtotal*list_mass[i]/n_fasteners)
        F_ynew = (a_ytotal*list_mass[i]/n_fasteners)
        F_znew = (a_ztotal*list_mass[i]/n_fasteners)
        #Calculate force ratios
        X_ratio = F_xnew/ F_x
        Y_ratio = F_ynew/ F_y
        Z_ratio = F_znew/ F_z
        #Create empty list to store the ratios within the loop to reset it for each level
        Ratio_list = []
        #Append the ratios to the list
        Ratio_list.append(X_ratio)
        Ratio_list.append(Y_ratio)
        Ratio_list.append(Z_ratio)
        #Check which ratio is the largest, this will be the ratio used
        Useful_ratio = max(Ratio_list)
        #Calculate new dimensions
        W_new = W * Useful_ratio
        D_new = D * Useful_ratio
        H_new = H * Useful_ratio
        T_new = T * Useful_ratio
        #Calculate mass
        #Calculate forces on main cylindrical shell





