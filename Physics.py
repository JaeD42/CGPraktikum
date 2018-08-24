from settings import *
import pygame
class Physics:

    def __init__(self,connections,points,train,back_ground,grid_size = 50):

        self.connections = set(connections)
        self.points = set(points)
        self.removed_points = set()
        self.train = train
        self.bg = back_ground
        self.grid_size = grid_size

        self.grid = {}

        for p in points:
            gx = int(p.pos[0]/grid_size)
            gy = int(p.pos[1]/grid_size)
            if not (gx,gy) in self.grid:
                self.grid[(gx,gy)]=[]
            self.grid[(gx,gy)].append(p)


    def add_connection(self,connection):
        self.connections.add(connection)

    def remove_connection(self,connection):
        self.connections.remove(connection)


    def get_point(self,coordinates):
        loc = (coordinates[0]/self.grid_size,coordinates[1]/self.grid_size)
        if not loc in self.grid:
            return None
        else:
            for p in self.grid[loc]:
                if p not in self.removed_points:
                    return p
        return None

    def add_point(self,point):
        self.points.add(point)
        gx = int(p.pos[0]/grid_size)
        gy = int(p.pos[1]/grid_size)
        if not (gx,gy) in self.grid:
            self.grid[(gx,gy)]=[]
        self.grid[(gx,gy)].append(p)

    def remove_point(self,point):
        self.points.remove(point)
        self.removed_points.add(point)


    def update_physics(self,dt):

        if not PAUSE:
            broken_conns = []
            for c in self.connections:
                broke = c.update_force()
                if broke:
                    broken_conns.append(c)
                    continue
                self.train.collision_with_connection(c)

            for c in broken_conns:
                self.remove_connection(c)



    def move(self,dt):

        if not PAUSE:
            for p in self.points:
                p.move(dt)
            self.train.move(dt)


    def draw(self,screen, ZOOM,TRANSLATE):
        screen.blit(*self.bg.get_img(SCREEN_MIDDLE,0,ZOOM,TRANSLATE))

        for c in self.connections:
            c.draw(screen,ZOOM,TRANSLATE)
        for p in self.points:
            p.draw(screen,ZOOM,TRANSLATE)

        self.train.draw(screen,ZOOM,TRANSLATE)
