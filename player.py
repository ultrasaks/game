from load_image import load_image
import pygame
from constants import *
import random


class Player(pygame.sprite.Sprite):
    img = load_image("test_sprite.png")

    def __init__(self, x, y, speed=5, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True
        self.doubleJ = False
        self.defence = 0  # потом
        self.damage = 0  # потом
        self.hp = 100  # потом
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right, world):
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
            self.doubleJ = True
            self.in_air = True
        elif self.jump and self.doubleJ:
            self.vel_y = -9
            self.jump = False
            self.doubleJ = False
            self.in_air = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        for tile in world.obstacle_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
