import numpy as np
import pygame

class BoundingBox():
    center = [] #achsen normiert, koordinaten des objekts
    axes = []
    lengths = []

    dragging = False

    def __init__(self, center, axes, lengths):
        self.center = np.array(center)
        self.axes = np.array(axes)
        self.lengths = np.array(lengths)

    def check_collision(self, point_coordinates):
        point_centered = (np.array(point_coordinates) - self.center)
        #test collision in direction of first axis of bounding box
        if(np.abs(np.dot(point_centered, self.axes[0])) > self.lengths[0]):
            return False
        #test in second direction
        if(np.abs(np.dot(point_centered, self.axes[1])) > self.lengths[1]):
            return False

        return True

    def update(self, center, axes, lengths):
        self.center = np.array(center)
        self.axes = np.array(axes)
        self.lengths = np.array(lengths)


class Train():
    v = []
    image = None
    width = None
    height = None
    coordinates = None
    mass_coordinates = []
    point_weights = []
    orientation = None
    bounding_box = None
    speed = 0
    is_on_object = False
    dragging = False


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
        print(self.is_on_object)
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
