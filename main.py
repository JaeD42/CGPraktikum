
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


def load_sound(name):
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound:', name)
        raise SystemExit
    return sound

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
    channel1.set_volume(0.3)
    channel2.set_volume(0.3)

    bgmusic = load_sound('Spring.wav')
    bgmusic.set_volume(0.3)
    train_sound = load_sound('train2.wav')
    train_sound.set_volume(0.7)
    duration = train_sound.get_length() # duration of thunder in secon
    channel1.play(bgmusic, loops = -1)
    channel2.play(train_sound, loops = -1)

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)
    bg = RTImage(pygame.transform.scale(load_image('landscape3.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)))
    soundtick = 0

    #list of movable objects for collision check (mouse dragging)
    movable_objects = []

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    img1 = pygame.transform.rotozoom(load_image('train_lastwagon.png'),0,0.2)
    img2 = pygame.transform.rotozoom(load_image('train_wagon.png'),0,0.2)
    img3 = pygame.transform.rotozoom(load_image('train_firstwagon.png'),0,0.2)
    wagon_imgs = [img1, img2, img3]

    train = Train(NUMBER_OF_WAGONS, wagon_imgs, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED )
    #train = Wagon(img, TRAIN_START_COORD, TRAIN_WEIGHTS, TRAIN_SPEED)
    rectangle_draging=False

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
            #fps = font.render("FPS:"+str(int(clock.get_fps()))+"  Zoom:"+str(ZOOM), True, pygame.Color('black'))
            physics.update_physics(STEPSIZE)
            physics.move(STEPSIZE)
            physics.draw(screen,ZOOM,TRANSLATE)


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
