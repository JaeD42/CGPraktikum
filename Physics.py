from settings import *
import pygame
class Physics:

    def __init__(self,connections,points,train,level):

        self.connections = set(connections)
        self.points = set(points)
        self.removed_points = set()
        self.train = train
        self.bg = level.get_background()
        self.level = level
        self.plateaus = level.plateaus


    def add_connection(self,connection):
        self.connections.add(connection)

    def remove_connection(self,connection):
        self.connections.remove(connection)

    def add_point(self,point):
        self.points.add(point)

    def remove_point(self,point):
        self.points.remove(point)


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

            self.train.collision_with_level(self.level)



    def move(self,dt):

        if not PAUSE:
            for p in self.points:
                p.move(dt)
            self.train.move(dt)

    def change_bridge_mode(self):
        for c in self.connections:
            c.bridge_mode = not c.bridge_mode

    def draw(self,screen, ZOOM,TRANSLATE):
        screen.blit(*self.bg.get_img(SCREEN_MIDDLE,0,1,[0,0]))

        for plat in self.plateaus:
            plat.draw(screen,ZOOM,TRANSLATE)

        for c in self.connections:
            c.draw(screen,ZOOM,TRANSLATE)
        for p in self.points:
            p.draw(screen,ZOOM,TRANSLATE)

        self.train.draw(screen,ZOOM,TRANSLATE)
