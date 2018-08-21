
import pygame
from Connection import Connection

class MassPoint:

    def __init__(self,pos,weight,radius=5,moveable=True):
        self.pos=[float(i) for i in pos]
        self.v = [0.0,0.0]
        self.weight=weight
        self.connections = []
        self.radius=radius
        self.moveable=moveable

    def connect_to(self,other_point,length,strength):
        c = Connection(self,other_point,length,strength)
        self.connections.append(c)
        other_point.connections.append(c)
        return c


    def distance_to(self,other_point):
        return ((self.pos[0]-other_point.pos[0])**2+(self.pos[1]-other_point.pos[1])**2)**0.5


    def move(self,dt,gravity=9.81):
        if not self.moveable:
            return
        for connection in self.connections:
            center = connection.get_center()
            dir = [center[0]-self.pos[0],center[1]-self.pos[1]]
            l = (dir[0]**2+dir[1]**2)**0.5



            self.v[0] += dt*(connection.force/self.weight)*(dir[0]/l)

            self.v[1] += dt*(connection.force/self.weight)*(dir[1]/l)


        if gravity:
            self.v[1] += dt*gravity/self.weight

        self.pos[0] += dt*self.v[0]
        self.pos[1] += dt*self.v[1]

    def draw(self,surface,zoom=1,translation=[0,0]):
        pygame.draw.circle(surface,(0,0,255),self.get_int_pos(zoom,translation),int(self.radius*zoom))

    def get_int_pos(self,zoom,translation):
        return [int((translation[i]+self.pos[i])*zoom) for i in range(2)]

    def get_pos(self):
        return self.pos


def create_bridge(start_pos,width,height,num_points,weight=5,D=50):
    points = []
    upper_points = []
    cur = start_pos[:]

    lH = width/(num_points-1)
    lV = height

    lD = (lH**2+lV**2)**0.5

    for i in range(num_points):
        points.append(MassPoint(cur,weight))
        cur[0]+=lH
    cur = start_pos
    cur[1]-=height
    cur[0]+=lH
    for i in range(num_points-2):
        upper_points.append(MassPoint(cur,weight))
        cur[0]+=lH

    connections = []
    for i in range(1,num_points):
        connections.append(points[i].connect_to(points[i-1],lH+1,D))



    for i in range(1,num_points-1):
        connections.append(points[i].connect_to(upper_points[i-1],lV,D))

        connections.append(points[i+1].connect_to(upper_points[i-1],lD,D))
        connections.append(points[i-1].connect_to(upper_points[i-1],lD,D))

    for i in range(1,num_points-2):
        connections.append(upper_points[i].connect_to(upper_points[i-1],lH,D))

    points[0].moveable=False
    points[-1].moveable=False


    points.extend(upper_points)

    return points,connections
