import os
import pygame
from settings import *

preloaded = {}

#load image of an object
def load_image(name, colorkey=None):
    if name in preloaded:
        return preloaded[name]
    fullname = os.path.join(DATA_DIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    preloaded[name]=image
    return image


def load_sound(name):
    fullname = os.path.join(DATA_DIR, name)
    sound = pygame.mixer.Sound(fullname)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound:', name)
        raise SystemExit
    return sound
