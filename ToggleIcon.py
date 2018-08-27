from load_data import load_image
from settings import *

class ToggleIcon:

    def __init__(self,images,pos,size):
        self.pos = pos
        self.imgs = [pygame.transform.scale(im,size) for im in images]
        self.cur_index = 0


    def toggle(self):
        self.cur_index = (self.cur_index+1)%len(self.imgs)

    def draw(self,screen):
        screen.blit(self.imgs[self.cur_index],self.pos)

    @staticmethod
    def bridgetype():
        lower = load_image(TRAIN_ON_CONN_IMG)
        through = load_image(TRAIN_THROUGH_CONN_IMG)
        return ToggleIcon([lower,through],CONN_IMG_POS,CONN_IMG_SIZE)
