import pygame


class Camera:
    def __init__(self):
        self.scroll = [0, 0]
        self.obstacle = []

    def obstacle_list(self, world, scroll, decor, pickups):
        self.scroll = scroll
        self.obstacle = world.obstacle_list
        for i in self.obstacle:
            i[1].x = i[1].x - self.scroll[0]
            i[1].y = i[1].y - self.scroll[1]
        for i in decor.decoration_group:
            i.rect.x = i.rect.x - self.scroll[0]
            i.rect.y = i.rect.y - self.scroll[1]
        for i in pickups.pickups_group:
            i.rect.x = i.rect.x - self.scroll[0]
            i.rect.y = i.rect.y - self.scroll[1]

        return self.obstacle
