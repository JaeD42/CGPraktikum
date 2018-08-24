
#!/usr/bin/env python

import random, os.path
from Physics import Physics
import numpy as np
from train import Train,Wagon
from settings import *
from events import calc_events
from RotateTranslateImage import RTImage
#import basic pygame modules
import pygame
from pygame.locals import *
from load_data import *

from Points import MassPoint, create_bridge

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")



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
    screen = pygame.display.set_mode(SCREENRECT.size, FLAGS, bestdepth)
    screen.set_alpha(None)

    #SOUND
    # initialize pygame.mixer
    pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12)

    # create separate Channel objects for simultaneous playback
    channel1 = pygame.mixer.Channel(0) # argument must be int
    channel2 = pygame.mixer.Channel(1)
    channel1.set_volume(0.1)
    channel2.set_volume(0.1)
    soundtick = 0

    bgmusic = load_sound(BGMUSIC)
    bgmusic.set_volume(BGMUSIC_VOL)
    train_sound = load_sound(TRAIN_SOUND)
    train_sound.set_volume(TRAIN_SOUND_VOL)

    bg = RTImage(pygame.transform.scale(load_image(BG), (SCREEN_WIDTH, SCREEN_HEIGHT)))
    wagon_imgs = [pygame.transform.rotozoom(load_image(img),0,0.2) for img in WAGON_IMGS]

    duration = train_sound.get_length() # duration of thunder in secon
    print(duration)
    channel1.play(bgmusic, loops = -1)

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    #list of movable objects for collision check (mouse dragging)
    movable_objects = []

    train = Train(NUMBER_OF_WAGONS, wagon_imgs, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED )
    #create a bridge
    points,connections = create_bridge(BRIDGE_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES, D=BRIDGE_STIFF, max_force = 2000)

    BRIDGE2_START = [BRIDGE_START[0],BRIDGE_START[1]+200]
    points2,connections2 = create_bridge(BRIDGE2_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES-1, D=BRIDGE_STIFF*2, max_force = 10000)
    conn = connections2[2]
    add_point = MassPoint((SCREEN_WIDTH,240),5,moveable=False)
    add_conn = add_point.connect_to_quick(points2[4],can_collide=True)

    points.extend(points2)
    connections.extend(connections2)
    points.append(add_point)
    connections.append(add_conn)


    physics = Physics(connections,points,train,bg)
    #print(BRIDGE_END)
    try:
        while running:
            ZOOM,TRANSLATE,PAUSE,running = calc_events()
            physics.update_physics(STEPSIZE)
            physics.move(STEPSIZE)
            physics.draw(screen,ZOOM,TRANSLATE)

            soundtick += 1

            if(soundtick % 1000 == 1):
                if(not channel2.get_busy()):
                    channel2.play(train_sound)


            if DEBUG:
                fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
                screen.blit(fps, (50, 50))

            pygame.display.flip()
            # - constant game speed / FPS -
            clock.tick(FPS)

        pygame.quit()
    except SystemExit:
        pygame.quit()





#call the "main" function if running this script
if __name__ == '__main__': main()
