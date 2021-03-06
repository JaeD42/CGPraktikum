#!/usr/bin/env python
'''
    Author: Jana Becker, Jan Disselhoff
'''
import numpy as np
import pygame
from Objects.BoundingBox import BoundingBox
from Graphics.RotateTranslateImage import RTImage
from Utils.settings import *
from math import pi
from Graphics.Effects import SmokeEffect

class Train():



    #imgs[2] = first wagon image
    #imgs[1] = middle wagon image
    #imgs[0] = last wagon image
    def __init__(self, number_of_wagons, imgs, start_coordinates, weights, speed):
        self.number_of_wagons = number_of_wagons
        self.start_coordinates = start_coordinates
        self.smoke = SmokeEffect()
        self.smoke_iters = 10
        self.counter = 0
        self.wagons = []

        for i in range(number_of_wagons):
            if(i==0):
                self.wagons.append(Wagon(imgs[0], start_coordinates, weights[0], speed))
            elif(i==number_of_wagons-1):
                wagon_length = imgs[0].get_width() + (number_of_wagons - 2) * imgs[1].get_width()
                coord = [start_coordinates[0]+ wagon_length, start_coordinates[1]]
                self.wagons.append(Wagon(imgs[2], coord, weights[number_of_wagons - 1], speed))
            else:
                wagon_length = imgs[0].get_width() + (i-1) * imgs[1].get_width()
                coord = [start_coordinates[0]+ wagon_length, start_coordinates[1]]
                self.wagons.append(Wagon(imgs[1], coord, weights[i - 1], speed))
        self.connect_wagons()

    @staticmethod
    def get_standard_train(level=None):

        from Utils.load_data import load_image
        wagon_imgs = [pygame.transform.rotozoom(load_image(img),0,0.2) for img in WAGON_IMGS]

        if level==None:
            train = Train(NUMBER_OF_WAGONS, wagon_imgs, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED )
        else:
            train = Train(NUMBER_OF_WAGONS, wagon_imgs, level.start, TRAIN_WEIGHTS, TRAIN_SPEED )
        return train

    def connect_wagons(self):
        next_wagon = self.wagons[self.number_of_wagons-1]
        for i, wagon in enumerate(reversed(self.wagons[0:-1])):
            if(i == 0):
                next_wagon.add_last_wagon(wagon)
            wagon.add_next_wagon(next_wagon)
            next_wagon = wagon




    def collision_with_connection(self,connection):
        for i in range(self.number_of_wagons):
            self.wagons[i].collision_with_connection(connection)

    def collision_with_level(self,level):
        for i in range(self.number_of_wagons):
            self.wagons[i].collision_with_level_elements(level)



    def move(self,dt,g=9.81):
        self.counter+=1
        self.smoke.update(dt)
        if self.counter>self.smoke_iters:
            pos = self.wagons[-1].center[:]
            pos[0]+=20
            pos[1]-=10
            self.smoke.add_smoke(pos,300,num_particles=100)
            self.counter=0
        for i in range(self.number_of_wagons):
            self.wagons[i].move(dt, g)

    def draw(self,surface,zoom=1,translation=[0,0]):
        self.smoke.draw(surface)
        #also draw connections
        for i in range(self.number_of_wagons):
            self.wagons[i].draw(surface, zoom, translation)


