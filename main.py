import pygame
import os
import sys
import random
import csv
from pygame.locals import *
from load_image import load_image
from player import Player
from enemy import Enemy
from constants import *
from slime import Slime

moving_left = False
moving_right = False
scroll_x, scroll_y = 0, 0


img_list = []
for x in range(21):
    img = load_image(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        global player
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(
                            img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Player(x * 38, y * 38, 5)
                        slime = Slime(x * 38, y * 38, 2)
                        pass
                    elif tile == 16:
                        # enemy =
                        # enemy_group.add(enemy)
                        pass
                    elif tile == 20:
                        # exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        # exit_group.add(exit)
                        pass

        return player, slime

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += scroll_x
            # tile[1][1] += scroll_y
            screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))


def draw_bg():
    screen.fill((105, 193, 231))


def kick():
    kickTest = pygame.sprite.Sprite()
    kickTest.image = load_image('hit.png')
    kickTest.rect = kickTest.image.get_rect()
    if player.flip:
        kickpos = -20
    else:
        kickpos = 20
    kickTest.rect.x, kickTest.rect.y = player.rect.x + kickpos, player.rect.y
    kicks.add(kickTest)
    player.isKick = 7


def debug_mode():
    kicks.draw(screen)
    textsurface = font_debug.render(
        str(round(clock.get_fps())), False, (255, 255, 0))
    screen.blit(textsurface, (0, 0))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Test')

    pygame.font.init()
    font_debug = pygame.font.SysFont('sprites/8514fixr.fon', 50)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    enemies = pygame.sprite.Group()
    slimes = pygame.sprite.Group()

    kick_sound = pygame.mixer.Sound("sounds/kick.wav")
    jump_sound = pygame.mixer.Sound("sounds/jump.wav")
    jump2_sound = pygame.mixer.Sound("sounds/djump.wav")
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    vol = 0.2
    pygame.mixer.music.set_volume(vol)

    running = True
    kicks = pygame.sprite.Group()
    players = pygame.sprite.Group()
    decoration_group = pygame.sprite.Group()

    world_data = []
    with open(f'levels/level1_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        readerData = [row for row in reader]

        rows = len(readerData)  # создание пустого уровня
        cols = len(readerData[0])
        for row in range(rows):
            r = [-1] * cols
            world_data.append(r)

        for x, row in enumerate(readerData):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World()
    player, slime = world.process_data(world_data)
    slimes.add(slime)
    players.add(player)

    while running:
        draw_bg()
        world.draw()
        player.draw(screen)
        debug_mode()

        for enemy in slimes:
            enemy.update(scroll_x)
            if pygame.sprite.spritecollide(enemy, kicks, False):
                enemy.kick(player, world)

            if pygame.sprite.spritecollide(enemy, players, False):
                player.kick(enemy)
            enemy.move(player, world)
        kicks.empty()
        scroll_x, scroll_y = 0, 0


        slimes.draw(screen)

        if player.alive:
            scroll_x, scroll_y = player.move(moving_left, moving_right, world)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.type == KEYDOWN:
                    if event.key in [K_a]:
                        moving_left = True
                    if event.key in [K_d]:
                        moving_right = True
                    if event.key in [K_w] and player.alive and (
                            not player.in_air or player.doubleJ):
                        if not player.in_air:
                            jump_sound.play()
                        else:
                            jump2_sound.play()
                        player.jump = True
                    if event.key in [K_ESCAPE]:
                        run = False
                    if event.key in [K_SPACE]:
                        kick_sound.play()
                        kick()
            if event.type == KEYUP:
                if event.key in [K_a]:
                    moving_left = False
                if event.key in [K_d]:
                    moving_right = False
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
