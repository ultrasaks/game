# initialized libs

import sys
import os
import pygame
from pygame.locals import *
from Utilities.constants import *
from Utilities.load_image import load_image
from items.runes import *
from items.poisons import Poison
from items.runes import *
import random

# slime


class Slime(pygame.sprite.Sprite):
    img_slime_jump = pygame.transform.scale(
        load_image("enemy/slime/jump.png"), (30, 30))
    img_slime_down_air = pygame.transform.scale(
        load_image("enemy/slime/down.png"), (30, 30))
    img_slime_down = pygame.transform.scale(
        load_image("enemy/slime/down_up.png"), (30, 30))
    img_slime_what = pygame.transform.scale(
        load_image("enemy/slime/what.png"), (30, 30))

    def __init__(self, x, y, speed=5, *group):
        super().__init__(*group)
        self.speed = speed
        self.vel_y = 0
        self.image = Slime.img_slime_down
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = False
        self.flip = False
        self.alive = True
        self.hp = 100
        self.flips = False
        self.damage = 15

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # зона поиска игрока
        self.x2, self.y2 = (500, 80)
        self.contact = 0  # кадры контакта с игроком

        self.NN = 61
        self.player_flip = True

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
                self.flips = True
                if self.in_air:
                    dx = -self.speed
            elif player.rect.x - 5 > self.rect.x and (x - self.x2, y - self.y2) < player.rect.center < (
                    x + self.x2, y + self.y2):
                self.flips = True
                if self.in_air:
                    dx = self.speed

            if not self.in_air:
                self.vel_y = -8
                self.in_air = True
            self.vel_y += GRAVITY_SLIME
            dy += self.vel_y
        else:
            self.NN += 1
            if self.player_flip:
                dx -= 8
            else:
                dx += 8
            self.vel_y += 1
            dy += GRAVITY_SLIME + 1

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
                self.image = self.img_slime_down_air
            elif dy < 0:
                self.image = self.img_slime_jump
        else:
            self.image = self.img_slime_what

        self.rect.x += dx
        self.rect.y += dy

    def kick(self, player, groups, groups2):
        self.NN = 0
        self.hp -= random.randint(player.damage[0], player.damage[1])
        self.player_flip = player.flip
        print(f'Слайм получил урон|{self.hp}')
        if self.hp <= 0:
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

    def kicks(self, player, groups, groups2):
        self.NN = 0
        self.hp -= random.choice(player)
        self.flip = self.flips
        print(f'Слайм получил урон|{self.hp}')
        if self.hp <= 0:
            if player.mana_count < 7:
                player.mana_count += 1
            self.kill()
            b = random.randin(0, 20)
            if b == 6:
                rune = Rune(self.rect.x, self.rect.y, 0,
                            random.choice(["speed", "jump"]))
                groups.add(rune)
            elif b in [10, 0]:
                poison = Poison(self.rect.x, self.rect.y + 8, 0,
                                random.choice(["heal", "mana", "heal", "regen", "mana", "heal", "mana", "heal", "regen", "mana", "super", "super"]))
                groups2.add(poison)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

    def draw_hp(self, display):
        pygame.draw.rect(display, (215, 24, 44),
                         (self.rect.center[0] - 8, self.rect.y - 5, 20, 5))
        pygame.draw.rect(display, (21, 143, 26),
                         (self.rect.center[0] - 8, self.rect.y - 5, self.hp * 0.2, 5))
