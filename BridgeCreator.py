from Physics import *
from settings import *
from Points import MassPoint,create_bridge
from Connection import Connection

class BridgeCreator():

    removed_points = []
    removed_connections = []


    def __init__(self,back_ground):
        self.points = []
        self.connections = []
        #self.points, self.connections = create_bridge()

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


        self.cost = COST
        self.grid_size = GRID_SIZE
        self.bg = back_ground
        self.grid = {}

        for p in self.points:
            gx = int(p.pos[0]/self.grid_size)
            gy = int(p.pos[1]/self.grid_size)
            self.grid[(gx,gy)] = p


    def add_point(self, coord):
        grid_pos = self.get_grid_pos(coord)
        print(grid_pos)
        if(not self.check_which_point(grid_pos)):
            p = MassPoint(self.get_coordinates(grid_pos), NODE_MASS, moveable=False)
            self.grid[grid_pos] = p
            self.points.append(p)


    def add_connection(self, coord1, coord2):
        grid_pos1 = self.get_grid_pos(coord1)
        grid_pos2 = self.get_grid_pos(coord2)
        p1 = self.grid[grid_pos1]
        p2 = self.grid[grid_pos2]

        #check if valid points
        if(not(p1 and p2)):
            return

        #check if connection already exists
        if(not p1.is_connected_to(p2)):
            c = p1.connect_to_quick(p2)
            self.connections.append(c)


        #if not, add in self.connections and to points

    def delete_point(self, coord1):
        grid_pos = self.get_grid_pos(coord)
        if(self.grid[grid_pos]):
            p = self.grid[grid_pos]
            self.removed_points.append(p)
            self.grid[grid_pos] = None
            self.points.remove(p)
            #delete all connections
            for i in p.connections:
                self.connections.remove(i)
                i.remove()

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

    def change_point_mass(self, coord):
        pass

    def change_point_movable(self, coord):
        pass

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

    def get_hover_object(self,pos):
        pass
