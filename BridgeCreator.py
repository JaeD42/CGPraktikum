from Physics import *
from settings import *
from Points import MassPoint,create_bridge
from Connection import Connection
from Effects import Effects

class BridgeCreator():

    removed_points = []
    removed_connections = []


    def __init__(self,back_ground, cost):
        self.points = []
        self.connections = []
        #self.points, self.connections = create_bridge()
        self.effects = Effects()

        points,connections = create_bridge(BRIDGE_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES, D=BRIDGE_STIFF, max_force = 2000)

        BRIDGE2_START = [BRIDGE_START[0],BRIDGE_START[1]+200]
        points2,connections2 = create_bridge(BRIDGE2_START,BRIDGE_END,BRIDGE_HEIGHT, BRIDGE_NODES-1, D=BRIDGE_STIFF*2, max_force = 10000)
        conn = connections2[2]
        add_point = MassPoint((SCREEN_WIDTH,240),5,moveable=False)
        add_conn = points2[3].connect_to_quick(add_point,can_collide=True)

        points.extend(points2)
        connections.extend(connections2)
        points.append(add_point)
        connections.append(add_conn)

        self.points = points
        self.connections = connections


        self.cost = cost
        self.grid_size = GRID_SIZE
        self.bg = back_ground
        self.grid = {}

        for p in self.points:
            gx = int(p.pos[0]/self.grid_size+0.5)
            gy = int(p.pos[1]/self.grid_size+0.5)
            self.grid[(gx,gy)] = p


    def get_grid_intersections(self):
        for i in range(1,int(SCREEN_WIDTH/self.grid_size) -1):
            for j in range(1, int(SCREEN_HEIGHT/self.grid_size) -1):
                yield((i*self.grid_size,j*self.grid_size))


    def change_points(self,amount):
        self.cost += amount
        if amount>0:
            self.effects.change_money(amount,pygame.mouse.get_pos(),2000,col=(0,255,0))
        else:
            self.effects.change_money(amount,pygame.mouse.get_pos(),2000,col=(255,0,0))



    def add_point(self, coord):
        if(self.cost >= POINT_COST):
            grid_pos = self.get_grid_pos(coord)
            if(not self.check_which_point(grid_pos)):
                p = MassPoint(self.get_coordinates(grid_pos), NODE_MASS, moveable=True)
                self.grid[grid_pos] = p
                self.points.append(p)
                self.change_points(-1*POINT_COST)


    def add_connection(self, coord1, coord2,is_floor=False):
        grid_pos1 = self.get_grid_pos(coord1)
        grid_pos2 = self.get_grid_pos(coord2)
        if not grid_pos1 in self.grid or not grid_pos2 in self.grid:
            return
        p1 = self.grid[grid_pos1]
        p2 = self.grid[grid_pos2]

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

    def delete_point(self, coord1):
        grid_pos = self.get_grid_pos(coord)
        if(self.grid[grid_pos]):
            p = self.grid[grid_pos]
            self.removed_points.append(p)
            self.grid[grid_pos] = None
            self.points.remove(p)
            self.change_points(POINT_COST)
            #delete all connections
            for i in p.connections:
                self.connections.remove(i)
                i.remove()
                self.change_points(CONNECTION_COST)

    def delete_connection(self, coord1, coord2):
        grid_pos1 = self.get_grid_pos(coord1)
        grid_pos2 = self.get_grid_pos(coord2)
        p1 = self.grid[grid_pos1]
        p2 = self.grid[grid_pos2]
        if(not(p1 and p2)):
            return

        check, c = p1.get_connection_to(p2)
        if(check):
            self.connections.remove(c)
            c.remove()
            self.change_points(CONNECTION_COST)

    def change_point_mass(self, coord):
        pass

    def change_point_moveable(self, coord):
        p = self.check_which_point_image_coords(coord)
        if(p.moveable and self.cost >= FIXED_CON_COST):
            p.change_moveable()
            self.change_points(-1*FIXED_CON_COST)
        elif(not p.moveable):
            p.change_moveable()
            self.change_points(FIXED_CON_COST)



    def get_grid_pos_phys(self,coordinated):
        loc = ((coordinates[0]+self.grid_size/2)/self.grid_size, (coordinates[1]+self.grid_size/2)/self.grid_size)
        return loc

    #get the position in grid coordinates
    def get_grid_pos(self, coordinates):
        coord = [coordinates[0]/ZOOM-TRANSLATE[0],coordinates[1]/ZOOM-TRANSLATE[1]]
        loc = (int((coord[0]+self.grid_size/2)/self.grid_size), int((coord[1]+self.grid_size/2)/self.grid_size))
        return loc

    def get_coordinates(self, grid_pos):
        return [grid_pos[0]*self.grid_size, grid_pos[1]*self.grid_size]

    def check_if_con_exists(self, pos1, pos2):
        p1 = self.check_which_point_image_coords(pos1)
        p2 = self.check_which_point_image_coords(pos2)
        print(p1.is_connected_to(p2))
        return p1.is_connected_to(p2)

    #check if there is a point on that position
    def check_which_point(self, pos):
        if not pos in self.grid:
            return None
        else:
            return self.grid[pos]

    def check_which_point_image_coords(self,coord):
        pos = self.get_grid_pos(coord)
        return self.check_which_point(pos)

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
