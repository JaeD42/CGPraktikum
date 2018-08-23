import pygame
from pygame.locals import *

#game constants
#screen
SCREEN_WIDTH        = 1300
SCREEN_HEIGHT       = 600
SCREENRECT          = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
FPS                 = 30
ZOOM                = 1.0
ZOOM_FACTOR         = 0.1
TRANSLATE           = [0,0]
PAUSE               = False

#train
TRAIN_WEIGHTS       = [40,40,3,2]
TRAIN_START_COORD   = [0,SCREEN_HEIGHT*0.305]
TRAIN_SPEED         = 30
NODE_MASS           = 2
GRAVITY             = 9.81

#bridge
BRIDGE_START        = [SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.4]
BRIDGE_END          = [SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.4]
BRIDGE_HEIGHT       = 70
BRIDGE_NODES        = 6
BRIDGE_STIFF        = 30


DEBUG               = False

STEPSIZE            = 0.03
