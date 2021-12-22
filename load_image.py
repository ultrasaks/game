import os
import sys
import pygame


def load_image(name):
    fullname = os.path.join('sprites', name)
    if not os.path.isfile(fullname):
        print(f"'{fullname}' not found!")
        sys.exit()
    image = pygame.image.load(fullname)
    return image