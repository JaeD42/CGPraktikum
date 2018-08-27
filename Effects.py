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
