#Support File for Task 5.3
import math as m 

import matplotlib.pyplot as plt
from tabulate import tabulate

class Material:
    def __init__(self,E,v,rho,sigma_max,name):
        self.E = E
        self.v = v 
        self.density =rho
        self.max_stress = sigma_max
        self.name = name


class Shell:
    def __init__(self, R, t, L):

        self.R = R
        self.t = t
        self.L = L 
        
    def A(self):
        return(2*m.pi*self.R*self.t)
    def mass(self,material):
        return(self.R*m.pi*self.L*self.t*2*material.density)
    def I(self):
        return(self.R**3*m.pi*self.t)


AL2024T6 = Material(10.5e+6,0.33,2795.67,406.791,"AL2024T6")
AL7075 = Material(10.3e+6,0.33,2795.67,275.79,"AL7075")
Ti6Al4V = Material(16e+6,0.31,4428.78,827.371,"Ti6Al4V")
AISI201 = Material(28e+6,0.27,7999.4925,275.79,"AISI201")
Materials =[AL2024T6,AL7075,Ti6Al4V,AISI201]

def euler_buckling(Structure,Material):

    E = Material.E

    A = Structure.A()
    L = Structure.L
    I = Structure.I()

    sigma_max = Material.max_stress

    sigma_cr = ((m.pi**2*E*I)/(A*L**2))/10e6

    return(sigma_cr)

def shell_buckling(Structure,Material,pressure):

    L = Structure.L
    R = Structure.R
    t = Structure.t
    v = Material.v
    p = pressure
    E = Material.E


    lambda_min = ((L**2)/(m.pi**2*R*t))*m.sqrt(12*(1-v**2))

    K = lambda_min + (12/m.pi**4)*(L**4/(R**2*t**2))*(1-v**2)*(1/lambda_min)
    
    Q = (p/E)*(R/t)**2

    sigma_shell = (1.983-0.983*m.e**(-23.14*Q))*K*((m.pi**2*E)/(12*(1-v**2)))*(t**2/L**2)
    sigma_shell = sigma_shell/(10**6) #conversion to MPa
    return(sigma_shell)

Launch_force = 32000 #N roughly 800kg times a load factor of 4

results =[]

for MAT in Materials:
    found = False
    R_min = 0
    Stress_s =[]
    Stress_e = [] 
    thickness = []
    Radius = []
    Launch_stress = []

    #Assumed Values

    shell = Shell(0.2,0.03,2.7)

    for i in range(100,1500,10):
        shell.R= 0.001*i
        #shell.t = shell.R/10
        sigma_s = shell_buckling(shell,MAT,0.5)
        sigma_e = euler_buckling(shell,MAT)
        Radius.append(shell.R)
        Stress_s.append(sigma_s)
        Stress_e.append(sigma_e)
        sigma_l = (Launch_force/shell.A())/10**6
        Launch_stress.append(sigma_l)


        if (round(sigma_e,2) >= round(sigma_l,2)) and (round(sigma_s,2) >= round(sigma_l,2)) and not found:
            R_min = shell.R
            mass = shell.mass(MAT)   
            results.append([R_min,mass,MAT.name])
            found = True

    # Plot the sine and cosine lines in a graph
    plt.plot(Radius, Stress_s)
    plt.plot(Radius,Stress_e)
    plt.plot(Radius,Launch_stress)
    # Add a title, axis labels, and a legend
    plt.title('Stresses at varying R, using: ' + MAT.name)
    plt.xlabel('R [m]')
    plt.ylabel('shell stress, Mpa')
    plt.legend(('Shell', 'Euler','Launch'))

    # Don't forget to call show()!
    plt.show()


print(tabulate(results,headers=["R min [m]","Shell Mass","Material"]))