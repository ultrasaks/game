import pygame

from player import Player
from Enemies.slime import Slime
from Enemies.rage_slime import RageSlime
from Utilities.constants import *

from Pickups.armor import Armor


class World:
    def __init__(self, img_list):
        self.obstacle_list = []
        self.img_list = img_list

    def process_data(self, data, decorations, enemies, pickups):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    if tile < 700:
                        img = self.img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect)

                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 11 <= tile <= 14:
                        decorations.add_decor(img, x * TILE_SIZE, y * TILE_SIZE)
                    elif tile == 15:
                        player = Player(x * 38, y * 38, 5)
                        pass
                    elif tile == 800:
                        slime = Slime(x * 38, y * 38, 2)
                        enemies.add(slime)
                        pass
                    elif tile == 801:
                        rage_slime = RageSlime(x * 38 + 10, y * 38, 2)
                        enemies.add(rage_slime)
                    elif tile == 700:
                        arm = Armor()
                        pickups.add_pickup(arm, x * 38 + 10, y * 38)
                        pass

        return player

    def draw(self, display, scroll_data):
        for tile in scroll_data:
            display.blit(tile[0], tile[1])