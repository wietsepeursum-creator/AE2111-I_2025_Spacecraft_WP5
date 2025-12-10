#Support File for Task 5.3
import math as m 


class Shell:
    def __init__(self, R, t, L):

        self.R = R
        self.t = t
        self.L = L 
        self.A = 2*m.pi*self.R*self.t
        self.I = self.R**3*m.pi*self.t
    
    
shell = Shell(1,0.001,2)
print(shell.A)
print(shell.I)
