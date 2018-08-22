#!/usr/bin/env python

import random, os.path
import numpy as np

#import basic pygame modules
import pygame
from pygame.locals import *

from Points import MassPoint, create_bridge

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#train
TRAIN_WEIGHTS       = [20,30,30,20]
TRAIN_START_COORD   = [0,SCREEN_HEIGHT*0.28]
TRAIN_SPEED         = 10
NODE_MASS           = 2
GRAVITY             = 9.81

#bridge
BRIDGE_START        = [SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.4]
BRIDGE_END          = [SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.4]
BRIDGE_HEIGHT       = 70
BRIDGE_NODES        = 6
BRIDGE_STIFF        = 300



main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#load image of an object
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

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
        self.bounding_box = self.calculate_bb()

    def draw(self,surface):
        surface.blit(self.image,self.coordinates)


def main(winstyle = 0):
    global ZOOM,TRANSLATE
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None
    pygame.display.set_caption("Choo Choo")
    running = True


    # Settings
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    bg = pygame.transform.scale(load_image('landscape3.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    img = pygame.transform.rotozoom(load_image('train.png'),0,0.2)
    train = Train(img, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED)
    rectangle_draging=False


    points,connections = create_bridge(BRIDGE_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES, D=BRIDGE_STIFF)

    try:
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            fps = font.render("FPS:"+str(int(clock.get_fps()))+"  Zoom:"+str(ZOOM), True, pygame.Color('black'))

            screen.blit(bg, (0,0))



            for c in connections:
                c.update_force()
                c.check_train(train)
            for p in points:
                p.move(0.06)

            for c in connections:
                c.draw(screen)
            for p in points:
                p.draw(screen)


            train.move()
            train.draw(screen)

            pygame.display.flip()

            # - constant game speed / FPS -
            clock.tick(FPS)


        pygame.quit()
    except SystemExit:
        pygame.quit()





#call the "main" function if running this script
if __name__ == '__main__': main()