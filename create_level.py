from Game.BridgeCreator import Bridge
from Objects.Grid import Grid
import pickle
from Graphics.RotateTranslateImage import RTImage
import pygame
from Utils.load_data import load_image
from Utils.settings import *
from Game.Game import Level
from Objects.Plateau import Plateau
from Objects.Grid import Grid
from Utils.settings import *


def lvl1():
    p1 = [[-200,400], [230,400]]
    p2 = [[1150, 400], [1500, 400]]
    p3 = [[400, 400], [700, 400]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0])
    p_start.flipped = True
    p_end = Plateau(p2[0], p2[1] ,PLATEAU_IMGS[0])
    p_middle = Plateau(p3[0], p3[1], PLATEAU_IMGS[1])

    grid = Grid.create_standard_grid((100,100),(1200,500),10,10)
    start = TRAIN_START_COORD
    goal = BRIDGE_END
    points = []
    conns = []
    max_points = 999

    return Level(start,goal,points,conns,grid,[p_start, p_end, p_middle], max_points, BG)

if __name__=="__main__":

    lvl1().save_level("lvl1")
