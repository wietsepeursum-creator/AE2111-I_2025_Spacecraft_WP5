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
    W = 27.5 #mm
    D = 5 #mm
    H = 36 #mm
    T = 3 #mm
    Mass = 0.009 #kg

    #Create list with final dimensions and forces
    Results_list = []
    

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
        Mass_new = Mass * Useful_ratio**3
        #Calculate forces on main cylindrical shell, following conventions in reader
        #Positive x - right, y - in, z - down
        B_x = Mass_new * a_xtotal + F_xnew
        B_y = Mass_new * a_ytotal + F_ynew
        B_z = Mass_new * a_ztotal + F_znew
        #Take into account all attachemnts impose force on cylinder
        B_x = B_x * n_fasteners
        B_y = B_y * n_fasteners
        B_z = B_z * n_fasteners
        #Append results in list in said order, with every [i] being the level
        Results_list.append((W_new, D_new, H_new, T_new, B_x, B_y, B_z))
    return (Results_list)

def panel_weight(transverse_thickness, closing_thickness, width, depth, L, R, n_floors):1
    #transverse_thickness (thickness of the transverse panels) we should get from cian and liv, as well as the width, depth, L, R and n_floors, closing_thickness (thickness of the closing panels) we should get from can

        # Define constants
    #Properties of the materials
    t_core = 0.015  # m the thickness of the nomex core
    t_fabric = 0.00019805  # m thickness of weave fabric PER LAYER
    rho_core = 48.2  # kg/m^3
    rho_fabric = 1611  # kg/m^3

    #create empty list for the masses of all panels
    mass_list = []

            #CLOSING PANELS
    # calculate the amount of weave fabric layers that fit in the minimum thickness, rounded up
    n_fabric_closing = math.ceil((closing_thickness - t_core) / t_fabric)
    areas_closing_list = [ width * L, width * L, depth * L, depth * L, width * depth, width * depth]

    #for a specific closing panel, calculate the mass (based on area) and append to list
    for area in areas_closing_list:
        mass_closing_panel = area * (n_fabric_closing * t_fabric * rho_fabric + t_core * rho_core)
        mass_list += [mass_closing_panel]

           #TRANSVERSE PANELS
    # calculate the amount of weave fabric layers that fit in the minimum thickness, rounded up
    n_fabric_transverse = math.ceil((transverse_thickness - t_core) / t_fabric)
    area_transverse = width * depth - math.pi * R ** 2
    #calculate the mass of the transverse panels (they are all equal), and append them to the mass list
    for i in range(n_floors):
        mass_transverse = area_transverse* (n_fabric_transverse * t_fabric * rho_fabric + t_core * rho_core)
        mass_list += [mass_transverse]

    total_panel_mass = sum(mass_list)

    #function returns a list of the masses of all panels (look at the numbering image for indexes), and the total sandwich panel mass
    return mass_list, total_panel_mass

