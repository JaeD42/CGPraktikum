
#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

#game constants
TRAIN_WEIGHT        = 200
TRAIN_START_COORD   = [0,20]
TRAIN_SPEED         = 10
NODE_MASS           = 2
GRAVITY             = 9.81
SCREENRECT          = Rect(0, 0, 640, 480)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
    #   , image.get_rect()


class Train():
    speed = None
    image = None
    coordinates = None
    weight = None

    def __init__(self, image, coordinates, weight, speed):
        self.image = image
        self.coordinates = coordinates #list
        self.weight = weight
        self.speed = speed

    def move(self):
        self.coordinates[0] = self.coordinates[0]+0.1*speed

    def draw(self,surface):
        surface.blit(self.image,self.coordinates)

from Points import MassPoint,create_bridge
from Connection import Connection
import time
def main(winstyle = 0):
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None


    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    points = []
    connections = []
    #for i in range(5):
    #    points.append(MassPoint([300+50*i,200+10*i**2],5,moveable=(i!=0)))

    #for i in range(4):
    #    connections.append(points[i].connect_to(points[i+1],60,10))

    points,connections = create_bridge([100,300],200,50,8)




    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    running = True
    try:
        while running:
            screen.fill((0,0,0))
            #train.draw(screen)
            for c in connections:
                c.update_force()
            for p in points:
                p.update_pos(0.06)

            for c in connections:
                c.draw(screen)
            for p in points:
                p.draw(screen)

            fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
            screen.blit(fps, (50, 50))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(30)

        pygame.quit()
    except SystemExit:
        pygame.quit()





#call the "main" function if running this script
if __name__ == '__main__': main()
