#Support File for Task 5.3
import math as m 

import matplotlib.pyplot as plt

class Material:
    def __init__(self,E,v,rho,sigma_max):
        self.E = E
        self.v = v 
        self.density =rho
        self.max_stress = sigma_max


class Shell:
    def __init__(self, R, t, L):

        self.R = R
        self.t = t
        self.L = L 
        self.A = 2*m.pi*self.R*self.t
        self.I = self.R**3*m.pi*self.t

    def mass(self,density):
        return(self.R*m.pi*self.L*self.t*2*density)



AL2024T6 = Material(10.5e+6,0.33,2795.67,406.791)
AL7075 = Material(10.3e+6,0.33,2795.67,275.79)
Ti6Al4V = Material(16e+6,0.31,4428.78,827.371)
AISI201 = Material(28e+6,0.27,7999.4925,275.79)


def euler_buckling(Structure,Material):

    E = Material.E

    A = Structure.A
    L = Structure.L
    I = Structure.I

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


Stress =[]
thickness = []

#Assumed Values
shell = Shell(0.2,0.001,3)

for i in range(1,100,1):
    shell.t= 0.0001*i 
    sigma = shell_buckling(shell,AL7075,0.5)
    thickness.append(shell.t)
    Stress.append(sigma)

# Plot the sine and cosine lines in a graph
plt.plot(thickness, Stress)
# Add a title, axis labels, and a legend
plt.title('Shell Buckling vs Thickness at a fixed R')
plt.xlabel('t [m]')
plt.ylabel('shell stress, Mpa')


# Don't forget to call show()!
plt.show()
