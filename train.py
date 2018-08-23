import numpy as np
import pygame
from BoundingBox import BoundingBox
from settings import *

class Train():


    def __init__(self, image, coordinates, weights, speed):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.coordinates = coordinates #list
        self.coordinates[0]+=200
        self.point_weights = weights
        self.orientation = 0
        self.speed = speed
        self.v = [speed, 0] #todo
        self.physics_v = [0,0]

        self.bounding_box = self.calculate_bb()

        num_of_points = len(self.point_weights)
        dist_between_points = int(self.width/(num_of_points-1))
        self.mass_coordinates = []
        for i in range(num_of_points):
            self.mass_coordinates.append([self.coordinates[0] + i*dist_between_points,
                                     self.coordinates[1]+self.height])


    def calculate_bb(self):
        #calculate bounding box
        lengths = np.array([self.width / 2, self.height / 2])
        axes = [np.array([np.sin(self.orientation), np.cos(self.orientation)]),
                np.array([-np.cos(self.orientation), np.sin(self.orientation)])]
        center = lengths + np.array([self.coordinates[0], self.coordinates[1]])
        return BoundingBox(center, axes, lengths)

    def move(self,dt,g=9.81):#todo, soll auch drehen koennen
        #print(self.is_on_object)
        if not self.is_on_object and self.coordinates[0]>200:
            self.physics_v[1]+= dt*g/sum(self.point_weights)
        else:
            self.physics_v[1]=0

        self.v[0] = np.cos(self.orientation)*self.speed + self.physics_v[0]
        self.v[1] = np.sin(self.orientation)*self.speed + self.physics_v[1]
        self.coordinates[0] += dt * self.v[0]
        self.coordinates[1] += dt * self.v[1]
        for i in range(len(self.mass_coordinates)):
            self.mass_coordinates[i][0] += dt * self.v[0]
            self.mass_coordinates[i][1] += dt * self.v[1]




        if self.coordinates[0]>pygame.display.get_surface().get_width():
            self.coordinates[0]-=pygame.display.get_surface().get_width()+self.width
            for i in range(len(self.mass_coordinates)):
                self.mass_coordinates[i][0] -=pygame.display.get_surface().get_width()+self.width

        self.is_on_object = False
        #self.bounding_box = self.calculate_bb()

    def draw(self,surface,zoom=1,translation=[0,0]):
        surface.blit(pygame.transform.rotozoom(self.image,self.orientation*360/6.28,zoom),[int((translation[i]+self.coordinates[i])*zoom) for i in range(2)])

    def translate(self,dx,dy):
        self.coordinates[0]+=dx
        self.coordinates[1]+=dy
        for i in range(len(self.mass_coordinates)):
            self.mass_coordinates[i][0] += dx
            self.mass_coordinates[i][1] += dy

    def update_rotation(self):
        s = np.sin(self.orientation)
        c = np.cos(self.orientation)
        for i in range(len(self.mass_coordinates)):
            self.mass_coordinates[i]=[self.coordinates[0] + c*i*dist_between_points - s*self.height,
                                     self.coordinates[1]+ s*i*dist_between_points + c*self.height]



    def is_on(self,connection,index):
        if index == 0:

            dir_to_conn = np.array([-connection.dir[1],connection.dir[0]])
            weight_point = np.array(self.mass_coordinates[0])
            translate_values = -dir_to_conn*np.dot(weight_point-connection.center,dir_to_conn)
            #print(translate_values)
            self.translate(translate_values[0],translate_values[1])

        if index == len(self.mass_coordinates)-1:
            #ToDO
            pass


        self.orientation = np.arccos(connection.dir[0])
#
        self.is_on_object=True


