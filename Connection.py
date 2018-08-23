import numpy as np
import pygame
from BoundingBox import BoundingBox
from settings import DEBUG
class Connection:

    def __init__(self,point1,point2,length,strength,max_force = 1000, can_collide = False):
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
        self.dir = pos1-pos2
        self.len = np.sqrt(np.dot(self.dir,self.dir))
        self.dir = self.dir/self.len
        self.can_collide=can_collide
        self.line_width = 1
        self.collision_width = 50

    #positive force: drags points to middle
    #negative force: push points away
    def update_force(self):
        length = self.p1.distance_to(self.p2)

        self.force = (length-self.correct_length)*self.strength

        pos1 = self.p1.get_pos()
        pos2 = self.p2.get_pos()
        self.center = (pos1+pos2)/2
        self.dir = pos1-pos2
        self.len = np.sqrt(np.dot(self.dir,self.dir))
        self.dir = self.dir/self.len


        if abs(self.force)>self.max_force:
            self.p1.connections.remove(self)
            self.p2.connections.remove(self)
            return True
        return False

    def get_color(self,start=[0,255,0],end=[255,0,0]):
        if DEBUG:
            m = self.max_force
            if m==-1:
                m=100
            fac = min(float(abs(self.force))/m,1)
            col = [int(fac*end[i]+(1-fac)*start[i]) for i in range(3)]
            return tuple(col)
        else:
            return [0,255,0]

    def check_weight(self,coord,weight,g=9.81):
        if self.can_collide:

            position_on_connection = np.dot(np.array(coord)-self.center,self.dir)/self.len
            #-0.5 when at point 1,0.5 when at point 2

            distance_to_line = np.dot(np.array(coord)-self.center,[-self.dir[1],self.dir[0]])


            if abs(position_on_connection)<0.5 and abs(distance_to_line)<10:
                self.line_width=5
                percent_of_force_for_p2 = (position_on_connection+0.5)
                self.p2.add_force[1]+=weight*g*percent_of_force_for_p2
                self.p1.add_force[1]+=weight*g*(1-percent_of_force_for_p2)
                return True
            return False

    def add_weight(self,weight,perc,g=9.81):
        percent_of_force_for_p2 = 1-(perc+1.0)/2
        self.p2.add_force[1]+=weight*g*percent_of_force_for_p2
        self.p1.add_force[1]+=weight*g*(1-percent_of_force_for_p2)

        if DEBUG:
            self.line_width = 5


    def get_bounding_box(self):
        other_dir = np.array([-self.dir[1],self.dir[0]])
        return BoundingBox(np.array(self.center)+(self.collision_width/2)*other_dir,[self.dir,[-self.dir[1],self.dir[0]]],[self.len/2,self.collision_width/2])


    def check_train(self,train,g=9.81):
        self.line_width=1
        if self.can_collide:
            coords = train.mass_coordinates
            weights = train.point_weights
            for i in range(len(coords)):
                if self.check_weight(coords[i],weights[i],g):
                    train.is_on(self,i)


    def draw(self,surface,zoom=1,translation=[0,0]):
        pygame.draw.line(surface,self.get_color(),self.p1.get_int_pos(zoom,translation),self.p2.get_int_pos(zoom,translation),self.line_width)
        self.line_width = 1
        #self.get_bounding_box().draw(surface)

    def get_center(self):
        return self.center
