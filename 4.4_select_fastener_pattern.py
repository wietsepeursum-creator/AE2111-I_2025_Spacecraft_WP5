import math
import numpy as np
import matplotlib.pyplot as plt

def fastener_selection(w,size_outside_e1,size_outside_e2,min_size_inbetween,bolt_size_start, t_2_lug_start):
    number_of_bolts = 2
    size_inbetween = (w - 2 * size_outside_e1 * bolt_size_start) / (number_of_bolts - 1)


    if size_inbetween< min_size_inbetween:
        print("error, size inbetween not enough, change parameters!!")
        return

    while size_inbetween>= (min_size_inbetween * bolt_size_start):

        number_of_bolts+=1
        size_inbetween = (w - 2 * size_outside_e1 * bolt_size_start) / (number_of_bolts - 1)


    size_inbetween = (w - 2 * size_outside_e1 * bolt_size_start ) / (number_of_bolts - 2)
    layout={"number_of_bolts": number_of_bolts-1,
            "size_inbetween": size_inbetween,
            "size_outside_e1":size_outside_e1*bolt_size_start,
            "size_outside_e2":size_outside_e2*bolt_size_start,
            "bolt_size": bolt_size_start,
            "w": w,
            "t_2_lug": t_2_lug_start}
    return(layout)

def hole_coordinates(output, length,w): #the bottom left is set as the origin
    number_of_bolts = output["number_of_bolts"]
    e1=output["size_outside_e1"]
    e2=output["size_outside_e2"]
    spacing=output["size_inbetween"]

    holes=[]
    for n in range(number_of_bolts):
        x1=-length/2+ e2
        x2=length/2-e2
        z= -w/2 + e1 + n * spacing
        holes+=[(x1,z)]
        holes+=[(x2,z)]
    holes.sort()
    return holes

def cog_calculator(holes, layout):
    w=layout["w"]
    bolt_size_start=layout["bolt_size"]

    bolt_area=math.pi * bolt_size_start**2 /4
    x_cg=0
    z_cg=0
    for hole in holes:
        x_cg+= bolt_area *  hole[0]
        z_cg+= bolt_area* hole[1]
    x_cg=x_cg/ (len(holes)*bolt_area)
    z_cg=z_cg/ (len(holes)* bolt_area)
    return x_cg,z_cg

def forces(Fx_cg,Fz_cg, Cog, layout, holes):
    number_of_bolts=layout["number_of_bolts"]
    bolt_size_start=layout["bolt_size"]
    area=math.pi * bolt_size_start**2 /4
    Fx=Fx_cg/number_of_bolts
    Fz=Fz_cg/number_of_bolts
    z_cg=Cog[1]
    x_cg=Cog[0]
    My_cg=-z_cg * Fx_cg + x_cg * Fz_cg
    sum_Ar_squared=0
    loads_per_hole=[]
    for hole in holes:
        r= ( (hole[0]-x_cg)**2 + (hole[1]-z_cg)**2 ) **0.5
        if My_cg<=10**(-15):
            My_cg=0
        loads_per_hole+=[[hole, Fx,Fz, My_cg * area * r]]
        sum_Ar_squared+= area * r**2
    for loads_hole in loads_per_hole:
        loads_hole[3]=loads_hole[3]/sum_Ar_squared
    return loads_per_hole

def bearing_check(loads_per_hole, layout, material_choice):   # this code minimized the diameter of the bolts so that the maximum skin stress ( with safety factor) is not exceeded, and then calculates the minimum skinn thickness of fastener plate so that the max bearing stress is fine
    safety_factor=3
    bolt_size_start=layout["bolt_size"]
    t_2_lug=layout["t_2_lug"]/1000
     #units are now in meters and pa
    t_sc_skin= 0.00028448158
    max_bearing_stress=[965 * 10 **6, 415 * 10**6][material_choice] / safety_factor
    max_skin_stress= 1680 * 10**6 /safety_factor
    D=bolt_size_start /1000
    D_options = []
    for hole_loads in loads_per_hole: # here it calculates the smallest diameter the bolts can be for the max skin stress
        F_res = (hole_loads[1] ** 2 + hole_loads[2] ** 2) ** 0.5
        sigma_skin = F_res / (D * t_sc_skin)
        while sigma_skin<=max_skin_stress and D>=0.002:
            D -= 0.001
            sigma_skin = F_res / (D * t_sc_skin)
        D+=0.001
        D_options+=[D]
    D=max(max(D_options), 0.001) #bolt diameter cannot be smaller then 1 mm


    t_2_lug_options=[]
    for hole_loads in loads_per_hole:  #now it calculates how thick the fastener then needs to be to satisfy max bearing stress
        F_res = (hole_loads[1] ** 2 + hole_loads[2] ** 2) ** 0.5
        sigma_bearing= F_res  / (D * t_2_lug)
        t_2_lug = 1/(max_bearing_stress * D / F_res)
        t_2_lug_options+=[t_2_lug]
    t_2_lug=max(max(t_2_lug_options),0.002) #2 mm is set as the minimum thickness for the fastener plate, t2


    return D, t_2_lug



        
    
    
    
''' for hole_loads in loads_per_hole:
    F_res= ( hole_loads[1]**2 + hole_loads[2] **2 ) **0.5
    sigma_bearing= F_res/ (D* t_2_lug)
    sigma_skin= F_res/ (D*t_sc_skin)

    if ( sigma_bearing >= max_bearing_stress) or (sigma_skin>= max_skin_stress):
        print("ERROR IN STRESS FIX IT!!! :(")
        return false'''





def total(material_number, w, length, bolt_size_start, Fx_cg, Fz_cg, t_2_lug_start): #this is the definition that runs the total code, so the other defs dont need to be referenced when importing this code in your file. for now it outputs just the hole coordinates, but it will be modified to do all tasks later
    materials = ["metal", "composite"]
    size_outside_e1 = [2, 3][material_number]
    size_outside_e2 = [3, 4][material_number]
    min_size_inbetween = [2.5, 5][material_number]

    layout = fastener_selection(w, size_outside_e1, size_outside_e2, min_size_inbetween, bolt_size_start, t_2_lug_start)

    holes=hole_coordinates(layout,length,w)
    cog_location=cog_calculator(holes,layout)
    loads_per_hole= forces(Fx_cg, Fz_cg, cog_location, layout, holes)

    updated_D_and_T2=bearing_check(loads_per_hole, layout, material_number)
    layout["bolt_size"]= updated_D_and_T2[0]
    layout["t_2_lug"] = updated_D_and_T2[1]
    return updated_D_and_T2

print(total(0,10,50,1,0.17,0.77,3))

