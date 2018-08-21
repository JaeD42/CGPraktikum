
#!/usr/bin/env python

import random, os.path
import numpy as np

#import basic pygame modules
import pygame
from pygame.locals import *

from Points import MassPoint

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#game constants
SCREEN_WIDTH        = 1300
SCREEN_HEIGHT       = 600
TRAIN_WEIGHTS       = [20,30,30,20]
TRAIN_START_COORD   = [0,SCREEN_HEIGHT-200]
TRAIN_SPEED         = 10
NODE_MASS           = 2
GRAVITY             = 9.81
SCREENRECT          = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
FPS                 = 30
ZOOM                = 1.0
TRANSLATE           = [0,0]

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
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
    #   , image.get_rect()

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

    dragging = False


    def __init__(self, image, coordinates, weights, speed):
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.coordinates = coordinates #list
        self.point_weights = weights
        self.orientation = 0
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
        for i in len(self.mass_coordinates):
            self.mass_coordinates[i] += 0.1 * self.speed
        self.bounding_box.update(self.calculate_bb())

    def draw(self,surface):
        surface.blit(self.image,self.coordinates)


def main(winstyle = 0):
    global ZOOM,TRANSLATE
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None
    pygame.display.set_caption("Choo Choo")
    pygame.key.set_repeat(1000,10)

    running = True


    # Settings
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    img = pygame.transform.rotozoom(load_image('train.png'),0,0.5)
    train = Train(img, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED)
    rectangle_draging=False

    p = MassPoint([100,100],1,moveable=False)

    try:
        while running:
            train.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        if rectangle.collidepoint(event.pos):
                            rectangle_draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = rectangle.x - mouse_x
                            offset_y = rectangle.y - mouse_y
                    elif event.button == 4:
                        ZOOM+=0.01
                    elif event.button == 5:
                        ZOOM-=0.01


                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        rectangle_draging = False


                elif event.type == pygame.MOUSEMOTION:
                    if rectangle_draging:
                        mouse_x, mouse_y = event.pos
                        rectangle.x = mouse_x + offset_x
                        rectangle.y = mouse_y + offset_y

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        TRANSLATE[1]+=10
                    elif event.key == pygame.K_DOWN:
                        TRANSLATE[1]-=10
                    elif event.key == pygame.K_LEFT:
                        TRANSLATE[0]+=10
                    elif event.key == pygame.K_RIGHT:
                        TRANSLATE[0]-=10





                #print(event.event_name())




            screen.fill((255,255,255))

            fps = font.render("FPS:"+str(int(clock.get_fps()))+"  Zoom:"+str(ZOOM), True, pygame.Color('black'))

            screen.blit(fps, (50, 50))

            p.draw(screen,ZOOM,TRANSLATE)

            pygame.display.flip()

            # - constant game speed / FPS -
            clock.tick(FPS)


        pygame.quit()
    except SystemExit:
        pygame.quit()





#call the "main" function if running this script
if __name__ == '__main__': main()
