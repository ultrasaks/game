import pygame
from items.item import Item
from Utilities.constants import *
from Utilities.load_image import load_image


class Rune(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, runes, *group):
        super().__init__(*group)
        self.type_rune = ""
        if runes == "speed":
            self.type_rune = "speed"
            self.image = pygame.transform.scale(load_image(
                "item/rune_speed.png"), (30, 30)).convert_alpha()
        elif runes == "jump":
            self.type_rune = "jump"
            self.image = pygame.transform.scale(load_image(
                "item/rune_jump.png"), (30, 30)).convert_alpha()
        else:  # ToDo: ЧТО ТЫ БЛЯТЬ СДЕЛАЛ ОНО ЖЕ ВСЁ ЛОМАЕТСЯ НА G
            self.type_rune = "jump"
            self.image = pygame.transform.scale(load_image(
                "item/rune_jump.png"), (30, 30)).convert_alpha()
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

    def proverka(self, player, display, ui):
        if player.rect.x >= self.rect.x + 50 or player.rect.x <= self.rect.x - 50:
            ui.image = pygame.transform.scale(
                load_image("UI/e_1.png"), (10, 10)).convert_alpha()
            ui.draw_e(self.rect, display, (255, 255, 255))
            player.rune_true = False
            if player.rect.x >= self.rect.x + 300 or player.rect.x <= self.rect.x - 300 and player.rect.y >= self.rect.y + 200 or player.rect.y <= self.rect.y - 200:
                self.kill()
        else:
            ui.image = pygame.transform.scale(
                load_image("UI/e_2.png"), (10, 10)).convert_alpha()
            ui.draw_e(self.rect, display, (220, 220, 220))
            player.rune_true = True
