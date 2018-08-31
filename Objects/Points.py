
import pygame
import numpy as np
from math import sqrt
from Objects.Connection import Connection
from Utils.settings import DEBUG, NODE_MASS, WEIGHT_PER_LENGTH, MAX_FORCE, BRIDGE_STIFF, SCREEN_WIDTH, SCREEN_HEIGHT
from itertools import count

MAX_COL = np.array([6,51,66])
MIN_COL = np.array([81, 128, 143])
WHITE = [255,255,255]

class MassPoint:

    _indx=count(0)

    def __init__(self,pos,weight = NODE_MASS,radius=6,moveable=True, mutable=True):
        self.pos=np.array([float(i) for i in pos])
        self.v = [0.0,0.0]
        self.start_weight = weight
        self.weight=weight
        self.connections = []
        self.radius=radius
        self.moveable=moveable
        self.add_force = [0.0,0.0]
        self.prev_force = [0.0,0.0]
        self.point_num = next(self._indx)
        self.mutable = mutable



    def create_pickleable(self):
        return [self.point_num, list(self.pos)[:], self.start_weight, self.radius, self.moveable]

    def set_mutable(self,mutable):
        self.mutable = mutable

    def connect_to(self,other_point,length,strength,can_collide=False,max_force=MAX_FORCE):
        c = Connection(self,other_point,length,strength,max_force=max_force,can_collide=can_collide)
        self.weight += length*WEIGHT_PER_LENGTH
        other_point.weight +=length*WEIGHT_PER_LENGTH
        self.connections.append(c)
        other_point.connections.append(c)
        return c


    def distance_to(self,other_point):
        return sqrt((self.pos[0]-other_point.pos[0])**2+(self.pos[1]-other_point.pos[1])**2)

    def move(self,dt,gravity=9.81):
        if not self.moveable:
            return

        pre = dt/self.weight
        for connection in self.connections:
            center = connection.center
            dir = [center[0]-self.pos[0],center[1]-self.pos[1]]
            l = sqrt(dir[0]*dir[0]+dir[1]*dir[1])


            self.v[0] += (connection.force*pre)*(dir[0]/l)

            self.v[1] += (connection.force*pre)*(dir[1]/l)
        self.v[0]=self.v[0]*0.99
        self.v[1]=self.v[1]*0.99


        if gravity:
            self.v[1] += dt*gravity

        self.v[0] += dt*self.add_force[0]/self.weight
        self.v[1] += dt*self.add_force[1]/self.weight
        if DEBUG:
            self.prev_force = self.add_force[:]
        self.add_force = [0.0,0.0]

        self.pos[0] += dt*self.v[0]
        self.pos[1] += dt*self.v[1]

    def draw(self,surface,zoom=1,translation=[0,0]):
        if self.moveable:
            pos = self.get_int_pos(zoom,translation)
            if(pos[0] > SCREEN_WIDTH or pos[1] > SCREEN_HEIGHT or pos[0] < 1 or pos[1] < 1):
                return
            pos[0] -= 1
            pos[1] -= 1
            col = surface.get_at(pos)
            lam = min((col[0] + col[1] + col[2])/600,1)
            col_p = lam * MAX_COL +(1-lam)*MIN_COL
            col_p = [int(i) for i in col_p]

            col_p = WHITE[:]
            return pygame.draw.circle(surface,(col_p[0],col_p[1],col_p[2]),pos,int(self.radius*zoom))
        else:
            p = self.get_int_pos(zoom,translation)
            pos = [p[0]-int(self.radius*zoom),p[1]-int(self.radius*zoom)]
            if(pos[0] > SCREEN_WIDTH or pos[1] > SCREEN_HEIGHT or pos[0] < 1 or pos[1] < 1):
                return
            pos[0] -= 1
            pos[1] -= 1
            col = surface.get_at(pos)
            lam = min((col[0] + col[1] + col[2])/600,1)
            col_p = lam * MAX_COL +(1-lam)*MIN_COL
            col_p = [int(i) for i in col_p]

            col_p = WHITE[:]

            return pygame.draw.rect(surface,(col_p[0],col_p[1],col_p[2]),[p[0]-int(self.radius*zoom),p[1]-int(self.radius*zoom),2*int(self.radius*zoom),2*int(self.radius*zoom)])


    def get_int_pos(self,zoom,translation):
        return [int((translation[i]+self.pos[i])*zoom) for i in range(2)]

    def get_pos(self):
        return self.pos

    def connect_to_quick(self,other_point,strength=BRIDGE_STIFF,can_collide=False,max_force=MAX_FORCE):
        return self.connect_to(other_point,self.distance_to(other_point),strength,can_collide,max_force)


    def get_connection_to(self,other_point):
        for c in self.connections:
            if c.p1==other_point or c.p2==other_point:
                return True , c
        return False, None


    def is_connected_to(self,other_point):
        return self.get_connection_to(other_point)[0]

    def change_moveable(self):
        self.moveable = not self.moveable

def create_bridge(start_pos,end_pos,height,num_points,weight=4,D=300, max_force = 1000):
    points = []
    upper_points = []
    cur = start_pos[:]

    width = end_pos[0]-start_pos[0]
    lH = width/(num_points-1)
    lV = height

    lD = (lH**2+lV**2)**0.5

    for i in range(num_points):
        points.append(MassPoint(cur,weight))
        cur[0]+=lH
    cur = start_pos[:]
    cur[1]-=height
    cur[0]+=lH
    for i in range(num_points-2):
        upper_points.append(MassPoint(cur,weight))
        cur[0]+=lH

    connections = []
    for i in range(1,num_points):
        connections.append(points[i].connect_to(points[i-1],lH+1,D,can_collide=True,max_force=max_force))



    for i in range(1,num_points-1):
        connections.append(points[i].connect_to(upper_points[i-1],lV,D,max_force=max_force))

        connections.append(points[i+1].connect_to(upper_points[i-1],lD,D,max_force=max_force))
        connections.append(points[i-1].connect_to(upper_points[i-1],lD,D,max_force=max_force))

    for i in range(1,num_points-2):
        connections.append(upper_points[i].connect_to(upper_points[i-1],lH,D,max_force=max_force))

    points[0].moveable=False
    points[-1].moveable=False


    points.extend(upper_points)

    return points,connections
