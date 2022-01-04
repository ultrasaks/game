import pygame


class Pickup:
    def __init__(self):
        self.pickups_group = pygame.sprite.Group()

    def add_pickup(self, pickup, x, y):
        pickup.rect = pickup.image.get_rect()
        pickup.rect.x, pickup.rect.y = x, y
        self.pickups_group.add(pickup)