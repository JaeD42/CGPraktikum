
#!/usr/bin/env python

import random, os.path
import numpy as np
from train import Train
from settings import *
from events import calc_events

#import basic pygame modules
import pygame
from pygame.locals import *

from Points import MassPoint, create_bridge

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")



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


def main(winstyle = 0):
    global ZOOM,TRANSLATE,PAUSE
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
    bg = pygame.transform.scale(load_image('landscape3.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bgmusic = load_sound('Spring.wav')
    bgmusic.set_volume(0.2)
    train_sound = load_sound('train2.wav')
    train_sound.set_volume(0.05)
    soundtick = 0

    #list of movable objects for collision check (mouse dragging)
    movable_objects = []

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    img = pygame.transform.rotozoom(load_image('train_silhouette.png'),0,0.2)
    train = Train(img, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED)
    rectangle_draging=False

    #create a bridge
    points,connections = create_bridge(BRIDGE_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES, D=BRIDGE_STIFF)

    try:
        while running:
            soundtick+=1

            bgmusic.play(-1)

            if(soundtick >= 5):
                train_sound.play(-1)
            ZOOM,TRANSLATE,PAUSE,running = calc_events()
            #fps = font.render("FPS:"+str(int(clock.get_fps()))+"  Zoom:"+str(ZOOM), True, pygame.Color('black'))
            if not PAUSE:
                broken_conns = []
                for c in connections:
                    broke = c.update_force()
                    if broke:
                        broken_conns.append(c)
                        continue
                    c.check_train(train)

                for c in broken_conns:
                    connections.remove(c)

                for p in points:
                    p.move(0.06)
                train.move()

            screen.fill((255,255,255))

            screen.blit(pygame.transform.rotozoom(bg,0,ZOOM), [TRANSLATE[i]*ZOOM for i in range(2)])

            for c in connections:
                c.draw(screen,ZOOM,TRANSLATE)
            for p in points:
                p.draw(screen,ZOOM,TRANSLATE)

            train.draw(screen,ZOOM,TRANSLATE)

            pygame.display.flip()

            # - constant game speed / FPS -
            clock.tick(FPS)
        pygame.quit()
    except SystemExit:
        pygame.quit()





#call the "main" function if running this script
if __name__ == '__main__': main()
