import numpy as np
import math

def resultant_force(forces):
    res = math.sqrt(forces[0]**2 + forces[1]**2 + forces[2]**2)
    return res

def angle_between_forces(force1, force2):
    dot_product = np.dot(force1, force2)
    magnitude1 = np.linalg.norm(force1)
    magnitude2 = np.linalg.norm(force2)
    cos_theta = dot_product / (magnitude1 * magnitude2)
    angle_rad = math.acos(cos_theta)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

