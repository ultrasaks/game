import pygame

from player import Player
from Enemies.slime import Slime
from Enemies.rage_slime import RageSlime
from Enemies.eyes import Eye
from Enemies.boss import Boss
from Enemies.eyes import *
from Utilities.constants import *

from pickups.armor import Armor
from pickups.exit import Exit
from pickups.cutscene import Cutscene
from pickups.death import Death
from pickups.bebra import Bebra
from pickups.heal import Heal


class World:
    def __init__(self, img_list, decor_list):
        self.obstacle_list = []
        self.img_list = img_list
        self.decor_list = decor_list

    def process_data(self, data, decorations, enemies, pickups, inventory=None):
        boss = None
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    if tile < 700:
                        if 500 <= tile < 700:
                            img = self.decor_list[tile - 500]
                        else:
                            img = self.img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect)
                    if 0 <= tile < 500 and tile != 15:
                        self.obstacle_list.append(tile_data)
                    elif 500 <= tile < 700:
                        decorations.add_decor(img, x * TILE_SIZE, y * TILE_SIZE)
                    elif tile == 15:
                        player = Player(x * 38, y * 38, 5, inventory)
                        pass

                    elif tile == 700:
                        arm = Armor()
                        pickups.add_pickup(arm, x * 38, y * 38)
                    elif tile == 701:
                        pickups.add_pickup(Exit(), x * 38, y * 38)
                    elif tile == 702:
                        pickups.add_pickup(Cutscene(), x * 38, y * 38)
                    elif tile == 703:
                        pickups.add_pickup(Death(), x * 38, y * 38)
                    elif tile == 704:
                        pickups.add_pickup(Bebra(), x * 38, y * 38)
                    elif tile == 705:
                        pickups.add_pickup(Heal(), x * 38, y * 38)

                    elif tile == 800:
                        slime = Slime(x * 38, y * 38, 2)
                        enemies.add(slime)
                    elif tile == 801:
                        slime = RageSlime(x * 38, y * 38, 2)
                        enemies.add(slime)
                    elif tile == 802:
                        boss = Boss(x * 38 + 10, y * 38, 2)
                    elif tile == 803:
                        eye = Eye(x * 38 + 10, y * 38, 2)
                        enemies.add(eye)
        return player, boss

    def draw(self, display, scroll_data):
        for tile in scroll_data:
            display.blit(tile[0], tile[1])