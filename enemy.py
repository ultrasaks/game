import pygame
from load_image import load_image
import random


class Enemy(pygame.sprite.Sprite):
    img = load_image('wtf.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hp = 100
        self.defence = 0  # потом
        self.damage = 0  # потом
фв