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


def lvl0():
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

def lvl1():
    h = 200
    mid = int(SCREEN_WIDTH/2)
    y_scale = 2
    p1 = [[-200,h],[200, h]]
    p2 = [[mid -70,h+180],[mid+40,h+180]]
    p3 = [[SCREEN_WIDTH-200, h], [SCREEN_WIDTH+200, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_mid = Plateau(p2[0], p2[1], PLATEAU_IMGS[1], img_scale_x = 0.4)
    p_end = Plateau(p3[0], p3[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_start.flipped = True

    grid_step = 10
    grid_x = [30, 65]
    grid_y = [SCREEN_WIDTH-10, SCREEN_HEIGHT-30]

    grid = Grid.create_standard_grid(grid_x,grid_y,grid_step*3,int(grid_step*1.5))

    plateaus = [p_start, p_mid, p_end]

    start = TRAIN_START_COORD
    goal = [p3[0][0] + 50, p3[0][1]]


    points = []
    conns = []
    fixed_points_pos = [(200, 210), (595, 385), (680, 385), (1120, 210)]
    for i in fixed_points_pos:
        grid.add_grid_point(i)
        p = MassPoint(i, moveable = False)
        points.append(p)



    max_points =400

    return Level(start, goal, points, conns, grid, plateaus, max_points, BG)


def lvl2():
    h = 150
    mid = int(SCREEN_WIDTH/2)
    y_scale = 1.5
    p1 = [[-350,h],[65, h]]
    p2 = [[mid-150,h+250],[652, 531]]
    p2_2 = [[mid,h+350],[mid+100,h+250]]
    p3 = [[SCREEN_WIDTH-80, h], [SCREEN_WIDTH+200, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_mid1 = Plateau(p2[0], p2[1], PLATEAU_IMGS[5], img_scale_y = y_scale)
    p_mid2 = Plateau(p2_2[0], p2_2[1], PLATEAU_IMGS[6], img_scale_y = y_scale, img_offset = [0,-100])
    p_end = Plateau(p3[0], p3[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_start.flipped = True

    grid_step = 10
    grid_x = [0, 0]
    grid_y = [SCREEN_WIDTH, SCREEN_HEIGHT]

    grid = Grid.create_standard_grid(grid_x,grid_y,66,31)

    plateaus = [p_start, p_mid1, p_mid2, p_end]

    start = TRAIN_START_COORD
    goal = [p3[0][0] + 50, p3[0][1]]


    points = []
    conns = []
    fixed_points_pos = [(60, 160), (500, 400), (540, 400), (660, 550),(780, 400), (820,400), (1240, 160)]
    for i in fixed_points_pos:
        grid.add_grid_point(i)
        p = MassPoint(i, moveable = False)
        points.append(p)



    max_points =500

    return Level(start, goal, points, conns, grid, plateaus, max_points, BG2)


def lvl3():
    h = 250
    mid = int(SCREEN_WIDTH/2)
    y_scale = 1.5
    p1 = [[-300,h],[120, h]]
    p2 = [[mid-450,h+350],[450, 500]]
    p2_2 = [[mid+200,h+250],[mid+450,h+350]]
    p3 = [[SCREEN_WIDTH-120, h], [SCREEN_WIDTH+200, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_mid1 = Plateau(p2[0], p2[1], PLATEAU_IMGS[4], img_scale_y = y_scale, img_offset = [0,-100])
    p_mid2 = Plateau(p2_2[0], p2_2[1], PLATEAU_IMGS[4], img_scale_y = y_scale)
    p_end = Plateau(p3[0], p3[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_start.flipped = True
    p_mid2.flipped = True

    grid_step = 10
    grid_x = [0, 0]
    grid_y = [SCREEN_WIDTH, SCREEN_HEIGHT]

    grid = Grid.create_standard_grid(grid_x,grid_y,66,31)

    plateaus = [p_start, p_mid1, p_mid2, p_end]

    start = TRAIN_START_COORD
    goal = [p3[0][0] + 50, p3[0][1]]


    points = []
    conns = []
    fixed_points_pos = [(120, 260), (120, 100), (440, 500), (860, 500), (1180, 100), (1180, 260)]
    for i in fixed_points_pos:
        grid.add_grid_point(i)
        p = MassPoint(i, moveable = False)
        points.append(p)



    max_points =500

    return Level(start, goal, points, conns, grid, plateaus, max_points, BG)


if __name__=="__main__":

    lvl3().save_level("lvl3")
