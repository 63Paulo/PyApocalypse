import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, item=None):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.item = item  
        self.feet = self.rect