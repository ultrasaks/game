# initialized libs

import sys
import os
import pygame
from pygame.locals import *
from constants import *
from load_image import load_image
import random

# slime


class RageSlime(pygame.sprite.Sprite):
    img_slime_jump = pygame.transform.scale(
        load_image("enemy/slime_rage/jump.png"), (35, 35))
    img_slime_down_air = pygame.transform.scale(
        load_image("enemy/slime_rage/down.png"), (35, 35))
    img_slime_down = pygame.transform.scale(
        load_image("enemy/slime_rage/down_up.png"), (35, 35))

    img_slime_what = pygame.transform.scale(
        load_image("enemy/slime_rage/what.png"), (35, 35))

    def __init__(self, x, y, speed=5, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = RageSlime.img_slime_down
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = False
        self.flip = False
        self.alive = True
        self.hp = 150
        self.damage = 20
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # зона поиска игрока
        self.x2, self.y2 = (500, 80)

        self.NN = 61
        self.player_flip = True
        self.contact = 0

    def move(self, player, world, tolchok=0):
        dx = 0
        dy = 0
        if self.NN >= 15:
            if tolchok == 1:
                dx += 150
            elif tolchok == 2:
                dx -= 150
            # корды которые определяют радиус
            x, y = self.rect.center

            if player.rect.x + 5 < self.rect.x and (x - self.x2, y - self.y2) < player.rect.center < (
                    x + self.x2, y + self.y2):
                if self.in_air:
                    dx = -self.speed
            elif player.rect.x - 5 > self.rect.x and (x - self.x2, y - self.y2) < player.rect.center < (
                    x + self.x2, y + self.y2):
                if self.in_air:
                    dx = self.speed

            if not self.in_air:
                self.vel_y = -9
                self.in_air = True
            self.vel_y += GRAVITY_SLIME
            dy += self.vel_y
        else:
            self.NN += 1
            if self.player_flip:
                dx -= 8
            else:
                dx += 8
            self.vel_y += 1.5
            dy += GRAVITY_SLIME + 1.5

        for tile in world:
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
        if self.NN >= 15:
            if dy > GRAVITY_SLIME:
                self.image = RageSlime.img_slime_down_air
            elif dy < 0:
                self.image = RageSlime.img_slime_jump
        else:
            self.image = RageSlime.img_slime_what

        self.rect.x += dx
        self.rect.y += dy

    def kick(self, player):
        self.NN = 0
        self.hp -= random.randint(player.damage[0], player.damage[1])
        self.player_flip = player.flip
        print(f'Слайм получил урон|{self.hp}')
        if self.hp <= 0:
            player.mana_count += 3
            self.kill()
    def kicks(self, player):
        self.NN = 0
        self.hp -= random.choice(player)
        self.flip = False
        print(f'Слайм получил урон|{self.hp}')
        if self.hp <= 0:

            self.kill()

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
