
from settings import *
from Physics import Physics
from train import Train
from ToggleIcon import ToggleIcon
from BridgeCreator import Bridge


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
        self.bridge_type_icon = ToggleIcon.bridgetype()
        self.music_type_icon = ToggleIcon.musictype()
        self.music_is_on = True
        self.conn_is_floor = True

        self.initial_bridge = None


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
                if event.key == pygame.K_s:
                    if(pygame.key.get_pressed()[pygame.K_LCTRL]):
                        if(self.build_mode):
                            self.BC.save_bridge()
                        else:
                            self.initial_bridge.save_bridge()
                if event.key == pygame.K_l:
                    if(pygame.key.get_pressed()[pygame.K_LCTRL]):
                        self.BC.load_bridge()
                if event.key == pygame.K_TAB:
                    self.toggle_conn_type()
                if event.key == pygame.K_SPACE:
                    if(self.initial_bridge):
                        PAUSE = not PAUSE
                    else:
                        self.build_mode = False
                        self.create_physics()
                if event.key == pygame.K_z and pygame.key.get_pressed()[pygame.K_LCTRL]:
                    self.build_mode = True
                    PAUSE = True
                    self.BC.load_bridge(self.initial_bridge)
                    self.initial_bridge = None


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
        if(self.is_on_music_icon(pos)):
            self.toggle_music()
        else:
            p = self.BC.check_which_point_image_coords(pos)
            self.first_selected = True
            self.first_pos = pos[:]
            if p!=None:
                self.first_is_point = True
            else:
                self.first_is_point = False



    def is_on_music_icon(self, mouse_pos):
        img = self.music_type_icon.imgs[0]
        size = (img.get_width(), img.get_height())
        pos = self.music_type_icon.pos
        if(mouse_pos[0]< pos[0]+size[0] and mouse_pos[0]> pos[0] and mouse_pos[1]< pos[1] + size[1] and mouse_pos[1]> pos[1]):
            return True
        return False

    def toggle_music(self):
        self.music_is_on = not self.music_is_on
        self.music_type_icon.toggle()


    def toggle_conn_type(self):
        self.conn_is_floor = not self.conn_is_floor
        self.bridge_type_icon.toggle()

    def selected_second(self,pos):
        if self.BC.get_grid_pos(pos)==self.BC.get_grid_pos(self.first_pos):
            if self.first_is_point:
                if(pygame.key.get_pressed()[pygame.K_LCTRL]):
                    self.BC.delete_point(pos)
                else:
                    self.BC.change_point_moveable(pos)
            else:
                if self.build_mode:
                    self.BC.add_point(pos)
        else:
            if self.first_is_point:
                if self.build_mode:
                    if(self.BC.check_if_con_exists(self.first_pos,pos)):
                        self.BC.delete_connection(self.first_pos,pos)
                    else:
                        self.BC.add_connection(self.first_pos,pos,is_floor=self.conn_is_floor)
            else:
                pass
        self.first_selected = False
        self.first_is_point = False

    def create_physics(self):
        self.build_mode = False
        points = self.BC.points
        connections = self.BC.connections
        self.initial_bridge = Bridge(points, connections)
        bg = self.BC.bg
        self.physics = Physics(connections,points,Train.get_standard_train(),bg)


    def step(self,dt, screen):
        r = self.handle_events()

        if self.build_mode:
            self.BC.draw(screen,ZOOM,TRANSLATE)
            if(self.first_selected):
                (x,y) = pygame.mouse.get_pos()
                pygame.draw.line(screen,(255,255,255),self.first_pos,(x,y),5)
            if(self.grid_mode):
                self.BC.show_grid(screen)
            self.bridge_type_icon.draw(screen)

        else:
            self.physics.update_physics(dt)
            self.physics.move(dt)
            self.physics.draw(screen,ZOOM,TRANSLATE)

        self.music_type_icon.draw(screen)


        return r
