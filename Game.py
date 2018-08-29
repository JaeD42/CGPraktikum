from BridgeCreator import Bridge
from Grid import Grid
import pickle
from RotateTranslateImage import RTImage
import pygame
from load_data import load_image
from settings import *
class Game:

    def __init__(self):
        self.levels = []
        self.current_level = None




class Level:

    def __init__(self,start,goal,points,conns,grid,plateaus,max_points,bg):

        self.plateaus = plateaus
        self.start = start
        self.goal = goal
        self.points = points
        self.connections = conns
        self.grid = grid
        self.max_points = max_points
        self.back_ground_path = bg
        self.bg = None
        #self.load_level()

    @staticmethod
    def load_from_file(path):
        l = Level(None,None,None,None,None,None,None,None)
        l.load_level(path)
        return l




    def game_is_won(self,train):
        c = train.wagons[0].center
        if c[0]>self.goal[0] and c[1]<self.goal[1]:
            print("WON")
            return True
        return False



    def save_level(self,path):
        b = Bridge(self.points,self.connections)
        d={}
        d["points"]=b.points
        d["connections"]=b.connections
        d["start"]=self.start
        d["goal"]=self.goal
        d["plateaus"]=self.plateaus
        d["grid"]=self.grid.positions
        d["max_money"]=self.max_points
        d["bg"]=self.back_ground_path

        filehandler = open(path, 'wb')
        pickle.dump(d,filehandler)
        filehandler.close()



    def load_plateau_imgs(self):
        for p in self.plateaus:
            img = load_image(p.path)
            if(p.flipped):
                img = pygame.transform.flip(img,True, False)
            p.add_img(img)

    def load_level(self,path):
        filehandler = open(path, 'rb')
        d = pickle.load(filehandler)
        filehandler.close()

        pickled_points = d["points"]
        pickled_connections = d["connections"]
        self.points,self.connections = Bridge(pickled_points,pickled_connections).load_from_pickled()
        self.start = d["start"]
        self.goal = d["goal"]
        self.plateaus = d["plateaus"]
        self.grid = Grid(d["grid"])
        self.grid.restore_points(self.points)


        self.max_points = d["max_money"]
        self.back_ground_path = d["bg"]
        self.bg = RTImage(pygame.transform.smoothscale(load_image(self.back_ground_path), (SCREEN_WIDTH, SCREEN_HEIGHT)))


    def get_max_points(self):
        return self.max_points

    def get_grid(self):
        return self.grid

    def get_points(self):
        return self.points

    def get_connections(self):
        return self.connections

    def get_background(self):
        return self.bg


if __name__=="__main__":
    from Plateau import Plateau
    from Grid import Grid
    from settings import *

    p1 = [[-200,400], [100,400]]
    p2 = [[1500, 400], [1800, 400]]
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

    l = Level(start,goal,points,conns,grid,[p_start, p_end, p1], max_points, BG)
    l.save_level("lvl1")
