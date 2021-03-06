from Utilities.load_image import load_image
import pygame
from Utilities.constants import *
from particles import *
import random
import math


class Player(pygame.sprite.Sprite):
    baseSprite = load_image("player/base.png")
    runSprite = load_image('player/step.png')
    runSprite2 = load_image('player/step2.png')
    jumpSprite = load_image('player/jump.png')
    fallSprite = load_image('player/fall.png')
    kickSprite = load_image('player/kick.png')

    def __init__(self, x, y, speed=5, inventory=None, *group):
        super().__init__(*group)
        self.speed = speed
        self.speed_2 = speed
        self.vel_y = 0
        self.image = self.baseSprite
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True
        self.doubleJ = False

        self.defence = 1
        self.defence_dop = 1
        self.damage = [15, 30]
        self.mana = True
        self.mana_count = 7
        self.mana_respawn = 0
        self.rune_true = False
        self.rune = False
        self.rune_type = ""
        self.regen = False
        self.regen_count = 0

        self.hp = 100
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.spriteN = 0
        self.spriteRun = False
        self.isKick = 0
        self.delay = 0

        self.marvin = False
        self.tomas = False
        self.runn = 0
        if inventory is None:
            self.inventory = [0, 100, [15, 30]]
        else:
            if inventory[0] < 1:
                self.equip_armor()
            self.hp = inventory[1]
            self.damage = inventory[2]

    def move(self, moving_left, moving_right, world, partickles_group):
        # движение за этот ход
        sprite_cadr = 6
        dx = 0
        dy = 0
        if self.rune_type == "speed":
            self.speed = 10
            sprite_cadr = 3
        if self.delay > 0:
            self.delay -= 1

        if moving_left:
            dx = -self.speed
            if self.in_air:
                dx -= 1
            else:
                if self.runn <= 0:
                    self.runn = 7
                    partickles_group.add(DustRun(self.rect, self.flip, 0.05, random.randint(2, 3)))

            self.flip = True
            self.direction = -1

        if moving_right:
            dx = self.speed
            if self.in_air:
                dx += 1
            else:
                if self.runn <= 0:
                    self.runn = 7
                    partickles_group.add(DustRun(self.rect, self.flip, 0.05, random.randint(2, 3)))
            self.flip = False
            self.direction = 1

        if moving_left or moving_right:  # спрайты во время бега
            self.runn -= 1
            self.spriteN += 1
            if self.spriteN >= sprite_cadr:  # за сколько кадров сменяется спрайт
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
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    if self.in_air:
                        for i in range(20):
                            speed = random.choice([0.3, 0.5, 0.2, 1])
                            px = random.randint(1, 4)
                            partickles_group.add(DustDown(self.rect, speed, px))
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
            self.hp -= enemy.damage * self.defence * self.defence_dop
            self.delay = 50
        if self.hp <= 0:
            self.alive = False
        # print("Герой крыс получил урон")

    def draw(self, display):
        display.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        self.mana_respawn += 1
        if self.mana_respawn >= 500:
            if self.mana_count < 7:
                self.mana_count += 1
            self.mana_respawn = 0
        if self.regen:
            self.regen_count += 1
            if self.regen_count % 60 == 0:
                if self.hp >= 95:
                    self.hp = 100
                else:
                    self.hp += 5
                if self.regen_count >= 360:
                    self.regen = False
                    self.regen_count = 0

    def equip_armor(self):
        self.baseSprite = load_image("player/armor_base.png")
        self.runSprite = load_image('player/armor_step1.png')
        self.runSprite2 = load_image('player/armor_step2.png')
        self.jumpSprite = load_image('player/armor_jump.png')
        self.fallSprite = load_image('player/armor_fall.png')
        self.kickSprite = load_image('player/armor_kick.png')

        self.defence = 0.5
