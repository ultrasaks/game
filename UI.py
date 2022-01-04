import pygame
from Utilities.load_image import load_image
from Utilities.constants import *


class UI:
    def __init__(self):
        self.image2 = pygame.transform.scale(load_image("UI/mana1.png"), (50, 50)).convert_alpha()
        self.image = self.image2
        self.true = True

        pygame.font.init()
        self.font_debug = pygame.font.SysFont('sprites/8514fixr.fon', 50)

    def draw_hp(self, player, display, color_hp=(21, 143, 26)):
        pygame.draw.rect(display, (215, 24, 44), (player.rect.center[0] - 25, player.rect.y - 10, 50, 5))
        pygame.draw.rect(display, color_hp, (player.rect.center[0] - 25, player.rect.y - 10, player.hp * 0.5, 5))

    def debug_mode(self, display, kicks, clock):
        kicks.draw(display)
        textsurface = self.font_debug.render(str(round(clock.get_fps())), False, (255, 255, 0))
        display.blit(textsurface, (10, 5))

    def draw_mana(self, display, player):
        if self.true and player.mana:
            self.image = self.image2
            display.blit(self.image, (DISPLAY_SIZE[0] - 60, DISPLAY_SIZE[1] - DISPLAY_SIZE[1] + 15))
