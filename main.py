import pygame
import time
import os
import sys
import random
import csv
from UI import UI
from ast import literal_eval

from pygame.locals import *

import ability
from player import Player
from Utilities.camera import Camera
from Utilities.constants import *
from items.runes import *
from Enemies.eyes import *
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
# mountains_back_img = pygame.transform.scale(load_image("background/back_mount.png"), (A_scroll * 3, B_scroll * 3))
mountains_img = pygame.transform.scale(load_image("background/mount.png"), (A_scroll * 3, B_scroll * 3))
# mountains_back = [[0 - mountains_back_img.get_width(), 0], [0, 0], [mountains_back_img.get_width(), 0]]
mountains = [[0 - mountains_img.get_width(), 0], [0, 0], [mountains_img.get_width(), 0]]
background_1 = pygame.transform.scale(load_image("background/sky.png"), DISPLAY_SIZE)
mountains_parralax = (0.2, 0.15)
dungeon_background = load_image("background/test.png")
dungeon_parralax = 0.6

marvin_count = 0
tomas_count = 0

fps_show = False
rune, mana = ("", "")


old_Inventory = None

level = 2
cutscenes = {0: [[410, 'Игрок бегает на кнопки [A]|[D] и [←]|[→]'], [300, 'Прыжок совершается на [W] или [↑]']],
             1: [[300, 'У тебя в руке меч, это значит что ты можешь бить им на [SPACE] или [↓]']],
             2: [[0, '']], 3: [[0, '']], 4: [[0, '']], 5: [[0, '']], 6: [[0, '']]}

isCutscene = False


