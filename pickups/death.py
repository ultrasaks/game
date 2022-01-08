import pygame
from Utilities.load_image import load_image


class Death(pygame.sprite.Sprite):
    img = load_image('tiles/16.png')

    def __init__(self):
        super().__init__()
        self.image = self.img

    def touch(self, player, level, isCutscene):
        player.hp = 0
        player.alive = False
        return level, isCutscene