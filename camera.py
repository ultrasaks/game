import pygame


class Camera():
    def __init__(self):
        self.scroll = [0, 0]
        self.obstacle = []

    def obstacle_list(self, world, scroll):
        self.scroll = scroll
        self.obstacle = world.obstacle_list
        for i in self.obstacle:
            i[1].x = i[1].x - self.scroll[0]
            i[1].y = i[1].y - self.scroll[1]

        return self.obstacle
