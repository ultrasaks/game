import pygame
from Utilities.constants import *
from Utilities.load_image import load_image


class Poison(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, poison, *group):
        super().__init__(*group)
        self.type_poison = ""
        if poison == "heal":
            self.type_poison = "heal"
            self.image = pygame.transform.scale(load_image(
                "item/poison_heal.png"), (15, 18)).convert_alpha()
        elif poison == "regen":
            self.type_poison = "regen"
            self.image = pygame.transform.scale(load_image(
                "item/poison_regen.png"), (5, 15)).convert_alpha()
        elif poison == "mana":
            self.type_poison = "mana"
            self.image = pygame.transform.scale(load_image(
                "item/poison_mana.png"), (15, 18)).convert_alpha()
        elif poison == "super":
            self.type_poison = "super"
            self.image = pygame.transform.scale(load_image(
                "item/poison_super.png"), (10, 15)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = speed
        self.in_air = False
        self.g = False
        self.vel_y = 0

    def move(self, world):
        dx = 0
        dy = 0
        if self.in_air and not self.g:
            dx += self.speed
        if not self.in_air and not self.g:
            self.vel_y = -4
            self.in_air = True
        self.vel_y += GRAVITY
        dy += self.vel_y
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
                    self.g = True
                    dx = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

    def poison_baf(self, player):
        if self.type_poison == "heal":
            if player.hp >= 75:
                player.hp = 100
            else:
                player.hp += 25
        elif self.type_poison == "mana":
            if player.mana_count < 7:
                player.mana_count += 1
        elif self.type_poison == "regen":
            player.regen = True
        elif self.type_poison == "super":
            if player.mana_count < 7:
                player.mana_count += 1
            if player.hp >= 75:
                player.hp = 100
            else:
                player.hp += 25

        self.kill()
