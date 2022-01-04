import pygame
import random
from Utilities.load_image import load_image


class Bird(pygame.sprite.Sprite):
    img_0 = load_image("decor_mobs/bird/bird0.png")
    img_1 = load_image("decor_mobs/bird/bird1.png")

    def __init__(self, y, x, speed=6, *group):
        super().__init__(*group)
        self.speed = speed
        self.image = Bird.img_0
        self.rect = self.image.get_rect()
        self.NN = 0
        self.anim = True
        self.rect.y = y
        self.rect.x = x

    def move(self):
        self.NN += 1
        dx = 0
        if self.NN % 7 == 0:
            if self.anim:
                self.anim = False
                self.image = Bird.img_1
            else:
                self.anim = True
                self.image = Bird.img_0

        dx += self.speed

        self.rect.x += dx
        if self.rect.x > 3000:
            self.rect.x = random.randint(-6000, 0)
            self.rect.y = random.randint(20, 2000)

    def update(self, scroll):
        self.rect.x -= scroll[0] * 0.7
        self.rect.y -= scroll[1] * 0.7

    def draw(self, display):
        display.blit(self.image, self.rect)
