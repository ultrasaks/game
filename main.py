import pygame
import os
import sys
import random
import csv
from UI import UI

from pygame.locals import *

import ability
from Utilities.load_image import load_image
from player import Player
from Utilities.camera import Camera
from Utilities.constants import *
from bird import Bird

from ability import Ability
from decor import Decor
from world import World
from pickup import Pickup

moving_left = False
moving_right = False
newLevel = False

scroll_data = []
scroll = [0, 0]
true_scroll = [0, 0]
level = 1
cutscenes = {0: [[410, 'Игрок бегает на кнопки [A]|[D] и [←]|[→]'], [300, 'Прыжок совершается на [W] или [↑]']],
             1: [[300, 'У тебя в руке меч, это значит что ты можешь бить им на [SPACE] или [↓]']]}
isCutscene = False


img_list = []
decor_list = []
for x in range(20):
    img = load_image(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

for x in range(500, 504):
    img = load_image(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    decor_list.append(img)


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


def startup():
    global kicks, players, decoration_group, enemies, decoration_mobs, abilities_group, all_sprites, \
        sprite, image, decorations, pickups, world_data, world, player, camera, ui
    kicks = pygame.sprite.Group()

    decoration_group = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    decoration_mobs = pygame.sprite.Group()
    abilities_group = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    image = pygame.transform.scale(load_image("enemy/slime/jump.png"), (15, 15))
    sprite.image = image
    sprite.rect = image.get_rect()
    all_sprites.add(sprite)

    decorations = Decor()
    pickups = Pickup()

    world_data = []
    with open(f'levels/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        readerData = [row for row in reader]

        rows = len(readerData)  # создание пустого уровня
        cols = len(readerData[0])
        for row in range(rows):
            r = [-1] * cols
            world_data.append(r)

        for x, row in enumerate(readerData):
            for y, tile in enumerate(row):
                try:
                    world_data[x][y] = int(tile)
                except:
                    pass

    world = World(img_list, decor_list)
    if players:
        players.empty()
        print(player.defence, player.hp)
        player = world.process_data(world_data, decorations, enemies, pickups, [player.defence, player.hp, player.damage])
    else:
        player = world.process_data(world_data, decorations, enemies, pickups)
    for i in range(50):
        bird = Bird(random.randint(50, 2000), random.randint(-6000, 0))
        decoration_mobs.add(bird)

    players.add(player)

    camera = Camera()
    ui = UI()


if __name__ == '__main__':
    global kicks, players, decoration_group, enemies, decoration_mobs, abilities_group, all_sprites, \
        sprite, image, decorations, pickups, world_data, world, player, camera, ui
    pygame.init()
    pygame.display.set_caption('Test')
    font_cutscene = pygame.font.SysFont('Tahoma', 15)

    players = pygame.sprite.Group()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    display = pygame.Surface(DISPLAY_SIZE, 0, 32)

    kick_sound = pygame.mixer.Sound("sounds/kick.wav")
    jump_sound = pygame.mixer.Sound("sounds/jump.wav")
    jump2_sound = pygame.mixer.Sound("sounds/djump.wav")
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    vol = 0.2
    pygame.mixer.music.set_volume(vol)

    startup()

    running = True
    pygame.mouse.set_visible(False)

    pause = False
    eventer = ""

    abilityy = Ability()

    color_hp = (21, 143, 26)

    while running:
        if newLevel:
            level += 1
            startup()
            newLevel = False

        if not pause:

            a = 0
            for i in abilities_group:
                a = i.default()
            if not a:
                color_hp = (21, 143, 26)
            else:
                color_hp = (20, 30, 255)
            scroll_data = camera.obstacle_list(world, scroll, decorations, pickups)
            draw_bg()
            decoration_mobs.draw(display)
            world.draw(display, scroll_data)
            decorations.decoration_group.draw(display)

            pickups.pickups_group.draw(display)

            for i in abilities_group:
                i.draw2(display)

            enemies.draw(display)
            player.draw(display)

            abilities_group.draw(display)
            ui.draw_hp(player, display, color_hp)
            ui.draw_mana(display, player)

            ui.debug_mode(display, kicks, clock)
            for mob in decoration_mobs:
                mob.update(scroll)
                mob.move()

            player.update(scroll)
            if not isCutscene:
                for enemy in enemies:
                    if pygame.sprite.spritecollide(enemy, kicks, False):
                        enemy.kick(player)

                    if pygame.sprite.spritecollide(enemy, players, False):
                        if enemy.contact == 5:
                            if not a:
                                color_hp = (21, 143, 26)
                                player.kick(enemy)
                                enemy.contact = 0
                            else:
                                color_hp = (20, 30, 255)
                        enemy.contact += 1
                    else:
                        enemy.contact = 0
                    enemy.update(scroll)
                    enemy.move(player, scroll_data)

                if player.alive:
                    player.move(moving_left, moving_right, scroll_data)
            else:
                for enemy in enemies:
                    enemy.update(scroll)
                if cutscenes[level][0][0] > 0:
                    cutscenes[level][0][0] -= 1

                    textsurface = font_cutscene.render(cutscenes[level][0][1], False, (255, 255, 0))
                    display.blit(textsurface, (player.rect.x - len(cutscenes[level][0][1]) * 3, player.rect.y - 100))
                else:
                    isCutscene = False
                    cutscenes[level].pop(0)

            if pygame.sprite.spritecollide(player, pickups.pickups_group, False):
                for pickup in pickups.pickups_group:
                    if pygame.sprite.spritecollide(pickup, players, False):
                        newLevel, isCutscene = pickup.touch(player, newLevel, isCutscene)

            kicks.empty()

            for i in abilities_group:
                i.update(scroll)
                i.move(player, scroll)
                i.clocker()

            true_scroll[0] = (player.rect.center[0] - true_scroll[0] - A_scroll) // 15
            true_scroll[1] = (player.rect.center[1] - true_scroll[1] - B_scroll) // 15
            scroll = true_scroll.copy()
            scroll[0], scroll[1] = int(scroll[0]), int(scroll[1])




        else:
            # moving_left = False
            # moving_right = False

            draw_bg()
            decoration_mobs.draw(display)
            world.draw(display, scroll_data)
            for i in abilities_group:
                i.draw2(display)

            enemies.draw(display)
            player.draw(display)

            abilities_group.draw(display)
            ui.draw_hp(player, display, color_hp)
            ui.draw_mana(display, player)
            if eventer == "ability":
                a = abilityy.update(player, ui)
                if a == 0:
                    abilityy.draw(display)
                else:
                    abilities_group.add(a)
                    pause = False
            if pygame.mouse.get_focused():
                sprite.rect.x, sprite.rect.y = pygame.mouse.get_pos()
                all_sprites.draw(display)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if player.alive:
                    if event.key in [K_a, K_LEFT]:
                        moving_left = True
                    if event.key in [K_d, K_RIGHT]:
                        moving_right = True
                    if event.key in [K_w, K_UP] and player.alive and (
                            not player.in_air or player.doubleJ):
                        if not player.in_air:
                            jump_sound.play()
                        else:
                            jump2_sound.play()
                        player.jump = True
                    if event.key in [K_SPACE, K_DOWN]:
                        kick_sound.play()
                        kick()
                if event.key in [K_ESCAPE]:
                    running = False
                if event.key in [K_TAB]:
                    if player.mana:
                        pause = True
                        eventer = "ability"
            if event.type == KEYUP:
                if event.key in [K_a, K_LEFT]:
                    moving_left = False
                if event.key in [K_d, K_RIGHT]:
                    moving_right = False
                if event.key in [K_TAB]:
                    pause = False
                    eventer = ""

        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
