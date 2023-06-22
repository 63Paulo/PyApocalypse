import pygame
import pytmx
import pyscroll
from pygame.locals import *

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Objet ajouté {item}")
        else:
            print("Le sac à dos est plein !")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Retirer l'objet {item}")
        else:
            print("Objet non présent dans le sac à dos")

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, 200, 100))

        font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            text = font.render(item, True, (0, 0, 0))
            surface.blit(text, (20, 20 + i * 20))

    def display_inventory(self):
        print("Sac à dos:")
        for item in self.items:
            print(item)
