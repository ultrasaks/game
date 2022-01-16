import pygame
from Utilities.load_image import load_image
from Utilities.constants import *
import random


class DustDown(pygame.sprite.Sprite):
    def __init__(self, rect, speed, px , *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("partickles/dust.png"), (px, px))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([rect.center[0] - 8, rect.center[0] + 8])
        if self.rect.x < rect.center[0]:
            self.speed = -speed
        else:
            self.speed = speed
        self.rect.y = rect.bottom - random.randint(1, 3)
        self.xx = 0
    def move(self):
        self.xx += 1
        if self.xx  % 2 == 0:
            self.rect.y -= 1.5

        self.rect.x += self.speed

        if self.xx >= 23:
            self.kill()

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]


class DustRun(pygame.sprite.Sprite):
    def __init__(self, rect,flip, speed, px , *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("partickles/dust.png"), (px, px))
        self.rect = self.image.get_rect()
        self.flip = flip
        if flip is False:
            self.speed = -speed
            self.rect.x = rect.left + 13
        else:
            self.speed = speed
            self.rect.x = rect.right - 13
        self.rect.y = rect.bottom - 1
        self.xx = 0

    def move(self):
        self.xx += 1
        self.rect.x += self.speed
        self.rect.y -= 0.06
        if self.xx >= 8:
            self.kill()

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

class DustBullet(pygame.sprite.Sprite):
    def __init__(self, rect, speed, px , *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("partickles/bullet_dust.png"), (px, px))
        self.rect = self.image.get_rect()
        self.speed = random.choice([-speed, speed])
        self.rect.x = rect.center[0]
        self.rect.y = rect.center[1]

        self.xx = 0

    def move(self):
        self.xx += 1
        self.rect.x += self.speed * 2
        if self.xx <= 9:
            self.rect.y -= 1.5
        else:
            self.rect.y += 2 * GRAVITY

        if self.xx >= 30:
            self.kill()

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]



