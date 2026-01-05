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

def panel_weight(transverse_thickness, closing_thickness, width, depth, L, R, n_floors): #LOIC AND INEZ 5.4
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

def force_on_lug_propellant_tank(n_lugs_propellant, alpha): #LOIC AND INEZ 5.4
            #DEFINE CONSTANTS
    m_propellant = 6.76 + 7.7  # kg, both tank and fuel
    g = 9.80665  # m/s^2
    ax_max = 2.5 * g
    ay_max = 1.8 * g
    az_max = 1.8 * g
    heigth_fuel_tank = 0.9128 - 0.171  # m, height minus diameter, since it is a cilinder with rounded ends
    radius_fuel_tank = 0.171 / 2 #m

    #simplify the name of the parameters
    r = radius_fuel_tank
    L = heigth_fuel_tank

            # CASE 1: Fy IS AT MAX AND Fz IS 0
    #calculate the Fx and Fy and Fz acting at the cog of the propellant tank, based on accelerations
    Fx = ax_max * m_propellant
    Fy = ay_max * m_propellant
    Fz = 0

    #divide Fx and Fy and Fz by 2, since the lugs are placed in 2 columns (see picture)
    Fx = Fx / 2
    Fy = Fy / 2
    Fz = Fz /2

        #CALCULATING REACTION FORCES ON 2 LUGS
    #reference Loic's calculation sheet to understand these equations
    #using coordinate system as in the reader
    R_upper_y = -r/L * Fx - 0.5 * Fy
    R_lower_y = r/L * Fx - 0.5 * Fy
    R_upper_x = 0.5 * Fx
    R_lower_x = 0.5 * Fx
    R_upper_z = 0
    R_lower_z = 0

    #create lists for the forces [Fx,Fy,Fz] per lug IN CASE 1:
    forces_upper_CASE1 = np.array([R_upper_x, R_upper_y, R_upper_z])
    forces_lower_CASE1 = np.array([R_lower_x, R_lower_y, R_lower_z])

    # if more than 2 lugs per column are used, distribute the force per lug over that amount
    forces_upper_CASE1 = forces_upper_CASE1 / n_lugs_propellant * 2
    forces_lower_CASE1 = forces_lower_CASE1 / n_lugs_propellant * 2


            # CASE 2: Fz IS AT MAX AND Fy IS 0
    # calculate the Fx and Fy and Fz acting at the cog of the propellant tank, based on accelerations
    Fx = ax_max * m_propellant
    Fy = 0
    Fz = az_max * m_propellant

    # divide Fx and Fy and Fz by 2, since the lugs are placed in 2 columns (see picture)
    Fx = Fx / 2
    Fy = Fy / 2
    Fz = Fz / 2

    # CALCULATING REACTION FORCES ON 2 LUGS
    # reference Loic's calculation sheet to understand these equations
    # using coordinate system as in the reader
    R_upper_y = - Fz/ ( 2 * math.tan(alpha/2) )
    R_lower_y = Fz/ ( 2 * math.tan(alpha/2) )
    R_upper_x = 0.5 * Fx
    R_lower_x = 0.5 * Fx
    R_upper_z = 0.5 * Fz
    R_lower_z = 0.5 * Fz


    # create array for the forces [Fx,Fy,Fz] per lug IN CASE 2:
    forces_upper_CASE2 = np.array([R_upper_x, R_upper_y, R_upper_z])
    forces_lower_CASE2 = np.array([R_lower_x, R_lower_y, R_lower_z])

    # if more than 2 lugs per column are used, distribute the force per lug over that amount
    forces_upper_CASE2 = forces_upper_CASE2 / n_lugs_propellant * 2
    forces_lower_CASE2 = forces_lower_CASE2 / n_lugs_propellant * 2
    return [forces_upper_CASE1, forces_lower_CASE1, forces_upper_CASE2, forces_lower_CASE2]

def mass_scaling_propellant_lugs(forces_list_new): #LOIC AND INEZ 5.4
    #This function takes as an input the forces that work on the lug in a specific configuration, and scales them with the old forces to calculate the mass of the new lug

    #DATA FROM PREVIOUS LUG
    #    PREVIOUS FORCES
    F_x_old = 489 #N
    F_y_old = 146.6 #N
    F_z_old = 146.6 #N
    resultant_old = (F_x_old**2 + F_y_old**2 + F_z_old**2)**0.5
    #  PREVIOUS DIMENSIONS
    mass_old = 0.009 #kg

    #DATA ON NEW LUG
    F_x_new = forces_list_new[0]
    F_y_new = forces_list_new[1]
    F_z_new = forces_list_new[2]
    resultant_new =  (F_x_new**2 + F_y_new**2 + F_z_new**2)**0.5

    #calculating the ratio between old and new forces
    ratio = resultant_new / resultant_old
    mass_new = mass_old * ratio
    #returns the new mass of lug in this configuration
    return mass_new

def total_mass_propellant_lugs(alpha):  #LOIC AND INEZ 5.4 FINAL FUNCTION, use this one for WEIGHT OF LUGS THAT ATTACH TO PROPELLANT TANK (it calls the other two)
    #FINAL FUNCTION THAT SHOULD BE CALLED FOR PROPELLANT LUGS MASS
    #it chooses the amount of lugs and calculates the total weight

    n_lugs_options = [2 , 4 , 6]  #calculations will be made with these amounts of lugs (times 2 because this is per side), and then in the end one of them is chosen
    # create empty list that will store the weight of each lug dependend on these options [2,4,6] above
    masses_per_lug = []

    for n_option in n_lugs_options:
        #call function that calculates loads on lugs based on the amount chosen
        forces = force_on_lug_propellant_tank(n_option, alpha)  #this is a list that consists of 4 lists of [fx, fy, fz]. There are 4 of them because these forces are different in the upper and lower lugs, and in two cases ([forces_upper_CASE1, forces_lower_CASE1, forces_upper_CASE2, forces_lower_CASE2])
        max_lug_mass = 0

        #calculate the mass for each of the entries in the force list [forces_upper_CASE1, forces_lower_CASE1, forces_upper_CASE2, forces_lower_CASE2]
        for forces_list in forces:
            lug_mass = mass_scaling_propellant_lugs(forces_list)
            #for each of the four entries it calculates the mass, and takes the highest mass
            max_lug_mass = max(lug_mass, max_lug_mass)

        #total mass is the mass per lug times the number of lugs times 2 (rows)
        total_mass = n_option * 2 * max_lug_mass
        #appends to the list
        masses_per_lug += [(max_lug_mass, total_mass)]

    total_mass = max(masses_per_lug)
    #return the total mass of all lugs in kg
    return total_mass[1]






