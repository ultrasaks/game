import pygame
from Utilities.load_image import load_image
from Utilities.constants import *


class UI:
    def __init__(self):
        pygame.font.init()
        self.image2 = pygame.transform.scale(
            load_image("UI/mana8.png"), (50, 50)).convert_alpha()
        self.image = self.image2
        self.image3 = pygame.transform.scale(load_image(
            "UI/RUNES_WINDOW.png"), (50, 50)).convert_alpha()
        self.rect3 = self.image3.get_rect()
        self.image4 = pygame.transform.scale(
            load_image("UI/e_1.png"), (10, 10)).convert_alpha()
        self.image5 = pygame.transform.scale(
            load_image("UI/play1.png"), (60, 60)).convert_alpha()
        self.rect5 = self.image5.get_rect()
        self.true = True
        self.font_debug = pygame.font.SysFont('sprites/8514fixr.fon', 50)
        self.font = pygame.font.SysFont('8514fixr', 30)

    def draw_hp(self, player, display, color_hp=(21, 143, 26)):
        pygame.draw.rect(display, (215, 24, 44), (5, 5, 200, 20))
        pygame.draw.rect(display, color_hp, (5, 5, player.hp * 2, 20))
        if player.regen:
            text = "5 hp/s"
            font = pygame.font.SysFont("Tahoma", 20)
            textsurface = font.render(text, False, (255, 255, 255))
            display.blit(textsurface, (150, 0))

    def debug_mode(self, display, kicks, clock):
        kicks.draw(display)
        textsurface = self.font_debug.render(
            str(round(clock.get_fps())), False, (255, 255, 0))
        display.blit(textsurface, (210, 5))

    def draw_mana(self, display, player):
        if player.mana_count > 7:
            player.mana_count = 7
        text = f"{player.mana_count}/7"
        textsurface = self.font.render(text, False, (240, 240, 240))
        self.image = pygame.transform.scale(load_image(f"UI/mana{player.mana_count + 1}.png"), (50, 50)).convert_alpha()
        display.blit(
            self.image, (DISPLAY_SIZE[0] - 60, DISPLAY_SIZE[1] - DISPLAY_SIZE[1] + 15))
        display.blit(
            textsurface, (DISPLAY_SIZE[0] - 48, DISPLAY_SIZE[1] - DISPLAY_SIZE[1] + 70))

    def draw_rnes_window(self, display):
        self.rect3.x = 30
        self.rect3.y = DISPLAY_SIZE[1] - 70
        display.blit(self.image3, (self.rect3.x, self.rect3.y))

    def draw_runes(self, display, player):
        sprite = pygame.sprite.Sprite()
        if player.rune_type == "speed":
            sprite.image = pygame.transform.scale(load_image(
                "item/rune_speed.png"), (35, 35)).convert_alpha()
        if player.rune_type == "jump":
            sprite.image = pygame.transform.scale(load_image(
                "item/rune_jump.png"), (35, 35)).convert_alpha()
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self.rect3.center
        group = pygame.sprite.Group()
        group.add(sprite)
        group.draw(display)

    def draw_e(self, object, display, color=(255, 255, 255)):

        text = "взять"
        font = pygame.font.SysFont('pressstart', 18)
        textsurface = font.render(text, False, color)
        display.blit(textsurface, (object.x + 8, object.y - 17))
        display.blit(self.image4, (object.x - 8, object.y - 15))
    def draw_marvin(self, display):
        text = "Санек Marvin - облегчил твою душу!"
        font = pygame.font.SysFont('pressstart', 22)
        textsurface = font.render(text, False, (240, 240, 240))
        display.blit(
            textsurface, (DISPLAY_SIZE[0] - DISPLAY_SIZE[0] + 100, DISPLAY_SIZE[1] - 45))
    def draw_tomas(self, display):
        text = "Томас Шелби с тобой! Урон повышен!"
        font = pygame.font.SysFont('pressstart', 22)
        textsurface = font.render(text, False, (240, 240, 240))
        display.blit(
            textsurface, (DISPLAY_SIZE[0] - DISPLAY_SIZE[0] + 100, DISPLAY_SIZE[1] - 45))
    def draw_play(self, display):
        self.rect.center = (display.get_widht() // 2, display.get_height() // 2)
        display.blit(self.image5, (self.rect.x, self.rect.y))
