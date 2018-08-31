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
def lvl4():
    w = 1300
    h = 600

    h = 150
    mid = int(SCREEN_WIDTH/2)

    y_scale = 1.5
    p1 = [[-350,h],[50, h]]
    p2 = [[4*SCREEN_WIDTH//9-25, 550],[4*SCREEN_WIDTH//9+25, 550]]
    p2_2 = [(6*SCREEN_WIDTH//9-25, 550),(6*SCREEN_WIDTH//9+25, 550)]
    p3 = [[SCREEN_WIDTH-50, h], [SCREEN_WIDTH+200, h]]
    p_start = Plateau(p1[0], p1[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_mid1 = Plateau(p2[0], p2[1], PLATEAU_IMGS[5], img_scale_y = y_scale,img_offset=[0,0])
    p_mid2 = Plateau(p2_2[0], p2_2[1], PLATEAU_IMGS[5], img_scale_y = y_scale, img_offset = [-128,0])
    p_end = Plateau(p3[0], p3[1], PLATEAU_IMGS[0], img_scale_y = y_scale)
    p_start.flipped = True
    p_mid2.flipped = True

    grid_x = [0, 0]
    grid_y = [SCREEN_WIDTH, SCREEN_HEIGHT]

    grid = Grid.create_standard_grid(grid_x,grid_y,63,31)

    plateaus = [p_start,p_mid1,p_mid2, p_end]

    start = TRAIN_START_COORD
    goal = [p3[0][0] + 50, p3[0][1]]


    points = []
    conns = []
    fixed_points_pos = [(63, 161), (585, 560), (860, 560), (SCREEN_WIDTH-41,161)]
    for i in fixed_points_pos:
        grid.add_grid_point(i)
        p = MassPoint(i, moveable = False)
        points.append(p)



    max_points =700

    return Level(start, goal, points, conns, grid, plateaus, max_points, BG3)

if __name__=="__main__":
    l = lvl4()
    l.save_level("lvl4")
