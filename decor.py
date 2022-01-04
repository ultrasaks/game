import pygame
from load_image import load_image


class Decor:
    def __init__(self):
        self.decoration_group = pygame.sprite.Group()

    def add_decor(self, img, x, y):
        decoration = pygame.sprite.Sprite()
        decoration.image = img
        decoration.rect = decoration.image.get_rect()
        decoration.rect.x, decoration.rect.y = x, y
        self.decoration_group.add(decoration)