class Wagon():

    def __init__(self, image, coordinates, weights, speed):
        self.image = RTImage(image)
        #self.last_img = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.coordinates = coordinates #links oben
        self.center = [self.coordinates[0]+self.width/2.0,self.coordinates[1]+self.height/2.0]

        self.point_weights = weights #max 2 gewichte (1 vorne, 1 hinten)
        self.orientation = 0
        self.speed = speed
        self.v = np.array([speed, 0])
        self.physics_v_mass = [[0,0],[0,0]]

        self.mass_coordinates = []
        self.mass_coordinates.append([self.coordinates[0], #todo: nach innen setzen
                                     self.coordinates[1]+self.height])

        self.mass_coordinates.append([self.coordinates[0]+self.width,
                                    self.coordinates[1]+self.height])
        self.mass_coordinates = np.array(self.mass_coordinates)

        self.next_wagon = None
        self.last_wagon = None
        self.last_zoom = 1
        self.on_plateau = True
        #self.orientation_changed = False



    def add_next_wagon(self,wagon):
        self.next_wagon = wagon

    def add_last_wagon(self, wagon):
        self.last_wagon = wagon

    def collision_mass_with_physics(self,bounding_box,index):

        collision_found,ax1_perc,ax2_perc,coordinate = bounding_box.check_collision_return_location(self.mass_coordinates[index])

        if collision_found:

            self.mass_coordinates[index]-=[(1+ax2_perc)*bounding_box.axes[1][i]*(bounding_box.lengths[1]) for i in range(2)]



            return self.point_weights[index],ax1_perc


        return 0,0

    def collision_with_level_elements(self,level):
        self.on_plateau = [False,False]
        for plat in level.plateaus:
            BB = plat.get_bounding_box()
            w,perc = self.collision_mass_with_physics(BB,0)
            if w:
                self.physics_v_mass[0]=[0,0]
                self.on_plateau[0]=True
            w,perc = self.collision_mass_with_physics(BB,1)
            if w:
                self.on_plateau[1]=True
                self.physics_v_mass[1]=[0,0]





    def collision_with_connection(self,connection):
        if not connection.can_collide:
            return

        w,perc = self.collision_mass_with_physics(connection.get_bounding_box(),0)

        if w:
            prozent = (1+perc)/2
            self.physics_v_mass[0]=[0,0.9*((prozent)*connection.p1.v[1]+(1-prozent)*connection.p2.v[1])]
            connection.add_weight(w,perc)

        w2,perc2 = self.collision_mass_with_physics(connection.get_bounding_box(),1)

        if w2:
            prozent = (1+perc2)/2
            self.physics_v_mass[1]=[0,0.9*((prozent)*connection.p1.v[1]+(1-prozent)*connection.p2.v[1])]

            connection.add_weight(w2,perc2)

    def correct_position(self):

        mass_dir = self.mass_coordinates[1]-self.mass_coordinates[0]
        self.orientation = np.arctan2(-1*mass_dir[1],mass_dir[0])


        len = np.sqrt(np.dot(mass_dir,mass_dir))
        normalized_dir = mass_dir/len
        if len!=self.width:
            self.mass_coordinates[1]+= (self.width-len)/2 * normalized_dir
            self.mass_coordinates[0]-= (self.width-len)/2 * normalized_dir

            self.center = (self.mass_coordinates[1]+self.mass_coordinates[0])/2 - [self.height/2 *-1*normalized_dir[1],self.height/2 *normalized_dir[0]]
            self.coordinates = 2*self.center - self.mass_coordinates[1]


    def stay_close_to_last_wagon(self):
        if(self.last_wagon):
            last_wagon_pos = self.last_wagon.mass_coordinates[1]
            dist = last_wagon_pos - self.mass_coordinates[0]

            len = np.sqrt(np.dot(dist, dist))
            if len==0:
                return
            dist = dist/len

            if(self.mass_coordinates[0][0] < last_wagon_pos[0]):
                self.mass_coordinates[1] -= 0.5 * dist * len

            elif(len > 5):
                self.mass_coordinates[1] -= 0.1 * dist * (len - 5)

            elif(len < 4.5):
                self.mass_coordinates[1] += 0.1 * dist * (len - 5)

    def stay_close_to_next_wagon(self):
        if(self.next_wagon != None):
            next_wagon_pos = self.next_wagon.mass_coordinates[0]
            dist = self.mass_coordinates[1] - next_wagon_pos

            len = np.sqrt(np.dot(dist, dist))
            if len==0:
                return
            dist = dist/len

            if(self.mass_coordinates[1][0] > next_wagon_pos[0]):
                self.mass_coordinates[1] -= 0.5 * dist * len

            elif(len > 5):
                self.mass_coordinates[1] -= 0.1 * dist * (len - 5)

            elif(len < 4.5):
                self.mass_coordinates[1] += 0.1 * dist * (len - 5)

    def move(self,dt,g=9.81):
        self.v[0] = np.cos(self.orientation)*self.speed
        self.v[1] = -1*np.sin(self.orientation)*self.speed
        self.mass_coordinates[0] += (np.array(self.physics_v_mass[0]) + self.v)*dt
        self.mass_coordinates[1] += (np.array(self.physics_v_mass[1]) + self.v)*dt

        self.stay_close_to_next_wagon()
        self.stay_close_to_last_wagon()

        self.correct_position()

        for i in range(2):
            if not self.on_plateau[i]:
                self.physics_v_mass[i][1]+=dt*g

    def draw(self,surface,zoom=1,translation=[0,0]):
        surface.blit(*self.image.get_img(self.center,57.295*self.orientation,zoom,translation))
        if DEBUG:
            pygame.draw.circle(surface,(255,0,0),[int(i) for i in self.mass_coordinates[0]],5)
            pygame.draw.circle(surface,(255,0,0),[int(i) for i in self.mass_coordinates[1]],5)
