
import pygame
import numpy as np
from math import sqrt
from Connection import Connection
from settings import DEBUG

class MassPoint:

    def __init__(self,pos,weight,radius=5,moveable=True):
        self.pos=np.array([float(i) for i in pos])
        self.v = [0.0,0.0]
        self.weight=weight
        self.connections = []
        self.radius=radius
        self.moveable=moveable
        self.add_force = [0.0,0.0]
        self.prev_force = [0.0,0.0]

    def connect_to(self,other_point,length,strength,can_collide=False,max_force=1000):
        c = Connection(self,other_point,length,strength,max_force=max_force,can_collide=can_collide)
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


        if gravity:
            self.v[1] += dt*gravity/self.weight

        self.v[0] += dt*self.add_force[0]/self.weight
        self.v[1] += dt*self.add_force[1]/self.weight
        if DEBUG:
            self.prev_force = self.add_force[:]
        self.add_force = [0.0,0.0]

        self.pos[0] += dt*self.v[0]
        self.pos[1] += dt*self.v[1]

    def draw(self,surface,zoom=1,translation=[0,0]):
        pygame.draw.circle(surface,(min(self.prev_force[1],255),0,255),self.get_int_pos(zoom,translation),int(self.radius*zoom))

    def get_int_pos(self,zoom,translation):
        return [int((translation[i]+self.pos[i])*zoom) for i in range(2)]

    def get_pos(self):
        return self.pos

    def connect_to_quick(self,other_point,strength=300,can_collide=False,max_force=1000):
        return self.connect_to(other_point,self.distance_to(other_point),strength,can_collide,max_force)

    def is_connected_to(self,other_point):
        for c in self.connections:
            if c.p1==other_point or c.p2==other_point:
                return True
        return False
        
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
