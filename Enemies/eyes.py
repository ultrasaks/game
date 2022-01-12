

import sys
import math
import os
import pygame
from pygame.locals import *
from Utilities.constants import *
from Utilities.load_image import load_image
from items.runes import *
from items.poisons import Poison
from items.runes import *
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, player, scroll, speed=5,  *group):
        super().__init__(*group)
        # self.speed = speed
        self.vel_y = 0
        self.image = pygame.transform.scale(
            load_image("enemy/bullet/bullet.png"), (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.flip = False
        self.alive = True
        self.damage = 25

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # зона поиска игрока
        self.contact = 0  # кадры контакта с игроком

        self.NN = 61
        self.player_flip = True
        self.target_x = player.rect.center[0]
        self.target_y = player.rect.center[1]
        self.angle = math.atan2(
            (self.rect.y - scroll[1]) - self.target_y, (self.rect.x - scroll[0]) - self.target_x)
        self.x_vel = math.cos(self.angle) * 5
        self.y_vel = math.sin(self.angle) * 5

        self.NN = 0

    def move(self, player, world, tolchok=0):
        self.NN += 1
        self.rect.x += -self.x_vel
        self.rect.y += -self.y_vel
        if self.NN >= 360:
            self.kill()

    def kick(self, player, groups, groups2, f):
        self.kill()

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

    def draw_hp(self, display):
        pass


class Eye(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=0, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = pygame.transform.scale(
            load_image("enemy/eye/eye.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = False
        self.flip = False
        self.alive = True
        self.hp = 100
        self.flips = False
        self.damage = 0

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # зона поиска игрока
        self.contact = 0  # кадры контакта с игроком
        self.x2, self.y2 = (2000, 2000)
        self.NN = 61
        self.player_flip = True
        self.bullet_cont = 0
        self.bullet_group = pygame.sprite.Group()
        self.scroll = []
        self.bad_eye = None
        self.type_enemy = "eye"
    def move(self, player, world, tolchok=0):
        x, y = self.rect.center
        if player.rect.x + 5 < self.rect.x and (x - self.x2, y - self.y2) < player.rect.center < (
                x + self.x2, y + self.y2) or player.rect.x - 5 > self.rect.x and (
                x - self.x2, y - self.y2) < player.rect.center < (x + self.x2, y + self.y2):
            if self.bullet_cont <= 0:
                bullet = Bullet(self.rect.center[0], self.rect.center[1], player, self.scroll, random.choice([8, 10, 15, 5, 20]))
                self.bullet_group.add(bullet)
                self.bullet_cont = 120
            else:
                self.bullet_cont -= 1
        return self.bullet_group

    def kick(self, player, groups, groups2, f):
        self.NN = 0
        self.hp -= random.randint(player.damage[0], player.damage[1])
        self.player_flip = player.flip
        print(f'Глазику не нравится|{self.hp}')
        if self.hp <= 0:
            self.alive = False
            if f:
                if player.mana_count < 7:
                    player.mana_count += 1
            self.kill()

            b = random.randint(0, 40)
            if b == 34:
                rune = Rune(self.rect.x, self.rect.y, 0,
                            random.choice(["speed", "jump"]))
                groups.add(rune)
            elif b in [28, 2, 7]:
                poison = Poison(self.rect.x, self.rect.y + 8, 0,
                                random.choice(["heal", "mana", "heal", "regen", "mana", "heal", "mana", "heal", "regen", "mana", "super", "super"]))
                groups2.add(poison)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.scroll = scroll

    def draw_hp(self, display):
        pygame.draw.rect(display, (215, 24, 44),
                         (self.rect.center[0] - 8, self.rect.y - 5, 20, 5))
        pygame.draw.rect(display, (21, 143, 26),
                         (self.rect.center[0] - 8, self.rect.y - 5, self.hp * 0.2, 5))


class BadEye(pygame.sprite.Sprite):
    def __init__(self, x, y,player, speed=0, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = pygame.transform.scale(
            load_image("enemy/bad_eye/bad_eye.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = False
        self.flip = False
        self.alive = True
        self.hp = 100
        self.flips = False
        self.damage = 30

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # зона поиска игрока
        self.contact = 0  # кадры контакта с игроком
        self.x2, self.y2 = (1250, 1250)
        self.NN = 61
        self.player_flip = True
        self.scroll = []
        self.bad_eye = None
        self.type_enemy = "bad_eye"
        self.bullet_cont = 60
        self.bullet_cd = 60
        self.speeds = 4
        self.bullet_group = pygame.sprite.Group()
        self.target_x = player.rect.center[0]
        self.target_y = player.rect.center[1]
        self.colvo_bullet = 1

    def move(self, player, world, tolchok=0):
        x, y = self.rect.center
        self.target_x = player.rect.center[0]
        self.target_y = player.rect.center[1]
        self.angle = math.atan2(
            (self.rect.y - self.scroll[1]) - self.target_y, (self.rect.x - self.scroll[0]) - self.target_x)
        self.x_vel = math.cos(self.angle) * self.speeds
        self.y_vel = math.sin(self.angle) * self.speeds
        self.rect.x += -self.x_vel
        self.rect.y += -self.y_vel
        if player.rect.x + 5 < self.rect.x and (x - self.x2, y - self.y2) < player.rect.center < (
                x + self.x2, y + self.y2) or player.rect.x - 5 > self.rect.x and (
                x - self.x2, y - self.y2) < player.rect.center < (x + self.x2, y + self.y2):
            if self.bullet_cont <= 0:
                for i in range(self.colvo_bullet):
                    bullet = Bullet(self.rect.center[0], self.rect.center[1], player, self.scroll, random.choice([8, 10, 15, 5, 20]))
                    self.bullet_group.add(bullet)
                    self.bullet_cont = self.bullet_cd
            else:
                self.bullet_cont -= 1
        else:
            self.bullet_cont = 0
        return self.bullet_group



    def kick(self, player, groups, groups2, f):
        self.NN = 0
        self.hp -= random.randint(player.damage[0], player.damage[1])
        self.player_flip = player.flip
        self.bullet_cd -= 10
        self.speeds += 2
        self.colvo_bullet += 1
        print(f'ПЛОХОЙ ГЛАЗ ЗЛИТСЯ|{self.hp}')
        if self.hp <= 0:
            self.bad_eye = None
            if f:
                if player.mana_count < 7:
                    player.mana_count += 1
            self.kill()

            b = 34
            if b == 34:
                rune = Rune(self.rect.x, self.rect.y, 0,
                            random.choice(["speed", "jump"]))
                groups.add(rune)
            elif b == 34:
                poison = Poison(self.rect.x, self.rect.y + 8, 0,
                                random.choice(["heal", "mana", "heal", "regen", "mana", "heal", "mana", "heal", "regen", "mana", "super", "super"]))
                groups2.add(poison)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.scroll = scroll

    def draw_hp(self, display):
        pygame.draw.rect(display, (215, 24, 44),
                         (self.rect.center[0] - 8, self.rect.y - 5, 20, 5))
        pygame.draw.rect(display, (21, 143, 26),
                         (self.rect.center[0] - 8, self.rect.y - 5, self.hp * 0.2, 5))