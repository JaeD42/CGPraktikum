import numpy as np
import pygame
from Objects.BoundingBox import BoundingBox
from Utils.settings import DEBUG
from Graphics.RotateTranslateImage import RTImage_Connection
from Utils.load_data import load_image
from Utils.settings import *
class Connection:

    bridge_mode = False

    def __init__(self,point1,point2,length,strength,max_force = MAX_FORCE, can_collide = False, mutable=True):
        self.p1 = point1
        self.p2 = point2
        self.img_Collide = RTImage_Connection(pygame.transform.rotozoom(load_image(BALKEN_UNTEN),0,0.1),length)
        self.img_not_Collide = RTImage_Connection(pygame.transform.rotozoom(load_image(BALKEN),0,0.1),length)

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
        self.collision_width = 10
        self.hover_width = 10
        self.mutable = mutable

    #positive force: drags points to middle
    #negative force: push points away

    def create_pickleable(self):
        return [self.p1.point_num,self.p2.point_num,self.correct_length, self.strength, self.max_force, self.can_collide]

    def set_mutable(self,mutable):
        self.mutable = mutable

    def update_force(self):
        self.len = self.p1.distance_to(self.p2)

        self.force = (self.len-self.correct_length)*self.strength

        pos1 = self.p1.pos
        pos2 = self.p2.pos
        self.center = [(pos1[0]+pos2[0])/2,(pos1[1]+pos2[1])/2]
        self.dir = [(pos1[0]-pos2[0])/self.len,(pos1[1]-pos2[1])/self.len]

        
        if abs(self.force)>self.max_force:
            self.p1.connections.remove(self)
            self.p2.connections.remove(self)
            return True

        return False

    def get_color(self,start=[0,255,0],end=[255,0,0]):
        m = self.max_force
        if m==-1:
            m=100
        fac = min(float(abs(self.force))/m,1)
        col = [int(fac*end[i]+(1-fac)*start[i]) for i in range(3)]
        return tuple(col)

    def get_perpendicular(self):
        perp = [-self.dir[1],self.dir[0]]
        if perp[1]<0:
            perp[1]=-1*perp[1]
            perp[0]=-1*perp[0]
        return perp

    def check_weight(self,coord,weight,g=9.81):
        if self.can_collide:

            position_on_connection = np.dot(np.array(coord)-self.center,self.dir)/self.len
            #-0.5 when at point 1,0.5 when at point 2

            distance_to_line = np.dot(np.array(coord)-self.center,self.get_perpendicular())


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
        other_dir = np.array(self.get_perpendicular())
        return BoundingBox(np.array(self.center)+(self.collision_width/2)*other_dir,[self.dir,other_dir],[self.len/2,self.collision_width/2])


    def check_train(self,train,g=9.81):
        self.line_width=1
        if self.can_collide:
            coords = train.mass_coordinates
            weights = train.point_weights
            for i in range(len(coords)):
                if self.check_weight(coords[i],weights[i],g):
                    train.is_on(self,i)

    def remove(self):
        self.p1.connections.remove(self)
        self.p2.connections.remove(self)

    def is_on_connection(self,pos):
        bb = BoundingBox(np.array(self.center),[self.dir,other_dir],[self.len/2,self.hover_width/2])
        return bb.check_collision(pos)

    def draw(self,surface,zoom=1,translation=[0,0]):

        if self.can_collide:
            d_img = self.img_Collide
        else:
            d_img = self.img_not_Collide

        if not DEBUG and not self.bridge_mode:
            orientation = np.arctan2(-1*self.dir[1],self.dir[0])
            return surface.blit(*d_img.get_img(self.center,self.len,57.295*orientation,zoom,translation))
        else:
            col = list(self.get_color())
            if not self.can_collide:
                col.append(122)

            r = pygame.draw.line(surface,self.get_color(),self.p1.get_int_pos(zoom,translation),self.p2.get_int_pos(zoom,translation),self.line_width)
            self.line_width = 1
            return r
        #self.get_bounding_box().draw(surface)

    def get_center(self):
        return self.center
