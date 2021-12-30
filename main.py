import pygame
import os
import sys
import random
import csv


from pygame.locals import *
from load_image import load_image
from player import Player
from camera import Camera
from constants import *
from slime import Slime
from rage_slime import RageSlime

moving_left = False
moving_right = False
scroll_data = []
scroll = [0, 0]
true_scroll = [0, 0]


img_list = []
for x in range(21):
    img = load_image(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


class World:
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

                        pass
                    elif tile == 16:
                        slime = Slime(x * 38, y * 38, 2)
                        rage_slime = RageSlime(x * 38 + 10, y * 38, 2)
                        enemies.add(slime)
                        enemies.add(rage_slime)
                        pass
                    elif tile == 20:
                        # exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        # exit_group.add(exit)
                        pass

        return player

    def draw(self, scroll_data):
        for tile in scroll_data:

            display.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))


def draw_bg():
    display.fill((105, 193, 231))


def kick():
    kickTest = pygame.sprite.Sprite()
    kickTest.image = load_image('hit.png')
    kickTest.rect = kickTest.image.get_rect()
    if player.flip:
        kickpos = -20
    else:
        kickpos = 20
    kickTest.rect.x, kickTest.rect.y = player.rect.x + kickpos, player.rect.y - 13
    kicks.add(kickTest)
    player.isKick = 7


def debug_mode():
    kicks.draw(display)
    textsurface = font_debug.render(str(round(clock.get_fps())), False, (255, 255, 0))
    display.blit(textsurface, (210, 0))


def draw_hp():
    pygame.draw.rect(display, (215, 24, 44), (0, 0, 200, 30))
    pygame.draw.rect(display, (21, 143, 26), (0, 0, player.hp * 2, 30))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Test')

    pygame.font.init()
    font_debug = pygame.font.SysFont('sprites/8514fixr.fon', 50)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0,32)
    display = pygame.Surface(DISPLAY_SIZE, 0,32)

    enemies = pygame.sprite.Group()

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
    player = world.process_data(world_data)

    players.add(player)
    camera = Camera()

    while running:
        scroll_data = camera.obstacle_list(world, scroll)
        draw_bg()
        world.draw(scroll_data)
        enemies.draw(display)
        player.draw(display)
        draw_hp()

        debug_mode()
        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, kicks, False):
                enemy.kick(player)

            if pygame.sprite.spritecollide(enemy, players, False):
                if enemy.contact == 5:
                    player.kick(enemy)
                    enemy.contact = 0
                enemy.contact += 1
            else:
                enemy.contact = 0
            enemy.update(scroll)
            enemy.move(player, scroll_data)

        kicks.empty()

        player.update(scroll)  # не поднимай вверх, оно должно быть и когда игрок не умер
        if player.alive:
            player.move(moving_left, moving_right, scroll_data)


        true_scroll[0] = (player.rect.center[0] - true_scroll[0] - A_scroll) // 15
        true_scroll[1] = (player.rect.center[1] - true_scroll[1] - B_scroll) // 15
        scroll = true_scroll.copy()
        scroll[0], scroll[1] = int(scroll[0]), int(scroll[1])

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if player.alive:
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
                    if event.key in [K_SPACE]:
                        kick_sound.play()
                        kick()
                if event.key in [K_ESCAPE]:
                    running = False
            if event.type == KEYUP:
                if event.key in [K_a]:
                    moving_left = False
                if event.key in [K_d]:
                    moving_right = False
        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
