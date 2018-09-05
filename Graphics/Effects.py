#!/usr/bin/env python
'''
    Author: Jana Becker, Jan Disselhoff
'''

import pygame
import time
import math

class Effects:

    def __init__(self):
        self.effects = []
        self.font = pygame.font.Font(None,20)

    def change_money(self,cost,pos,duration=500,col=(255,0,0)):
        self.effects.append((self.font.render(str(cost),True,col),time.time(),float(duration)/1000,pos))

    def draw(self,screen):
        to_remove = []
        rects = []
        for values in self.effects:
            surf,start,max_time,pos = values
            if time.time()-start>max_time:
                to_remove.append(values)
            else:
                posx,posy = pos
                posy =int(posy-((time.time()-start)*20)/max_time)
                posx =int(posx+(math.sin(5*(time.time()-start))*5))
                rects.append(screen.blit(surf,(posx,posy)))
        for i in to_remove:
            self.effects.remove(i)
        return rects


from Objects.SmokeSimulation import SmokeSimulation
class SmokeEffect:

    def __init__(self):
        self.effects = []

    def add_smoke(self,pos,duration,num_particles=25):
        self.effects.append([SmokeSimulation(num_particles,pos),duration,duration])

    def update(self,dt):
        to_remove = []
        for val in self.effects:
            val[1]-=1
            if val[1]<0:
                to_remove.append(val)
            else:
                val[0].step(dt)
        for s in to_remove:
            self.effects.remove(s)

    def draw(self,screen):

        return [val[0].draw(screen,[int(255*(1-float(val[1])/val[2]))]*3) for val in self.effects]
