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

    dragging = False


    def __init__(self, image, coordinates, weights, speed):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.coordinates = coordinates #list
        self.point_weights = weights
        self.orientation = 0
        self.speed = speed
        self.v = [speed, 0] #todo

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

    def move(self):#todo, soll auch drehen koennen
        self.coordinates[0] += 0.1 * self.speed
        for i in range(len(self.mass_coordinates)):
            self.mass_coordinates[i][0] += 0.1 * self.speed
        if self.coordinates[0]>pygame.display.get_surface().get_width():
            self.coordinates[0]-=pygame.display.get_surface().get_width()+self.width
            for i in range(len(self.mass_coordinates)):
                self.mass_coordinates[i][0] -=pygame.display.get_surface().get_width()+self.width

        #self.bounding_box = self.calculate_bb()

    def draw(self,surface,zoom=1,translation=[0,0]):
        surface.blit(pygame.transform.rotozoom(self.image,0,zoom),[int((translation[i]+self.coordinates[i])*zoom) for i in range(2)])
