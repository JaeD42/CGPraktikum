
from settings import *
from Physics import Physics
from train import Train
class UI():

    physics = None
    SCROLL_UP = 4
    SCROLL_DOWN = 5
    LEFT_MOUSE = 1
    RIGHT_MOUSE = 3
    grid_mode = False

    def __init__(self, bridge_creator):
        self.BC = bridge_creator
        self.first_pos = (0,0)
        self.first_selected = False
        self.first_is_point = False
        self.second_pos = (0,0)
        self.build_mode = True


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
        global ZOOM,TRANSLATE,PAUSE, RUNNING

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                #scrolling
                if event.button == self.SCROLL_UP:
                    self.zoom(zoom_in = True)
                elif event.button == self.SCROLL_DOWN:
                    self.zoom(zoom_in = False)


                elif event.button == self.LEFT_MOUSE: #Left Click
                    self.left_down()
                elif event.button == self.RIGHT_MOUSE: #Right Click
                    self.right_down()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == self.LEFT_MOUSE: #Left Release
                    self.left_up()
                elif event.button == self.RIGHT_MOUSE: #Right Release
                    self.right_up()



            elif event.type == pygame.KEYDOWN:
                dx = 0
                dy = 0
                if event.key == pygame.K_UP:
                    TRANSLATE[1]+=5
                if event.key == pygame.K_DOWN:
                    TRANSLATE[1]-=5
                if event.key == pygame.K_LEFT:
                    TRANSLATE[0]+=5
                if event.key == pygame.K_RIGHT:
                    TRANSLATE[0]-=5
                if event.key == pygame.K_g:
                    #show grid
                    self.grid_mode = not self.grid_mode
                if event.key == pygame.K_b:
                    #show bridge connections instead of images
                    if(self.build_mode):
                        self.BC.change_bridge_mode()
                    else:
                        self.physics.change_bridge_mode()
                if event.key == pygame.K_SPACE:
                    PAUSE = not PAUSE
                    self.build_mode = False
                    self.create_physics()
        return RUNNING



    def left_down(self):
        pos = pygame.mouse.get_pos()
        self.selected(pos)

    def left_up(self):
        pos = pygame.mouse.get_pos()
        self.selected_second(pos)

    def right_down(self):
        pass

    def right_up(self):
        pass

    def selected(self,pos):
        p = self.BC.check_which_point_image_coords(pos)
        self.first_selected = True
        self.first_pos = pos[:]
        if p!=None:
            self.first_is_point = True
        else:
            self.first_is_point = False



    def selected_second(self,pos):
        if self.BC.get_grid_pos(pos)==self.BC.get_grid_pos(self.first_pos):
            if self.first_is_point:
                self.BC.check_which_point_image_coords(pos).change_moveable()
            else:
                if self.build_mode:
                    self.BC.add_point(pos)
        else:
            if self.first_is_point:
                if self.build_mode:
                    self.BC.add_connection(self.first_pos,pos)
            else:
                pass
        self.first_selected = False
        self.first_is_point = False

    def create_physics(self):
        self.build_mode = False
        points = self.BC.points
        connections = self.BC.connections
        bg = self.BC.bg
        self.physics = Physics(connections,points,Train.get_standard_train(),bg)

    def step(self,dt, screen):
        r = self.handle_events()
        if self.build_mode:
            self.BC.draw(screen,ZOOM,TRANSLATE)
        else:
            self.physics.update_physics(dt)
            self.physics.move(dt)
            self.physics.draw(screen,ZOOM,TRANSLATE)
        if(self.grid_mode):
            self.show_grid(screen)
        return r

    def show_grid(self, screen):
        grid_line = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        for pos in self.BC.get_grid_intersections():
            offset = 5
            pygame.draw.line(grid_line, (0,0,0, 100), (pos[0]-offset, pos[1]), (pos[0]+offset, pos[1]))
            pygame.draw.line(grid_line, (0,0,0, 100), (pos[0], pos[1]-offset), (pos[0],pos[1]+offset))
        screen.blit(grid_line, (0,0))
