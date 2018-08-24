
from settings import *
class UI():

    physics = None

    def __init__(self):
        pass


    def zoom(self,zoom_in = True):
        global ZOOM,TRANSLATE

        (x,y) = pygame.mouse.get_pos()
        pZOOM = ZOOM
        if zoom_in:
            ZOOM+=ZOOM_FACTOR
        else:
            ZOOM=max(ZOOM-ZOOM_FACTOR,1)

        xI = (x/pZOOM-TRANSLATE[0])
        yI = (y/pZOOM-TRANSLATE[1])
        TRANSLATE[0] = x/ZOOM-xI
        TRANSLATE[1] = y/ZOOM-yI

    def translate(self,dx,dy):
        global TRANSLATE

        TRANSLATE[0]+=dx
        TRANSLATE[1]+=dy

        TRANSLATE[0]=max(TRANSLATE[0],-0.3*SCREEN_WIDTH*(ZOOM-1))
        TRANSLATE[1]=max(TRANSLATE[1],-0.3*SCREEN_HEIGHT*(ZOOM-1))

        TRANSLATE[0]=min(TRANSLATE[0],0.5*SCREEN_WIDTH*(ZOOM-1))
        TRANSLATE[1]=min(TRANSLATE[1],0.5*SCREEN_HEIGHT*(ZOOM-1))



    def handle_events(self):
        global ZOOM,TRANSLATE,PAUSE
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                #scrolling
                if event.button == 4:
                    self.zoom(zoom_in = True)
                elif event.button == 5:
                    self.zoom(zoom_in = False)


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



    def clicked(self):
        pass

    def released(self):

        if selbestellewieclick
            self.create_point()

        if nichtselbestelle und zwei punkte:
            self.create_connection(beide_punkte)
        pass
