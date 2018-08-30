from Utils.settings import *
from Objects.Points import MassPoint

class Grid:

    def __init__(self,positions=[]):
        self.positions = positions
        self.points = {}
        self.old_zoom = 1
        self.old_t = [0,0]
        self.old_grid = None



    @staticmethod
    def create_standard_grid(upper_left,lower_right,num_points_x,num_points_y):
        width = lower_right[0]-upper_left[0]
        height = lower_right[1]-upper_left[1]
        positions = []
        for i in range(num_points_x):
            for j in range(num_points_y):
                positions.append([upper_left[0]+float(width)*i/(num_points_x-1),upper_left[1]+float(height)*j/(num_points_y-1)])
        g = Grid()
        g.positions=positions
        return g

    def no_close_points(self,pos,dist):
        for p in self.points:
            continue

    def empty(self):
        self.points={}

    def restore_points(self,points):
        for p in points:
            pos = self.get_closest_grid_pos(p.pos)
            self.points[tuple(pos)]=p


    def get_closest_grid_pos(self,pos):
        minDist = 10**5
        minPos = None
        for grid_pos in self.positions:
            d = abs(grid_pos[0]-pos[0])+abs(grid_pos[1]-pos[1])
            if d<minDist:
                minDist = d
                minPos = grid_pos
        return minPos[:]


    def add_grid_point(self,pos):
        self.positions.append(pos)

    def remove_grid_point(self,pos):
        self.positions.remove(pos) #??

    def point_exists(self,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        if t in self.points:
            return True
        return False

    def get_point_at_pos(self,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        if t in self.points:
            return True,self.points[t]
        return False,None

    def add_point_at_pos(self,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        self.points[t]=MassPoint(t,NODE_MASS)
        return self.points[t]

    def remove_point_at_pos(self,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        P = self.points[t]
        del self.points[t]
        return P

    def is_valid_grid_pos(self,pos,max_dist):
        minDist = 10**5
        minPos = None
        for grid_pos in self.positions:
            d = abs(grid_pos[0]-pos[0])+abs(grid_pos[1]-pos[1])
            if d<minDist:
                minDist = d
                minPos = grid_pos
        return minDist<max_dist

    def is_same_grid_pos(self,pos1,pos2):
        return self.get_closest_grid_pos(pos1)==self.get_closest_grid_pos(pos2)

    def draw(self,screen,z,t):
        if self.old_grid==None or self.old_zoom!=z or self.old_t!=t:
            surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
            offset = 2
            grid_line = pygame.Surface((2*offset+1,2*offset+1), pygame.SRCALPHA)
            pygame.draw.line(grid_line, (0,0,0, 100), (offset, 0), (offset, 2*offset+1))
            pygame.draw.line(grid_line, (0,0,0, 100), (0, offset), (2*offset+1,offset))

            for pos in self.positions:
                posx = (pos[0]+t[0])*z-offset
                posy = (pos[1]+t[1])*z-offset
                surf.blit(grid_line, (posx,posy))
            self.old_grid = surf
            self.old_zoom = z
            self.old_t = t[:]
        screen.blit(self.old_grid,(0,0))
