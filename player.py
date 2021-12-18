from load_image import load_image
import pygame
from constants import *
import random


class Player(pygame.sprite.Sprite):
    img = load_image("test_sprite.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.speed = 5
        self.vel_y = 0
        self.image = self.img
        self.rect = self.image.get_rect()
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True
        self.defence = 0  # потом
        self.damage = 0  # потом
        self.hp = 100  # потом

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            if self.in_air:
                dx -= 1
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            if self.in_air:
                dx += 1
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
