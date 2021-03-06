#!/usr/bin/env python
'''
    Author: Jana Becker, Jan Disselhoff
'''


import random, os.path
from Game.Physics import Physics
import numpy as np
from Objects.train import Train,Wagon
from Utils.settings import *
from Graphics.RotateTranslateImage import RTImage
from Game.BridgeCreator import BridgeCreator
from Game.UI import UI
from Graphics.Sound import Sound
#import basic pygame modules
import pygame
from pygame.locals import *
from Utils.load_data import *

from Objects.Points import MassPoint, create_bridge

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

    sound =Sound()

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    #list of movable objects for collision check (mouse dragging)
    movable_objects = []

    Interface = UI()

    sound.play_bg()
    soundtick=0
    running = True
    try:
        while running:
            running = Interface.step(STEPSIZE,screen)

            if(not Interface.music_is_on):
                sound.mute()
            else:
                sound.unmute()

            if(not Interface.build_mode):
                soundtick += 1
                if soundtick>1000:
                    sound.play_train_sound()
                    soundtick = 0



            if SHOW_FPS:
                fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
                screen.blit(fps, (50, 50))
                mouse = font.render(str(pygame.mouse.get_pos()), True, pygame.Color('white'))
                screen.blit(mouse, (50, 80))
            pygame.display.flip()
            # - constant game speed / FPS -
            clock.tick(FPS)

        pygame.quit()
    except SystemExit:
        pygame.quit()





#call the "main" function if running this script
if __name__ == '__main__': main()