img_list = []
decor_list = []
for x in range(20):
    img = load_image(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

for x in range(500, 505):
    img = load_image(f'tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    decor_list.append(img)


def draw_bg():
    global level, mountains_back_img, mountains, mountains_back, mountains_img, background_1, mountains_parralax, \
        dungeon_parralax, dungeon, dungeon_background
    if level <= 7:
        display.fill((0, 191, 255))
        if not pause:
            mountains[0][0] -= scroll[0] * mountains_parralax[1]
            mountains[1][0] -= scroll[0] * mountains_parralax[1]
            mountains[2][0] -= scroll[0] * mountains_parralax[1]

        for i in mountains:
            display.blit(mountains_img, (i[0], i[1]))
        decoration_mobs.draw(display)
    else:
        display.blit(dungeon_background, (dungeon[0], dungeon[1]))
        if not pause:
            dungeon[0] -= scroll[0] * dungeon_parralax
            dungeon[1] -= scroll[1] * dungeon_parralax
    print(dungeon)


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
        sprite, image, decorations, pickups, world_data, world, player, camera, ui, old_Inventory, cur_cutscene, \
        boss, bosses, mountains_back_img, mountains, mountains_back, mountains_img, background_1, \
        mountains_parralax, Rrune, Rmana, dungeon
    kicks = pygame.sprite.Group()
    boss = None
    decoration_group = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    decoration_mobs = pygame.sprite.Group()
    abilities_group = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    dungeon = [-300, -300]

    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    image = pygame.transform.scale(
        load_image("enemy/slime/jump.png"), (15, 15))
    sprite.image = image
    sprite.rect = image.get_rect()
    all_sprites.add(sprite)

    decorations = Decor()
    pickups = Pickup()
    # mountains_back = [[0 - mountains_back_img.get_width(), 0], [0, 0], [mountains_back_img.get_width(), 0]]
    mountains = [[0 - mountains_img.get_width(), 0], [0, 0], [mountains_img.get_width(), 0]]

    world_data = []
    if level <= 8:
        pygame.mixer.music.load("sounds/musicm.mp3")
    else:
        pygame.mixer.music.load("sounds/musicd.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    vol = 0.3
    pygame.mixer.music.set_volume(vol)
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
        if player.hp > 0:
            old_Inventory = [player.defence, player.hp, player.damage]
            Rrune = [player.rune, player.rune_type, player.rune_true]
            Rmana = [player.mana, player.mana_count, player.mana_respawn]
        players.empty()
        player, boss = world.process_data(world_data, decorations, enemies, pickups, old_Inventory)
        player.rune, player.rune_type, player.rune_true = Rrune
        player.mana, player.mana_count, player.mana_respawn = Rmana
    elif old_Inventory:
        players.empty()
        player, boss = world.process_data(world_data, decorations, enemies, pickups, old_Inventory)
        player.rune, player.rune_type, player.rune_true = Rrune
        player.mana, player.mana_count, player.mana_respawn = Rmana
    else:
        player, boss = world.process_data(world_data, decorations, enemies, pickups)
    old_Inventory = [player.defence, player.hp, player.damage]
    for i in range(50):
        bird = Bird(random.randint(50, 2000), random.randint(-6000, 0))
        decoration_mobs.add(bird)
    players.add(player)
    camera = Camera()
    ui = UI()
    cur_cutscene = 0

    if boss is not None:
        bosses.add(boss)


def save_game(a=False):
    with open('savefile.json', 'wb') as savefile:
        if a:
            savefile.write(str.encode(str({'level': 0, 'inventory': [1, 100, [15, 30]],
                                           'runes': [False, '', False], 'mana': [True, 7, 374]})))
        else:
            savefile.write(str.encode(str({'level': level, 'inventory': old_Inventory,
                                       'runes': [player.rune, player.rune_type, player.rune_true],
                                       'mana': [player.mana, player.mana_count, player.mana_respawn]})))


def open_save():
    global level, old_Inventory, Rrune, Rmana
    if os.path.exists('savefile.json'):
        with open('savefile.json', 'rb') as savefile:
            data = literal_eval(savefile.read().decode())
            level = data['level']
            old_Inventory = data['inventory']
            Rrune = data["runes"]
            Rmana = data["mana"]
def menu(display, screen):

    pygame.init()
    pygame.mixer.music.load("sounds/music.wav")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
    vol = 0.2
    pygame.mixer.music.set_volume(vol)

    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    image = pygame.transform.scale(
        load_image("enemy/slime/jump.png"), (15, 15))
    sprite.image = image
    sprite.rect = image.get_rect()
    all_sprites.add(sprite)
    value = ""
    running = True

    back = pygame.transform.scale(load_image("UI/menu_back.png"), DISPLAY_SIZE)

    play1 = pygame.transform.scale(load_image("UI/play1.png"), (90, 90))
    play2 = pygame.transform.scale(load_image("UI/play2.png"), (95, 95))
    play_rect = play1.get_rect()
    play_rect.center = (back.get_width() // 2, back.get_height() // 2)
    exit1 = pygame.transform.scale(load_image("UI/exit1.png"), (80, 80))
    exit2 = pygame.transform.scale(load_image("UI/exit2.png"), (85, 85))
    exit_rect = exit1.get_rect()
    exit_rect.center = (back.get_width() // 2 - 105, back.get_height() // 2)
    restart1 = pygame.transform.scale(load_image("UI/restart1.png"), (80, 80))
    restart2 = pygame.transform.scale(load_image("UI/restart2.png"), (85, 85))
    restart_rect = restart1.get_rect()
    restart_rect.center = (back.get_width() // 2 + 105, back.get_height() // 2)
    play_song = pygame.mixer.Sound("sounds/play.wav")
    exit_song = pygame.mixer.Sound("sounds/exit.wav")
    restart_song = pygame.mixer.Sound("sounds/new.wav")
    play_song.set_volume(0.5)
    exit_song.set_volume(0.5)
    exit_song.set_volume(0.5)

    while running:
        display.blit(back, (0, 0))
        if play_rect.collidepoint(pygame.mouse.get_pos()):
            display.blit(play2, (play_rect.x, play_rect.y))
            for i in pygame.event.get():
                if i.type == MOUSEBUTTONDOWN:
                    running = False
                    play_song.play()
                    return "play"
        else:
            display.blit(play1, (play_rect.x, play_rect.y))

        if exit_rect.collidepoint(pygame.mouse.get_pos()):
            display.blit(exit2, (exit_rect.x, exit_rect.y))
            for i in pygame.event.get():
                if i.type == MOUSEBUTTONDOWN:
                    running = False
                    exit_song.play()
                    time.sleep(0.5)
                    return "exit"
        else:
            display.blit(exit1, (exit_rect.x, exit_rect.y))
        if restart_rect.collidepoint(pygame.mouse.get_pos()):
            display.blit(restart2, (restart_rect.x, restart_rect.y))
            for i in pygame.event.get():
                if i.type == MOUSEBUTTONDOWN:
                    running = False
                    restart_song.play()
                    return "newgame"
        else:
            display.blit(restart1, (restart_rect.x, restart_rect.y))

        if pygame.mouse.get_focused():
            sprite.rect.x, sprite.rect.y = pygame.mouse.get_pos()
            all_sprites.draw(display)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                return "exit"
        screen.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))
        pygame.display.flip()
        clock.tick(60)

def pauses(display):

    pygame.init()
    back = pygame.transform.scale(load_image("UI/pause_back.png"), DISPLAY_SIZE)
    play1 = pygame.transform.scale(load_image("UI/play1.png"), (90, 90))
    play2 = pygame.transform.scale(load_image("UI/play2.png"), (95, 95))
    play_rect = play1.get_rect()
    play_rect.center = (back.get_width() // 2, back.get_height() // 2)
    exit1 = pygame.transform.scale(load_image("UI/exit1.png"), (80, 80))
    exit2 = pygame.transform.scale(load_image("UI/exit2.png"), (85, 85))
    exit_rect = exit1.get_rect()
    exit_rect.center = (back.get_width() // 2 - 105, back.get_height() // 2)
    play_song = pygame.mixer.Sound("sounds/play.wav")
    exit_song = pygame.mixer.Sound("sounds/exit.wav")
    play_song.set_volume(0.5)
    exit_song.set_volume(0.5)
    display.blit(back, (0, 0))
    if play_rect.collidepoint(pygame.mouse.get_pos()):
        display.blit(play2, (play_rect.x, play_rect.y))
        for i in pygame.event.get():
            if i.type == MOUSEBUTTONDOWN:
                running = False
                play_song.play()
                return "play"
    else:
        display.blit(play1, (play_rect.x, play_rect.y))

    if exit_rect.collidepoint(pygame.mouse.get_pos()):
        display.blit(exit2, (exit_rect.x, exit_rect.y))
        for i in pygame.event.get():
            if i.type == MOUSEBUTTONDOWN:
                running = False
                exit_song.play()
                return "exit"
    else:
        display.blit(exit1, (exit_rect.x, exit_rect.y))
    return ""

if __name__ == '__main__':
    runnings = True
    while runnings:
        # save_game()
        screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        display = pygame.Surface(DISPLAY_SIZE, 0, 32)
        pygame.display.set_icon(load_image("UI/logo.png"))
        pygame.display.set_caption("RatNCat")
        a = menu(display, screen)
        if a == "exit":
            sys.exit(0)
        elif a == "play":
            open_save()
        elif a == "newgame":
            save_game(a=True)
            open_save()
        jumper = 0
        global kicks, players, decoration_group, enemies, decoration_mobs, abilities_group, all_sprites, \
            sprite, image, decorations, pickups, world_data, world, player, camera, ui, cur_cutscene, boss
        pygame.init()
        pygame.display.set_caption('Test')
        font_cutscene = pygame.font.SysFont('Tahoma', 15)

        players = pygame.sprite.Group()
        runes = pygame.sprite.Group()
        poisons = pygame.sprite.Group()
        clock = pygame.time.Clock()

        bullet_group = pygame.sprite.Group()
        partickles_group = pygame.sprite.Group()
        background_group = pygame.sprite.Group()

        kick_sound = pygame.mixer.Sound("sounds/kick.wav")
        jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        jump2_sound = pygame.mixer.Sound("sounds/djump.wav")

        bullet_kick = pygame.mixer.Sound("sounds/bullet_kick.wav")

        kick_sound.set_volume(0.3)
        jump_sound.set_volume(0.3)
        jump2_sound.set_volume(0.3)
        bullet_kick.set_volume(0.3)

        startup()

        running = True
        pygame.mouse.set_visible(False)
        pause = False
        eventer = ""
        abilityy = Ability()
        color_hp = (21, 143, 26)
        runner = ""
        while running:
            if newLevel:
                level += 1
                startup()
                newLevel = False
                save_game()

            draw_bg()

            world.draw(display, scroll_data)

            pickups.pickups_group.draw(display)

            for i in abilities_group:
                i.draw2(display)
            runes.draw(display)
            poisons.draw(display)
            partickles_group.draw(display)
            enemies.draw(display)
            player.draw(display)
            decorations.decoration_group.draw(display)

            if boss is not None:
                for bossK in bosses:  # без группы и следования по спрайтам в ней нельзя удалить спрайт, спасибо пайгейм
                    bossK.draw(display)

            abilities_group.draw(display)
            ui.draw_hp(player, display, color_hp)
            ui.draw_mana(display, player)
            if player.rune:
                ui.draw_runes(display, player)
            ui.draw_rnes_window(display)
            if fps_show is True:
                ui.debug_mode(display, kicks, clock)
            if level <= 8:
                for mob in decoration_mobs:
                    mob.update(scroll)
                    mob.move()
            a = 0
            for i in abilities_group:
                a = i.default()
            if not a:
                color_hp = (21, 143, 26)
            else:
                color_hp = (20, 30, 255)
            if not pause:
                scroll_data = camera.obstacle_list(
                    world, scroll, decorations, pickups)
                player.update(scroll)
                if boss is not None:
                    for bossK in bosses:  # без группы и следования по спрайтам в ней нельзя удалить спрайт, спасибо пайгейм
                        bossK.update(scroll)
                        bossK.move(player, scroll_data, enemies)
                        for i in abilities_group:
                            i.kick(bossK, runes, poisons, i, False)

                        if pygame.sprite.spritecollide(bossK, players, False):
                            if bossK.contact == 7:
                                if not a:
                                    color_hp = (21, 143, 26)
                                    player.kick(bossK)
                                    bossK.contact = 0
                                    bossK.kick_wait = 15
                                else:
                                    color_hp = (20, 30, 255)
                            bossK.contact += 1
                        else:
                            bossK.contact = 0
                        if pygame.sprite.spritecollide(bossK, kicks, False):
                            bossK.kick(player, poisons)
                if not isCutscene:
                    for i in partickles_group:
                        i.update(scroll)
                        i.move()
                    for item in runes:
                        item.update(scroll)
                        item.move(scroll_data, partickles_group)
                        item.proverka(player, display, ui)

                    for poison in poisons:
                        poison.update(scroll)
                        poison.move(scroll_data, partickles_group)
                        if pygame.sprite.spritecollide(poison, players, False):
                            poison.poison_baf(player)

                    for enemy in enemies:
                        enemy.draw_hp(display)

                        if pygame.sprite.spritecollide(enemy, kicks, False):
                            enemy.kick(player, runes, poisons, True)
                            if enemy.type_enemy == "eye" and enemy.alive is False and random.randint(0, 10) == 10:
                                enemies.add(BadEye(enemy.rect.x, enemy.rect.y, player))

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
                        if enemy.type_enemy == "eye":
                            bullet_group = enemy.move(player, scroll_data)
                        else:
                            enemy.move(player, scroll_data, partickles_group)

                        bullet_group.draw(display)
                        for i in bullet_group:
                            if pygame.sprite.spritecollide(i, players, False):
                                player.kick(i)
                                bullet_kick.play()
                                i.kick(partickles_group)
                            if pygame.sprite.spritecollide(i, kicks, False):
                                i.kick(partickles_group)
                            i.update(scroll)
                            i.move(player, scroll_data)

                    if player.marvin:
                        ui.draw_marvin(display)
                        marvin_count += 1
                        if marvin_count >= 90:
                            player.marvin = False
                            marvin_count = 0
                    if player.tomas:
                        ui.draw_tomas(display)
                        tomas_count += 1
                        if tomas_count >= 90:
                            player.tomas = False
                            tomas_count = 0

                    if player.alive:
                        player.move(moving_left, moving_right, scroll_data, partickles_group)
                    else:
                        startup()
                else:
                    for enemy in enemies:
                        enemy.update(scroll)
                    if cutscenes[level][cur_cutscene][0] > 0:
                        cutscenes[level][cur_cutscene][0] -= 1
                        textsurface = font_cutscene.render(cutscenes[level][cur_cutscene][1], False, (255, 255, 0))
                        display.blit(textsurface, (player.rect.x - len(cutscenes[level][cur_cutscene][1]) * 3, player.rect.y - 100))
                    else:
                        jumper += 1
                        isCutscene = False
                        cur_cutscene += 1

                if pygame.sprite.spritecollide(player, pickups.pickups_group, False):
                    for pickup in pickups.pickups_group:
                        if pygame.sprite.spritecollide(pickup, players, False):
                            newLevel, isCutscene = pickup.touch(player, newLevel, isCutscene)

                kicks.empty()

                for i in abilities_group:
                    i.update(scroll)
                    i.move(player, scroll)
                    i.clocker(player)

                true_scroll[0] = (player.rect.center[0] - true_scroll[0] - A_scroll) // 15
                true_scroll[1] = (player.rect.center[1] - true_scroll[1] - B_scroll) // 15
                scroll = true_scroll.copy()
                scroll[0], scroll[1] = int(scroll[0]), int(scroll[1])

            else:
                if eventer == "ability":
                    a = abilityy.update(player, ui)
                    if a == 0:
                        abilityy.draw(display)
                    else:
                        abilities_group.add(a)
                        pause = False
                elif eventer == "pause":
                    b = pauses(display)
                    if b == "exit":
                        running = False
                    elif b == "play":
                        pause = False
                        eventer = ""
                if pygame.mouse.get_focused():
                    sprite.rect.x, sprite.rect.y = pygame.mouse.get_pos()
                    all_sprites.draw(display)



            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_F5:
                        fps_show = not fps_show
                    if player.alive:
                        if event.key in [K_a, K_LEFT]:
                            moving_left = True
                        if event.key in [K_d, K_RIGHT]:
                            moving_right = True
                        if event.key in [K_w, K_UP] and player.alive and (not player.in_air or player.doubleJ and player.rune_type == "jump"):
                            if not player.in_air:
                                jump_sound.play()
                            else:
                                jump2_sound.play()
                            player.jump = True
                        if level != 0:
                            if event.key in [K_SPACE, K_DOWN]:
                                kick_sound.play()
                                kick()
                    if event.key in [K_ESCAPE]:
                        pause = not pause
                        eventer = "pause"
                    if event.key in [K_TAB]:
                        if player.mana_count == 7:
                            pause = True
                            eventer = "ability"
                    if event.key in [K_e] and player.rune_true:
                        for i in runes:
                            player.rune = True
                            player.rune_type = i.type_rune
                            i.kill()
                    if event.key in [K_g] and player.rune is True:
                        ff = 0
                        if player.flip is False:
                            ff = 10
                        else:
                            ff = -10
                        rune = Rune(player.rect.x, player.rect.y,ff, player.rune_type)
                        runes.add(rune)
                        player.speed = player.speed_2
                        player.rune = False
                        player.rune_type = ""

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
    sys.exit(0)
