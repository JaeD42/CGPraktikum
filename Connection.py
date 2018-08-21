import numpy as np
import pygame
class Connection:

    def __init__(self,point1,point2,length,strength,max_force = -1):
        self.p1 = point1
        self.p2 = point2
        self.correct_length = float(length)
        self.strength = strength
        self.force = 0
        self.max_force = max_force
        self.color = pygame.Color(255,255,0,1)
        pos1 = self.p1.get_pos()
        pos2 = self.p2.get_pos()
        self.center = [(pos1[0]+pos2[0])/2,(pos1[1]+pos2[1])/2]

    #positive force: drags points to middle
    #negative force: push points away
    def update_force(self):
        length = self.p1.distance_to(self.p2)

        self.force = (length-self.correct_length)*self.strength

        pos1 = self.p1.get_pos()
        pos2 = self.p2.get_pos()
        self.center = [(pos1[0]+pos2[0])/2,(pos1[1]+pos2[1])/2]

    def get_color(self,start=[0,255,0],end=[255,0,0]):
        m = self.max_force
        if m==-1:
            m=100
        fac = min(float(abs(self.force))/m,1)
        col = [int(fac*end[i]+(1-fac)*start[i]) for i in range(3)]


        return tuple(col)



    def draw(self,surface,zoom=1,translation=[0,0]):
        pygame.draw.line(surface,self.get_color(),self.p1.get_int_pos(zoom,translation),self.p2.get_int_pos(zoom,translation))

    def get_center(self):
        return self.center
