import pygame
import os
from pygame.locals import *
import sys

#System
MAIN_DIR = os.path.split(os.path.abspath(sys.argv[0]))[0]
DATA_DIR = os.path.join(MAIN_DIR, 'data')
BRIDGE_DIR = os.path.join(MAIN_DIR, 'bridges')

#load lvl:
LOAD_LVL            = 0
LVLS                = ['lvl1','lvl2','lvl3','lvl4']
#grid
GRID_SIZE           = 100
MIN_POINT_DIST      = 70


DEBUG               = True
GM                  = False
SHOW_FPS            = True

STEPSIZE            = 0.02


#pygame flags
FLAGS               = pygame.DOUBLEBUF

#game constants
#game
MAX_SCORE           = 3000
POINT_COST          = 10
CONNECTION_COST     = 10
FIXED_CON_COST      = 50
INITIAL_COST        = 1000

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
RUNNING             = True

#train
NUMBER_OF_WAGONS    = 5
TRAIN_WEIGHTS       = [[4000,4000]]*5
TRAIN_START_COORD   = [-400,0.0]
TRAIN_SPEED         = 30
NODE_MASS           = 2
GRAVITY             = 9.81

#bridge
BRIDGE_START        = [SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.4]
BRIDGE_END          = [SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.4]
BRIDGE_HEIGHT       = 70
BRIDGE_NODES        = 5
BRIDGE_STIFF        = 10000
MAX_FORCE           = 100000
WEIGHT_PER_LENGTH   = 0.5


#Sound and images
BGMUSIC             = 'Spring.wav'
TRAIN_SOUND         = 'train_whistle_short.wav'
BGMUSIC_VOL         = 0.2
TRAIN_SOUND_VOL     = 0.3

BG                  = 'landscape.png'
WAGON_IMGS          = ['train_lastwagon.png', 'train_wagon.png', 'train_firstwagon.png']
PLATEAU_IMGS        = ['plateau0.png', 'plateau2.png', 'plateau1.png', 'plateau3.png','plateau4.png', 'plateau5.png', 'plateau6.png']
BALKEN              = 'balken.png'
BALKEN_UNTEN        = 'balken_unten.png'


#Toggle Icon Bridge
TRAIN_ON_CONN_IMG   = "zugauf.png"
TRAIN_THROUGH_CONN_IMG = "zugdurch.png"
CONN_IMG_POS        = (10,10)
CONN_IMG_SIZE       = (50,50)

#Icon Music
MUSIC_ON            = 'music.png'
MUSIC_OFF           = 'music_off.png'
MUSIC_SIZE          = (50,50)
