import pygame
import sys
import os
from pygame.locals import *
from Utilities.constants import *
from Utilities.load_image import load_image
import random


class Item(pygame.sprite.Sprite):

    def __init__(self, x, y,speed, *group):
        super().__init__(*group)
        self.image = load_image("item/base.png")
        self.rect = self.image.get_rect()


