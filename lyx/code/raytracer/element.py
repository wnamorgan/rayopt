import numpy as np
from abc import ABC, abstractmethod
from raytracer.ray import Ray
from raytracer.hit import Hit
from math import sin, cos
# === ABSTRACT ELEMENT CLASS ===
class Element(ABC):
    @abstractmethod
    def intersect(self, ray: Ray):
        pass

    @abstractmethod
    def redirect(self, ray: Ray, hit: Hit):
        pass

class Element(ABC):
    def __init__(self, material, center, orientation, name='element'):
        self.center = np.array(center, dtype=float)
        self.orientation = orientation
        self.material = material
        self.name = name
        self.R_G_from_L = Element.Euler_to_DCM(*orientation,deg=True) # DCM from local to global coordinates
        self.R_L_from_G = self.R_G_from_L.T


    def ray_local_from_global(self,ray_global):
        ray_local = ray_global.copy()
        ray_local.origin    = np.dot(self.R_L_from_G,(ray_global.origin - self.center).reshape(3,1)).reshape(3)
        ray_local.direction = np.dot(self.R_L_from_G,ray_global.direction.reshape(3,1)).reshape(3)
        return ray_local
    
    def ray_global_from_local(self,ray_local):
        ray_global = ray_local.copy()
        ray_global.origin    = self.center + np.dot(self.R_G_from_L,self.ray_local.origin.reshape(3,1)).reshape(3)
        ray_global.direction = np.dot(self.R_G_from_L,ray_local.direction.reshape(3,1)).reshape(3)
        return ray_global

    @abstractmethod
    def intersect(self, ray):
        pass

    @abstractmethod
    def normal(self, point):
        pass

    def redirect(self, ray, hit):
        return self.material.redirect(ray, hit)
    
    @staticmethod
    def Euler_to_DCM(yaw,pitch,roll,deg=False):
        R = np.zeros(shape=(3,3))
        if (deg == True):
            theta = np.deg2rad(pitch)
            psi   = np.deg2rad(yaw)
            phi   = np.deg2rad(roll)
        else:
            theta = pitch
            psi   = yaw
            phi   = roll
        R[0][0] =  cos(theta)*cos(psi)
        R[0][1] =  cos(theta)*sin(psi)
        R[0][2] = -sin(theta)
        R[1][0] =  sin(phi)*sin(theta)*cos(psi) - cos(phi)*sin(psi)
        R[1][1] =  sin(phi)*sin(theta)*sin(psi) + cos(phi)*cos(psi)
        R[1][2] =  sin(phi)*cos(theta)
        R[2][0] =  cos(phi)*sin(theta)*cos(psi) + sin(phi)*sin(psi)
        R[2][1] =  cos(phi)*sin(theta)*sin(psi) - sin(phi)*cos(psi)
        R[2][2] =  cos(phi)*cos(theta)
        return np.transpose(R) # Take transpose to get body to base DCM