class Wagon():

    def __init__(self, image, coordinates, weights, speed):
        self.image = image
        self.last_img = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.coordinates = coordinates #links oben
        self.center = [self.coordinates[0]+self.width/2.0,self.coordinates[1]+self.height/2.0]

        self.point_weights = weights #max 2 gewichte (1 vorne, 1 hinten)
        self.orientation = 0
        self.speed = speed
        self.v = [speed, 0]
        self.physics_v_mass = [[0,0],[0,0]]

        self.mass_coordinates = []
        self.mass_coordinates.append([self.coordinates[0], #todo: nach innen setzen
                                     self.coordinates[1]+self.height])

        self.mass_coordinates.append([self.coordinates[0]+self.width,
                                    self.coordinates[1]+self.height])
        self.mass_coordinates = np.array(self.mass_coordinates)

        self.last_zoom = 1
        self.orientation_changed = False



    def collision_mass_with_physics(self,bounding_box,index):

        collision_found,ax1_perc,ax2_perc,coordinate = bounding_box.check_collision_return_location(self.mass_coordinates[index])

        if collision_found:
            if ax2_perc<0:
                self.mass_coordinates[index]-=[(1+ax2_perc)*bounding_box.axes[1][i]*bounding_box.lengths[1] for i in range(2)]
            else:
                self.mass_coordinates[index]-=[(1+ax2_perc)*bounding_box.axes[1][i]*bounding_box.lengths[1] for i in range(2)]

            self.physics_v_mass[index]=[0,0]

            return self.point_weights[index],ax1_perc


        return 0,0

    def collision_with_connection(self,connection):
        if not connection.can_collide:
            return

        w,perc = self.collision_mass_with_physics(connection.get_bounding_box(),0)

        if w!=0:
            connection.add_weight(w,perc)

        w2,perc2 = self.collision_mass_with_physics(connection.get_bounding_box(),1)

        if w2!=0:
            connection.add_weight(w2,perc2)


    def correct_position(self):
        mass_dir = self.mass_coordinates[1]-self.mass_coordinates[0]
        new_orientation = np.arctan(-1*mass_dir[1]/mass_dir[0])

        if new_orientation!=self.orientation:
            self.orientation_changed=True
            self.orientation=new_orientation


        len = np.sqrt(np.dot(mass_dir,mass_dir))
        normalized_dir = mass_dir/len
        if len!=self.width:
            self.mass_coordinates[1]+= (self.width-len)/2 * normalized_dir
            self.mass_coordinates[0]-= (self.width-len)/2 * normalized_dir



            self.center = (self.mass_coordinates[1]+self.mass_coordinates[0])/2 - [self.height/2 *-1*normalized_dir[1],self.height/2 *normalized_dir[0]]
            self.coordinates = 2*self.center - self.mass_coordinates[1]



    def move(self,dt,g=9.81):


        #self.physics_v_mass[1][1]+=dt*g

        self.v[0] = np.cos(self.orientation)*self.speed
        self.v[1] = -1*np.sin(self.orientation)*self.speed
        self.mass_coordinates[0] += (np.array(self.physics_v_mass[0]) + self.v)*dt
        self.mass_coordinates[1] += (np.array(self.physics_v_mass[1]) + self.v)*dt

        self.correct_position()

        for i in range(2):
            if not ((self.mass_coordinates[i][0]<BRIDGE_START[0] or self.mass_coordinates[i][0]>BRIDGE_END[0]) and abs(self.mass_coordinates[i][1]-BRIDGE_START[1])<10):
                self.physics_v_mass[i][1]+=dt*g
            else:
                self.physics_v_mass[i][1] = 0

    def draw(self,surface,zoom=1,translation=[0,0]):
        if self.last_zoom==zoom and not self.orientation_changed:
            pass
        else:
            self.last_zoom = zoom
            self.orientation_changed = False
            self.last_img = pygame.transform.rotozoom(self.image,self.orientation*360/6.28,zoom)
        offset = [self.last_img.get_width()/2,self.last_img.get_height()/2]
        surface.blit(self.last_img,[int((translation[i]+self.center[i]-offset[i])*zoom) for i in range(2)])
        pygame.draw.circle(surface,(255,0,0),[int(i) for i in self.mass_coordinates[0]],5)
        pygame.draw.circle(surface,(255,0,0),[int(i) for i in self.mass_coordinates[1]],5)
