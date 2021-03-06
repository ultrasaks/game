import pygame
from Utilities.load_image import load_image


class Bebra(pygame.sprite.Sprite):
    img = load_image('pickups/bebra.png')

    def __init__(self):
        super().__init__()
        self.image = self.img
        self.sound = pygame.mixer.Sound("sounds/tomas.mp3")

    def touch(self, player, level, isCutscene, *other):
        player.damage[1] += 30
        player.hp = 100
        self.kill()
        self.sound.play()
        player.tomas = True
        return level, isCutscene