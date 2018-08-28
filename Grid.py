

class Grid:

    def __init__(self):
        self.positions = []
        self.points = {}

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

    def get_point_at_pos(self,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        if t in self.points:
            return True,self.points[t]
        return False,None

    def add_point_at_pos(self,point,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        self.points[t]=point

    def remove_point_at_pos(self,pos):
        t = tuple(self.get_closest_grid_pos(pos))
        del self.points[t]

    def is_valid_grid_pos(self,pos,max_dist):
        pass

    def is_same_grid_pos(self,pos1,pos2):
        return self.get_closest_grid_pos(pos1)==self.get_closest_grid_pos(pos2)

    def draw(self,screen):
        pass
