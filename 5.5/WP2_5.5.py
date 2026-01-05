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

def force_on_lug_propellant_tank(n_lugs_propellant, alpha): #LOIC AND INEZ 5.4 alpha angle between lugs in radians, can be chosen
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

def mass_scaling_propellant_lugs(forces_list_new):
                #Define constants
    #PREVIOUS BACKPLATE DATA
    #    PREVIOUS FORCES
    forces_list_old = [209.07, 195.98, 73.3] #N
    #  PREVIOUS DIMENSIONS
    mass_old = 0.009 #kg

    max_ratio = 0
    for i in range(len(forces_list_new)):
        force_old = forces_list_old[i]
        force_new = forces_list_new[i]
        current_ratio = force_new / force_old
        max_ratio = max(current_ratio, max_ratio)

    mass_new = mass_old * mass_ratio
    return mass_new

def total_mass_propellant_lugs(alpha):
    n_lugs_options = [2 , 4 , 6]  #calculations will be made with these values (times 2 because this is per side)
    # create empty list
    masses_per_lug = []  #this list will consist of the mass per lug that is needed for the amount of lugs option
    for n_option in n_lugs_options:
        forces = force_on_lug_propellant_tank(n_option, alpha)  #this is a list that consists of 4 lists of [fx, fy, fz]. There are 4 of them because these forces are different in the upper and lower lugs, and in two cases ([[forces_upper_CASE1, forces_lower_CASE1, forces_upper_CASE2, forces_lower_CASE2])
        max_lug_mass = 0
        for forces_list in forces:
            lug_mass = mass_scaling_propellant_lugs(forces_list)
            max_lug_mass = max(lug_mass, max_lug_mass)
        total_mass = n_option * 2 * max_lug_mass
        masses_per_lug += (max_lug_mass, total_mass)
    return masses_per_lug







