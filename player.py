from load_image import load_image
import pygame
from constants import *
import random
import math


class Player(pygame.sprite.Sprite):
    baseSprite = load_image("test_sprite.png")
    runSprite = load_image('test_sprite_step.png')
    runSprite2 = load_image('test_sprite_step2.png')
    jumpSprite = load_image('test_sprite_jump.png')
    fallSprite = load_image('test_sprite_fall.png')
    kickSprite = load_image('test_sprite_kick.png')

    def __init__(self, x, y, speed=5, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = self.baseSprite
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True
        self.doubleJ = False
        self.defence = 1  # потом
        self.damage = 15, 30
        self.hp = 100  # потом
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.spriteN = 0
        self.spriteRun = False
        self.isKick = 0
        self.delay = 0

    def move(self, moving_left, moving_right, world):
        # движение за этот ход
        dx = 0
        dy = 0
        if self.delay > 0:
            self.delay -= 1

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

        if moving_left or moving_right:  # спрайты во время бега
            self.spriteN += 1
            if self.spriteN >= 6:  # за сколько кадров сменяется спрайт
                self.spriteN = 0
                if self.spriteRun:
                    self.spriteRun = False
                else:
                    self.spriteRun = True
            if self.spriteRun:
                self.image = self.runSprite
            else:
                self.image = self.runSprite2
        else:
            self.image = self.baseSprite

        if self.jump and not self.in_air:  # прыжок
            self.vel_y = -12
            self.jump = False
            self.doubleJ = True
            self.in_air = True
        elif self.jump and self.doubleJ:  # двойной прыжок
            self.vel_y = -9
            self.jump = False
            self.doubleJ = False
            self.in_air = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        for tile in world:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in the y direction
            if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if dy > GRAVITY:
            # падение
            self.image = self.fallSprite
        elif dy < 0:
            # прыжок
            self.image = self.jumpSprite

        if self.isKick > 0:
            # self.image = self.colorImage
            self.image = self.kickSprite
            self.isKick -= 1

        self.rect.x += dx
        self.rect.y += dy
        scroll_x, scroll_y = 0, 0
        return scroll_x, scroll_y

    def kick(self, enemy):
        if self.delay == 0:
            self.hp -= enemy.damage * self.defence
            self.delay = 50
        if self.hp <= 0:
            self.alive = False
        # print("Герой крыс получил урон")

    def draw(self, display):
        display.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

    def equip_armor(self):
        self.baseSprite = load_image("player/armor_base.png")
        self.runSprite = load_image('player/armor_step1.png')
        self.runSprite2 = load_image('player/armor_step2.png')
        self.jumpSprite = load_image('player/armor_jump.png')
        self.fallSprite = load_image('player/armor_fall.png')
        self.kickSprite = load_image('player/armor_kick.png')

        self.defence = 0.5