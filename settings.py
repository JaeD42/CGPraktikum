import pygame
from pygame.locals import *

#game constants
#screen
SCREEN_WIDTH        = 1300
SCREEN_HEIGHT       = 600
SCREENRECT          = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_MIDDLE       =[SCREEN_WIDTH/2,SCREEN_HEIGHT/2]
FPS                 = 600
ZOOM                = 1.0
ZOOM_FACTOR         = 0.1
TRANSLATE           = [0,0]
PAUSE               = False

#train
NUMBER_OF_WAGONS    = 5
TRAIN_WEIGHTS       = [[5,5]]*5
TRAIN_START_COORD   = [0,SCREEN_HEIGHT*0.305]
TRAIN_SPEED         = 30
NODE_MASS           = 2
GRAVITY             = 9.81

#bridge
BRIDGE_START        = [SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.4]
BRIDGE_END          = [SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.4]
BRIDGE_HEIGHT       = 70
BRIDGE_NODES        = 6
BRIDGE_STIFF        = 200

#grid
GRID_SIZE           = 50


DEBUG               = True

STEPSIZE            = 0.02


#pygame flags
FLAGS = DOUBLEBUF
