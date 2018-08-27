import pygame
from load_data import load_sound
from settings import *

class Sound:

    def __init__(self):
        self.channel1 = pygame.mixer.Channel(0) # argument must be int
        self.channel2 = pygame.mixer.Channel(1)
        self.channel1.set_volume(0.1)
        self.channel2.set_volume(0.1)

        self.bgmusic = load_sound(BGMUSIC)
        self.bgmusic.set_volume(BGMUSIC_VOL)

        self.train_sound = load_sound(TRAIN_SOUND)
        self.train_sound.set_volume(TRAIN_SOUND_VOL)




    def play_bg(self):
        self.channel1.play(self.bgmusic, loops = -1)


    def play_train_sound(self):
        if(not self.channel2.get_busy()):
            self.channel2.play(self.train_sound)
