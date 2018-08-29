import pygame
import numpy as np
class RTImage:

    def __init__(self,img,zoom=1.0,rotation=0):
        self.img = img
        self.last_img = img
        self.zoom = zoom
        self.rotation = rotation
        self.half_size = np.array([self.last_img.get_width()/2,self.last_img.get_height()/2])


    def update_image(self, img):
        self.img = img
        self.last_img = pygame.transform.rotozoom(self.img,self.rotation,self.zoom)

    def get_img(self,center,rotation,zoom,translation):
        if self.zoom != zoom or self.rotation!=rotation:
            self.rotation = rotation
            self.zoom = zoom

            self.last_img = pygame.transform.rotozoom(self.img,self.rotation,self.zoom)
            self.half_size = np.array([self.last_img.get_width()/2,self.last_img.get_height()/2])

        return (self.last_img, (center-self.half_size + translation)*zoom)

class RTImage_Connection:
    def __init__(self,img,length,zoom=1.0,rotation=0):
        self.img = img
        self.last_img = pygame.transform.rotozoom(self.img.subsurface(0,0,length,self.img.get_height()),rotation,zoom)
        self.length = length
        self.zoom = zoom
        self.rotation = rotation
        self.half_size = np.array([self.last_img.get_width()/2,self.last_img.get_height()/2])


    def update_image(self, img):
        self.img = img
        self.last_img = pygame.transform.rotozoom(self.img.subsurface(0,0,self.length,self.img.get_height()),self.rotation,self.zoom)

    def get_img(self,center,length,rotation,zoom,translation):
        if self.zoom != zoom or self.rotation!=rotation or self.length!=length:
            self.rotation = rotation
            self.zoom = zoom


            self.last_img = pygame.transform.rotozoom(self.img.subsurface(0,0,self.length,self.img.get_height()),self.rotation,self.zoom)
            self.half_size = np.array([self.last_img.get_width()/2,self.last_img.get_height()/2])

        return (self.last_img, (center-self.half_size + translation)*zoom)
