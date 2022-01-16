import pygame
from Utilities.load_image import load_image


class Heal(pygame.sprite.Sprite):
    img = load_image('pickups/705.png')

    def __init__(self):
        super().__init__()
        self.image = self.img

    def touch(self, player, level, isCutscene, *other):
        player.hp = 100
        self.kill()
        return level, isCutscene