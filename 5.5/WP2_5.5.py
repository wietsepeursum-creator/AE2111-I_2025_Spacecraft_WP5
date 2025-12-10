import numpy as np
import math

def resultant_force(forces):
    res = math.sqrt(forces[0]**2 + forces[1]**2 + forces[2]**2)
    return res

