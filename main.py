import pygame
import os
import sys
import random
from load_image import load_image
from player import Player
from enemy import Enemy
from constants import *


moving_left = False
moving_right = False


def draw_bg():
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 0, 0), (0, 300), (SCREEN_SIZE[0], 300))


def kick():
    kickTest = pygame.sprite.Sprite()
    kickTest.image = load_image('hit.png')
    kickTest.rect = kickTest.image.get_rect()
    if player.flip:
        kickpos = -20
    else:
        kickpos = 32
    kickTest.rect.x, kickTest.rect.y = player.rect.x + kickpos, player.rect.y
    kicks.add(kickTest)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Test')
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    enemies = pygame.sprite.Group()
    for _ in range(10):
        enem = Enemy(random.randint(0, SCREEN_SIZE[0]), random.randint(100, 300))
        enemies.add(enem)

    running = True
    player = Player()
    kicks = pygame.sprite.Group()

    while running:
        draw_bg()
        player.draw(screen)
        kicks.draw(screen)
        enemies.draw(screen)

        for enemy in enemies:
            if pygame.sprite.spritecollide(enemy, kicks, False):
                enemy.kick()
        kicks.empty()

        if player.alive:
            player.move(moving_left, moving_right)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        moving_left = True
                    if event.key == pygame.K_d:
                        moving_right = True
                    if event.key == pygame.K_w and player.alive and not player.in_air:
                        player.jump = True
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        kick()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
