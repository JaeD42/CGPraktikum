import pygame
from settings import *

def calc_events():
    global ZOOM,TRANSLATE,PAUSE, ZOOM_FACTOR
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            #scrolling
            if event.button in [4,5]:
                (x,y) = pygame.mouse.get_pos()
                pZOOM = ZOOM
                if event.button == 4:
                    ZOOM+=ZOOM_FACTOR
                elif event.button == 5:
                    ZOOM=max(ZOOM-ZOOM_FACTOR,1)


                xI = (x/pZOOM-TRANSLATE[0])
                yI = (y/pZOOM-TRANSLATE[1])
                #TRANSLATE[0]+=(x*pZOOM/ZOOM - x)
                #TRANSLATE[1]+=(y*pZOOM/ZOOM - y)
                TRANSLATE[0] = x/ZOOM-xI
                TRANSLATE[1] = y/ZOOM-yI

            elif event.button == 1: #Left Click
                pass
            elif event.button == 3: #Right Click
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: #Left Release
                pass
            elif event.button == 3: #Right Release
                pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                TRANSLATE[1]+=5
            elif event.key == pygame.K_DOWN:
                TRANSLATE[1]-=5
            elif event.key == pygame.K_LEFT:
                TRANSLATE[0]+=5
            elif event.key == pygame.K_RIGHT:
                TRANSLATE[0]-=5
            elif event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
    return ZOOM,TRANSLATE,PAUSE,running
