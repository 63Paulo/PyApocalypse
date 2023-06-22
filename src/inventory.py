import pygame
from pygame.locals import *

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Added item: {item}")
        else:
            print("Inventory is full!")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed item: {item}")
        else:
            print("Item not found in inventory!")

    def draw(self, surface):
        # Dessinez les éléments de l'inventaire sur la surface donnée
        # Utilisez les méthodes et attributs de Pygame pour dessiner les éléments

        # Exemple simple : dessiner un rectangle pour représenter l'inventaire
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, 200, 100))

        # Exemple : dessiner le texte des éléments de l'inventaire
        font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            text = font.render(item, True, (0, 0, 0))
            surface.blit(text, (20, 20 + i * 20))

    def display_inventory(self):
        print("Sac à dos:")
        for item in self.items:
            print(item)

    def draw_inventory(self):
        self.player.inventory.draw(self.screen)  # Dessiner l'inventaire du joueur sur la surface du jeu
