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