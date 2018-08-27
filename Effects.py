import pygame
import time

class Effects:

    def __init__(self):
        self.effects = []
        self.font = pygame.font.Font(None,20)

    def change_money(self,cost,pos,duration=500,col=(255,0,0)):
        self.effects.append((self.font.render(str(cost),True,col),time.time(),float(duration)/1000,pos))

    def draw(self,screen):
        to_remove = []
        for values in self.effects:
            surf,start,max_time,pos = values
            if time.time()-start>max_time:
                to_remove.append(values)
            else:
                posx,posy = pos
                posy =int(posy-((time.time()-start)*20)/max_time)
                screen.blit(surf,(posx,posy))
        for i in to_remove:
            self.effects.remove(i)


from SmokeSimulation import SmokeSimulation
class SmokeEffect:

    def __init__(self):
        self.effects = []

    def add_smoke(self,pos,duration,num_particles=25):
        self.effects.append([SmokeSimulation(num_particles,pos),duration,duration])

    def draw(self,screen):
        to_remove = []
        for val in self.effects:
            val[1]-=1
            if val[1]<0:
                to_remove.append(val)
            else:
                val[0].step(0.03)
                val[0].draw(screen,[int(255*(1-float(val[1])/val[2]))]*3)
