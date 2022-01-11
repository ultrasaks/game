# initialized libs

import sys
import os
import pygame
from pygame.locals import *
from Utilities.constants import *
from Utilities.load_image import load_image
import random



class Boss(pygame.sprite.Sprite):
    img_base = load_image("boss/base.png")
    img_step1 = load_image('boss/step1.png')
    img_step2 = load_image('boss/step2.png')

    def __init__(self, x, y, speed=20, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = self.img_base
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = False
        self.flip = False
        self.alive = True
        self.hp = 750
        self.damage = 30
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.NN = 15
        self.player_flip = True
        self.contact = 0
        self.step = 0

    def move(self, player, world, tolchok=0):
        dx = 0
        dy = 0
        if self.NN >= 15:
            # if tolchok == 1:
            #     dx += 150
            # elif tolchok == 2:
            #     dx -= 150

            if player.rect.x < self.rect.center[0]:
                if self.in_air:
                    dx -= 2
                dx = -self.speed
                self.flip = False

            elif player.rect.x > self.rect.center[0]:
                if self.in_air:
                    dx += 2
                dx = self.speed
                self.flip = True
            if player.rect.y < self.rect.y and not self.in_air:
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
            if dx < 0:
                a = dx - 15
            else:
                a = dx + 15
            if tile[1].colliderect(self.rect.x + a, self.rect.y, self.width, self.height):
                dy = -15
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
            self.step += 1
            if self.step <= -7:
                self.image = self.img_base
            elif self.step <= 0:
                self.image = self.img_step2
            elif self.step <= 7:
                self.image = self.img_base
            elif self.step <= 14:
                self.image = self.img_step1
            else:
                self.step = -14

            # if dy > GRAVITY_SLIME:
            #     self.image = self.img_base
            # elif dy < 0:
            #     # self.image = self.img_slime_jump
        else:
            # self.image = self.img_slime_what
            pass

        self.rect.x += dx
        self.rect.y += dy

    def kick(self, player):
        self.NN = 0
        self.hp -= random.randint(player.damage[0], player.damage[1])
        self.player_flip = player.flip
        print(f'кот получил урон|{self.hp}')
        if self.hp <= 0:
            player.mana_count += 3
            self.kill()

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

    def draw(self, display):
        display.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)