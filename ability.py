import pygame
from Utilities.load_image import load_image
from pygame.locals import *
from Utilities.constants import *


class Shield(pygame.sprite.Sprite):
    image_shield = pygame.transform.scale(
        load_image("abilities/ability111.png"), (60, 60))
    image_shield2 = pygame.transform.scale(
        load_image("abilities/ability110.png"), (40, 40))

    def __init__(self, player, *group):
        super().__init__(*group)
        self.image2 = Shield.image_shield2
        self.image = Shield.image_shield
        self.rect = self.image.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect2.x, self.rect2.y = (
            player.rect.center[0] - 15, player.rect.center[1] - 40)
        self.rect.center = player.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        self.true = True
        self.NN = 0
        self.flip = False
        self.damage = [0, 1, 2]

    def move(self, player, scroll):
        self.flip = player.flip
        self.rect.center = player.rect.center
        self.rect2.x, self.rect2.y = (
            player.rect.center[0] - 15, player.rect.y - 40)

    def draw(self, display):
        display.blit(self.image, self.rect)

    def draw2(self, display):
        display.blit(self.image2, self.rect2)

    def kick(self, mobs):
        if pygame.sprite.collide_mask(self, mobs):
            mobs.kicks(self.damage)

    def clocker(self):
        self.NN += 1
        if self.NN >= 480:
            self.kill()

    def update(self, scroll):
        pass

    def default(self):
        return True


class Sword(pygame.sprite.Sprite):
    image_sword_right = pygame.transform.scale(
        load_image("abilities/ability000.png"), (60, 60))
    image_sword_left = pygame.transform.scale(
        load_image("abilities/ability001.png"), (60, 60))

    def __init__(self, player, *group):
        super().__init__(*group)
        if player.flip is False:
            self.image = Sword.image_sword_right
            self.speed = 15
        else:
            self.image = Sword.image_sword_left
            self.speed = -15
        self.flip = player.flip

        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.mask = pygame.mask.from_surface(self.image)
        self.damage = [300, 200, 250, 350, 500, 100, 1]
        self.true = True
        self.NN = 0

    def move(self, player, scroll):
        dx = self.speed
        self.rect.x += dx

    def draw(self, display):
        display.blit(self.image, self.rect)

    def draw2(self, display):
        pass

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

    def kick(self, mobs):
        if pygame.sprite.collide_mask(self, mobs):
            mobs.kicks(self.damage)
            self.kill()

    def clocker(self):
        self.NN += 1
        if self.NN >= 30:
            self.kill()

    def default(self):
        return False


class Ability():
    def __init__(self):
        self.display = pygame.Surface(DISPLAY_SIZE)
        self.background = pygame.transform.scale(load_image(
            "abilities/background_dop.png"), DISPLAY_SIZE).convert_alpha()
        self.image00 = pygame.transform.scale(load_image(
            "abilities/ability00.png"), (256 / 2, 384 / 2)).convert_alpha()
        self.image01 = pygame.transform.scale(load_image(
            "abilities/ability01.png"), (256 / 2, 384 / 2)).convert_alpha()
        self.image10 = pygame.transform.scale(load_image(
            "abilities/ability10.png"), (256 / 2, 384 / 2)).convert_alpha()
        self.image11 = pygame.transform.scale(load_image(
            "abilities/ability11.png"), (256 / 2, 384 / 2)).convert_alpha()
        self.image1 = self.image00
        self.image2 = self.image10
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect1.x, self.rect1.y = (
            DISPLAY_SIZE[0] // 2 // 2, DISPLAY_SIZE[1] // 2 // 2)
        self.rect2.x, self.rect2.y = (
            self.rect1.x + 300, DISPLAY_SIZE[1] // 2 // 2)

    def update(self, player, ui):
        ability = 0
        if self.rect1.collidepoint(pygame.mouse.get_pos()):
            self.image1 = self.image01
            for i in pygame.event.get():
                if i.type == MOUSEBUTTONDOWN:
                    ability = Sword(player)
                    player.mana = False
                    player.mana_count = 0
                    ui.NN = 0
        else:
            self.image1 = self.image00
        if self.rect2.collidepoint(pygame.mouse.get_pos()):
            self.image2 = self.image11
            for i in pygame.event.get():
                if i.type == MOUSEBUTTONDOWN:
                    ability = Shield(player)
                    player.mana = False
                    player.mana_count = 0
                    ui.NN = 0
        else:
            self.image2 = self.image10
        return ability

    def draw(self, display):
        display.blit(self.background, (0, 0))
        display.blit(self.image1, self.rect1)
        display.blit(self.image2, self.rect2)
