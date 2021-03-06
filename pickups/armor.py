import pygame
from Utilities.load_image import load_image


class Armor(pygame.sprite.Sprite):
    img = load_image('pickups/700.png')

    def __init__(self):
        super().__init__()
        self.image = self.img

    def touch(self, player, level, isCutscene):
        player.equip_armor()
        self.kill()
        return level, isCutscene