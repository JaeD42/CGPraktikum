#!/usr/bin/env python
'''
    Author: Jana Becker, Jan Disselhoff
'''
from settings import *
import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")



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


    img = pygame.transform.rotozoom(load_image('train_silhouette.png'),0,0.2)
    width = img.get_width()
    height = img.get_height()
    diag = (width**2+height**2)**0.5 /2


    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    running = True
    i=0
    import numpy as np
    try:
        while running:
            i+=1
            print(i)
            screen.fill((255,255,255))

            rot_in_deg = float(i+135)/360*2*3.1415
            rotated = pygame.transform.rotozoom(img,i,1)
            screen.blit(rotated,[300-rotated.get_width()/2,300-rotated.get_height()/2])
            pygame.draw.circle(screen,(255,0,0),[300,300],5)

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
