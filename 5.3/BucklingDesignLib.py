#Support File for Task 5.3
import math as m 


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

a=1
shell = Shell(1,0.001,2)

AL2024T6 = Material(10.5e+6,0.33,2795.67,406.791)
AL7075 = Material(10.3e+6,0.33,2795.67,275.79)
Ti6Al4V = Material(16e+6,0.31,4428.78,827.371)
AISI201 = Material(28e+6,0.27,7999.4925,275.79)

print(shell.A)
print(shell.I)
