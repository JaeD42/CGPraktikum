from Game.Physics import *
from Utils.settings import *
from Objects.Points import MassPoint,create_bridge
from Objects.Connection import Connection
from Graphics.Effects import Effects

import pickle
from tkinter import *
from tkinter import messagebox
from Objects.Grid import Grid
import sys
if (sys.version_info > (3, 0)):
    import tkinter.simpledialog as simpledialog
else:
    import tkSimpleDialog as simpledialog
class Bridge():
    def __init__(self, points, connections):
        self.points = [p.create_pickleable() for p in points]
        self.connections = [c.create_pickleable() for c in connections]


    def load_from_pickled(self):
        points = {}
        for p in self.points:
            points[p[0]] = MassPoint(p[1], p[2], p[3], p[4])
        conns = []
        for c in self.connections:
            conns.append(points[c[0]].connect_to(points[c[1]],c[2],c[3],c[5],c[4]))
        return list(points.values()),conns

    def save_bridge(self, file = ""):
        try:
            if(not file):
                Tk().wm_withdraw() #to hide the main window
                file=simpledialog.askstring("Save", "Please enter filename:")
                file = os.path.join(BRIDGE_DIR, file+".bridge")
            filehandler = open(file, 'wb')
            pickle.dump(self, filehandler)
        except:
            print('save failed')

class BridgeCreator():

    def __init__(self,level):
        self.effects = Effects()

        self.removed_points = []
        self.removed_connections = []
        self.cost = level.get_max_points()

        self.bg = level.get_background()
        self.grid = level.get_grid()
        self.points =level.get_points()
        self.connections = level.get_connections()
        self.level = level
        self.plateaus = level.plateaus


    def save_bridge(self, file = ""):
        try:
            if(not file):
                Tk().wm_withdraw() #to hide the main window
                file=simpledialog.askstring("Save", "Please enter filename:")
                file = os.path.join(BRIDGE_DIR, file+".bridge")
            filehandler = open(file, 'wb')
            pickle.dump(Bridge(self.points, self.connections), filehandler)
        except:
            print('save failed')

    def load_bridge(self, file = "", bridge=None):
        try:
            if (bridge!=None):
                self.points,self.connections = bridge.load_from_pickled()


            elif(not file):
                Tk().wm_withdraw() #to hide the main window
                file=simpledialog.askstring("Load", "Please enter filename:")
                file = os.path.join(BRIDGE_DIR, file+".bridge")

            if(bridge==None):
                filehandler = open(file, 'rb')
                bridge = pickle.load(filehandler)
                self.points,self.connections = bridge.load_from_pickled()

            print("here")
            self.grid.empty()
            self.grid.restore_points(self.points)
            self.cost = self.level.get_max_points()
            for p in self.points:
                if p.moveable:
                    self.cost -=POINT_COST
                else:
                    p.set_mutable(False)
            for c in self.connections:
                self.cost -=CONNECTION_COST
        except:
            print("load failed")




    def change_points(self,amount):
        self.cost += amount
        if amount>0:
            self.effects.change_money(amount,pygame.mouse.get_pos(),2000,col=(0,255,0))
        else:
            self.effects.change_money(amount,pygame.mouse.get_pos(),2000,col=(255,0,0))



    def add_point(self, coord):
        if(self.cost >= POINT_COST):
            if(not self.grid.point_exists(coord) and self.grid.no_close_points(coord,MIN_POINT_DIST)):
                p =self.grid.add_point_at_pos(coord)
                self.points.append(p)
                self.change_points(-1*POINT_COST)


    def add_connection(self, coord1, coord2,is_floor=False):
        exists1,p1 = self.grid.get_closest_point(coord1)
        exists2,p2 = self.grid.get_closest_point(coord2)
        if not exists1 or not exists2:
            return

        #check if valid points
        if(not(p1 and p2)):
            return

        if((not p1.moveable) and (not p2.moveable)):
            return
        #check if connection already exists
        if(not p1.is_connected_to(p2) and self.cost >= CONNECTION_COST):
            try:
                c = p1.connect_to_quick(p2,can_collide=is_floor)
                self.connections.append(c)
                self.change_points(-1* CONNECTION_COST)
            except:
                print('connection too long')

        #if not, add in self.connections and to points

    def delete_point(self, coord):
        ex,p = self.grid.get_point_at_pos(coord)
        if ex and p.mutable:
            p = self.grid.remove_point_at_pos(coord)
            self.removed_points.append(p)
            self.points.remove(p)
            self.change_points(POINT_COST)
            #delete all connections
            print(len(p.connections))
            for i in p.connections:
                self.connections.remove(i)
                self.change_points(CONNECTION_COST)
            [i.remove() for i in p.connections[:]]

            print(len(p.connections))

    def delete_connection(self, coord1, coord2):
        ex1,p1 = self.grid.get_point_at_pos(coord1)
        ex2,p2 = self.grid.get_point_at_pos(coord2)
        if(not(ex1 and ex2)):
            return

        check, c = p1.get_connection_to(p2)
        if(check and c.mutable):
            self.connections.remove(c)
            c.remove()
            self.change_points(CONNECTION_COST)

    def change_point_mass(self, coord):
        pass

    def change_point_moveable(self, coord):
        ex,p = self.grid.get_point_at_pos(coord)
        if ex and p.mutable and (p.moveable and self.cost >= FIXED_CON_COST):
            p.change_moveable()
            self.change_points(-1*FIXED_CON_COST)
        elif ex and p.mutable and (not p.moveable):
            p.change_moveable()
            self.change_points(FIXED_CON_COST)


    def check_if_con_exists(self, pos1, pos2):
        ex1,p1 = self.grid.get_point_at_pos(pos1)
        ex2,p2 = self.grid.get_point_at_pos(pos2)
        if(ex1 and ex2):
            return p1.is_connected_to(p2)
        else:
            return False


    def draw(self,screen, ZOOM, TRANSLATE):

        for plat in self.plateaus:
            plat.draw(screen,ZOOM,TRANSLATE)
        for c in self.connections:
            c.draw(screen,ZOOM,TRANSLATE)
        for p in self.points:
            p.draw(screen,ZOOM,TRANSLATE)

        cost_display = pygame.font.Font(None, 20)
        cost_display = cost_display.render('Points remaining: '+ str(self.cost), True, (255,255,255))
        screen.blit(cost_display, (10,SCREEN_HEIGHT-30))
        self.effects.draw(screen)

    def change_bridge_mode(self):
        Connection.bridge_mode = not Connection.bridge_mode
        #for c in self.connections:
        #    c.bridge_mode = not c.bridge_mode

    def get_hover_object(self,pos):
        pass

    def show_grid(self,screen,ZOOM,TRANSLATE):
        self.grid.draw(screen,ZOOM,TRANSLATE)
