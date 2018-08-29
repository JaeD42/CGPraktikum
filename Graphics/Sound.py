import pygame
from Utils.load_data import load_sound
from Utils.settings import *



class Sound:

    def __init__(self):
        self.channels = [pygame.mixer.Channel(i) for i in range(5)]

        self.bg_vol = BGMUSIC_VOL
        self.train_sound_vol = TRAIN_SOUND_VOL


        for c in self.channels:
            c.set_volume(0.1)

        self.bgmusic = load_sound(BGMUSIC)
        self.bgmusic.set_volume(self.bg_vol)

        self.train_sound = load_sound(TRAIN_SOUND)
        self.train_sound.set_volume(self.train_sound_vol)

        #self.cash_sound = load_sound(CASH_SOUND)
        #self.cash_sound.set_volume(CASH_SOUND)



    def play_bg(self):
        self.channels[0].play(self.bgmusic, loops = -1)

    def mute(self):
        self.bgmusic.set_volume(0)
        self.train_sound.set_volume(0)

    def unmute(self):
        if(self.bgmusic.get_volume() == 0):
            self.bgmusic.set_volume(self.bg_vol)
        if(self.train_sound.get_volume() == 0):
            self.train_sound.set_volume(self.train_sound_vol)

    def play_train_sound(self):
        if(not self.channels[1].get_busy()):
            self.channels[1].play(self.train_sound)

    def play_cash_sound(self):
        self.channels[2].play(self.cash_sound)
