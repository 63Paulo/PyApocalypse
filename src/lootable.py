import pygame


class Lootable:
    def __init__(self, x, y, width, height, items):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = items