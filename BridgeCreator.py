from Physics import *
from settings import *
from Points import MassPoint,create_bridge
from Connection import Connection
from Effects import Effects

import pickle
from tkinter import *
from tkinter import messagebox
from Grid import Grid
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

    def __init__(self,back_ground, cost):
        self.points = []
        self.connections = []
        #self.points, self.connections = create_bridge()
        self.effects = Effects()

        self.removed_points = []
        self.removed_connections = []

        # points,connections = create_bridge(BRIDGE_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES, D=BRIDGE_STIFF, max_force = 2000)
        #
        # BRIDGE2_START = [BRIDGE_START[0],BRIDGE_START[1]+200]
        # points2,connections2 = create_bridge(BRIDGE2_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES-1, D=BRIDGE_STIFF*2, max_force = 10000)
        # conn = connections2[2]
        # add_point = MassPoint((SCREEN_WIDTH,240),5,moveable=False)
        # add_conn = points2[3].connect_to_quick(add_point,can_collide=True)
        #
        # points.extend(points2)
        # connections.extend(connections2)
        # points.append(add_point)
        # connections.append(add_conn)

        # self.points = points
        # self.connections = connections


        self.cost = cost

        self.bg = back_ground
        print(Grid)
        self.grid = Grid.create_standard_grid((100,100),(1200,500),10,10)

        #for p in self.points:
        #    gx = int(p.pos[0]/self.grid_size+0.5)
        #    gy = int(p.pos[1]/self.grid_size+0.5)
        #    self.grid[(gx,gy)] = p


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
                return
            elif(not file):
                Tk().wm_withdraw() #to hide the main window
                file=simpledialog.askstring("Load", "Please enter filename:")
                file = os.path.join(BRIDGE_DIR, file+".bridge")
            filehandler = open(file, 'rb')
            bridge = pickle.load(filehandler)
            self.points,self.connections = bridge.load_from_pickled()
        except:
            print('load failed')




    def change_points(self,amount):
        self.cost += amount
        if amount>0:
            self.effects.change_money(amount,pygame.mouse.get_pos(),2000,col=(0,255,0))
        else:
            self.effects.change_money(amount,pygame.mouse.get_pos(),2000,col=(255,0,0))



    def add_point(self, coord):
        if(self.cost >= POINT_COST):
            if(not self.grid.point_exists(coord)):
                p =self.grid.add_point_at_pos(coord)
                self.points.append(p)
                self.change_points(-1*POINT_COST)


    def add_connection(self, coord1, coord2,is_floor=False):
        exists1,p1 = self.grid.get_point_at_pos(coord1)
        exists2,p2 = self.grid.get_point_at_pos(coord2)
        if not exists1 or not exists2:
            return

        #check if valid points
        if(not(p1 and p2)):
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

        if(self.grid.point_exists(coord)):
            p = self.grid.remove_point_at_pos(coord)
            self.removed_points.append(p)
            self.points.remove(p)
            self.change_points(POINT_COST)
            #delete all connections
            for i in p.connections:
                self.connections.remove(i)
                i.remove()
                self.change_points(CONNECTION_COST)

    def delete_connection(self, coord1, coord2):
        ex1,p1 = self.grid.get_point_at_pos(coord1)
        ex2,p2 = self.grid.get_point_at_pos(coord2)
        if(not(ex1 and ex2)):
            return

        check, c = p1.get_connection_to(p2)
        if(check):
            self.connections.remove(c)
            c.remove()
            self.change_points(CONNECTION_COST)

    def change_point_mass(self, coord):
        pass

    def change_point_moveable(self, coord):
        ex,p = self.grid.get_point_at_pos(coord)
        if ex and (p.moveable and self.cost >= FIXED_CON_COST):
            p.change_moveable()
            self.change_points(-1*FIXED_CON_COST)
        elif ex and (not p.moveable):
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
        screen.blit(*self.bg.get_img(SCREEN_MIDDLE,0,ZOOM,TRANSLATE))

        for c in self.connections:
            c.draw(screen,ZOOM,TRANSLATE)
        for p in self.points:
            p.draw(screen,ZOOM,TRANSLATE)

        cost_display = pygame.font.Font(None, 20)
        cost_display = cost_display.render('Points remaining: '+ str(self.cost), True, (255,255,255))
        screen.blit(cost_display, (10,SCREEN_HEIGHT-30))
        self.effects.draw(screen)

    def change_bridge_mode(self):
        for c in self.connections:
            c.bridge_mode = not c.bridge_mode

    def get_hover_object(self,pos):
        pass

    def show_grid(self,screen):
        self.grid.draw(screen)
