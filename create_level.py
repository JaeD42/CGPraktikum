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
    h = 300
    p1 = [[-200,h], [230,h]]
    p2 = [[1150, h], [1500, h]]
    p3 = [[400, h], [700, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0])
    p_start.flipped = True
    p_end = Plateau(p2[0], p2[1] ,PLATEAU_IMGS[0])
    p_middle = Plateau(p3[0], p3[1], PLATEAU_IMGS[1])
    p_middle.in_front = True

    grid = Grid.create_standard_grid((100,100),(1200,500),10,10)
    start = TRAIN_START_COORD
    goal = BRIDGE_END
    points = []
    conns = []
    max_points = 999

    fixed_points_pos = [(225, 325), (225, 400), (650, 500), (1170, 300)]
    

    return Level(start,goal,points,conns,grid,[p_start, p_end, p_middle], max_points, BG)

if __name__=="__main__":

    lvl1().save_level("lvl1")
