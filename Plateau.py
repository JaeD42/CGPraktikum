
import math
import numpy as np
from BoundingBox import BoundingBox
import pygame
class Plateau:

    def __init__(self,startP,endP):
        self.start = startP
        self.end = endP
        self.center = [(self.start[i]+self.end[i])/2 for i in range(2)]
        self.dir = [(-self.start[i]+self.end[i]) for i in range(2)]
        self.len = math.sqrt(self.dir[0]**2+self.dir[1]**2)
        self.dir = [self.dir[0]/self.len,self.dir[1]/self.len]
        self.collision_width = 100

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
        pygame.draw.line(screen,[255,255,255],self.start,self.end,5)
