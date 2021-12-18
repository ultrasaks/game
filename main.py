import pygame
import os
import sys
import random

FPS = 60
SCREEN_SIZE = 800, 600
GRAVITY = 0.75
moving_left = False
moving_right = False


def load_image(name):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"'{fullname}' not found!")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    images = load_image("test_sprite.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.speed = 5
        self.vel_y = 0
        self.image = Player.images
        self.rect = self.image.get_rect()
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True
        self.defence = 0  # потом
        self.damage = 0  # потом
        self.hp = 100  # потом

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            if player.in_air:
                dx -= 1
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            if player.in_air:
                dx += 1
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Enemy(pygame.sprite.Sprite):
    img = load_image('wtf.png')

    def __init__(self, x, y):
        super().__init__()
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hp = 100
        self.defence = 0  # потом
        self.damage = 0  # потом

    def kick(self):
        self.hp -= random.randint(20, 40)
        print(f'HIT! HP={self.hp}')
        if self.hp <= 0:
            self.kill()


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
        player.draw()
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
