import pygame
from Utilities.load_image import load_image


class Exit(pygame.sprite.Sprite):
    img = load_image('pickups/701.png')

    def __init__(self):
        super().__init__()
        self.image = self.img

    def touch(self, player, level, isCutscene):
        player.hp = 0
        return level, isCutscene