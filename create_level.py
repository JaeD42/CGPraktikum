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
from Objects.Points import MassPoint


def lvl1():
    h = 300
    p1 = [[-200,h], [230,h]]
    p2 = [[1150, h], [1500, h]]
    p3 = [[400, h], [700, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0])
    p_start.flipped = True
    p_end = Plateau(p2[0], p2[1] ,PLATEAU_IMGS[0])
    p_middle = Plateau(p3[0], p3[1], PLATEAU_IMGS[1])

    grid = Grid.create_standard_grid((100,100),(1200,500),10,10)
    #todo
    start = TRAIN_START_COORD
    goal = BRIDGE_END
    points = []
    conns = []
    max_points = 999

    fixed_points_pos = [(225, 325), (225, 400), (650, 500), (1170, 300)]


    return Level(start,goal,points,conns,grid,[p_start, p_end, p_middle], max_points, BG)

def lvl2():
    h = 200
    mid = int(SCREEN_WIDTH/2)
    y_scale = 2
    p1 = [[-200,h],[200, h]]
    p2 = [[mid -70,h+200],[mid+70,h+200]]
    p3 = [[SCREEN_WIDTH-200, h], [SCREEN_WIDTH+200, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_mid = Plateau(p2[0], p2[1], PLATEAU_IMGS[1], img_scale_x = 0.5)
    p_end = Plateau(p3[0], p3[1], PLATEAU_IMGS[1], img_scale_y = y_scale)
    p_start.flipped = True

    grid = Grid.create_standard_grid((100,100),(1200,500),10,10)

    plateaus = [p_start, p_mid, p_end]

    start = TRAIN_START_COORD
    goal = p3[0]


    points = []
    conns = []
    fixed_points_pos = [(200, 200), (580, 400), (700, 400), (1100, 200)]
    for i in fixed_points_pos:
        grid.add_grid_point(i)
        p = MassPoint(i)
        p.set_mutable(False)
        point.append(p)



    max_points = 100

    return Level(start, goal, points, conns, grid, plateaus, max_points, BG)


if __name__=="__main__":

    lvl2().save_level("lvl2")
