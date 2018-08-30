
import math
import numpy as np
from Objects.BoundingBox import BoundingBox
from Utils.load_data import load_image
from Utils.settings import *
from Graphics.RotateTranslateImage import RTImage
import pygame
class Plateau:

    def __init__(self,startP,endP, path,img_scale_x = 1.0, img_scale_y = 1.0,  img_offset = [0,0]):
        self.start = startP[:]
        self.end = endP[:]
        self.center = [(self.start[i]+self.end[i])/2 for i in range(2)]
        self.center[1] += 2
        self.center[0] += 2
        self.dir = [(-self.start[i]+self.end[i]) for i in range(2)]
        self.len = math.sqrt(self.dir[0]**2+self.dir[1]**2)
        self.dir = [self.dir[0]/self.len,self.dir[1]/self.len]
        self.collision_width = 20
        self.path = path
        self.img = None
        self.flipped = False
        self.img_scale_x = img_scale_x
        self.img_scale_y = img_scale_y
        self.img_center = [0,0]
        self.img_offset = img_offset


    def add_img(self,img):
        img = pygame.transform.rotozoom(img ,0, 0.3)
        w = img.get_width()
        h = img.get_height()
        img = pygame.transform.smoothscale(img,
                                           (int(self.img_scale_x*w),
                                            int(self.img_scale_y*h)))
        if(self.flipped):
            img = pygame.transform.flip(img,True, False)

        self.img = RTImage(img)
        self.img_center = [self.start[0]+img.get_width()//2 + self.img_offset[0],self.start[1]+img.get_height()//2 + self.img_offset[1]]


    def get_perpendicular(self):
        perp = [-self.dir[1],self.dir[0]]
        if perp[1]<0:
            perp[1]=-1*perp[1]
            perp[0]=-1*perp[0]
        return perp

    def get_bounding_box(self):
        other_dir = np.array(self.get_perpendicular())
        return BoundingBox(np.array(self.center)+(self.collision_width/2)*other_dir,[self.dir,other_dir],[self.len/2,self.collision_width/2])

    def draw(self,screen,zoom,translate):
        if(self.img):
            screen.blit(*self.img.get_img(self.img_center,0,zoom,translate))
        if(DEBUG):
            pygame.draw.line(screen,[255,255,255],self.start,self.end,5)
