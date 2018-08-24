from Physics import *
from settings import *
from Points import MassPoint
from Connection import Connection

class BridgeCreator():

    removed_points = []
    removed_connections = []


    def __init__(self):
        self.points, self.connections = create_bridge()
        self.cost = COST
        self.grid_size = GRID_SIZE

        self.grid = {}

        for p in self.points:
            gx = int(p.pos[0]/grid_size)
            gy = int(p.pos[1]/grid_size)
            self.grid[(gx,gy)] = p


    def add_point(self, coord):
        grid_pos = self.get_grid_pos(coord)
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
            self.connections.add(c)


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

    #get the position in grid coordinates
    def get_grid_pos(self, coord):
        coord = [coordinates[0]/ZOOM-TRANSLATE[0],coordinates[1]/ZOOM-TRANSLATE[1]]
        loc = ((coordinates[0]+self.grid_size/2)/self.grid_size, (coordinates[1]+self.grid_size/2)/self.grid_size)
        return loc

    def get_coordinates(self, grid_pos):
        return [grid_pos[0]*self.grid_size, grid_pos[1]*self.grid_size]

    #check if there is a point on that position
    def check_which_point(self, pos):
        if not pos in self.grid:
            return None
        else:
            return self.grid[pos]
