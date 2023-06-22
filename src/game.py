import pygame
import pytmx
import pyscroll
from pygame.locals import *
from map import MapManager
from inventory import Inventory
from dialog import DialogBox
from player import NPCHostile, Player



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Apocalypse')
        self.npc_hostile = NPCHostile("Walk", 0, [""])
        self.npc_hostile = NPCHostile("Walk2", 0, [""])
        self.player = Player()        
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()
        self.game_over = False
        self.inventory_visible = False

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
        elif pressed[pygame.K_s]:
            self.player.move_down()
        elif pressed[pygame.K_q]:
            self.player.move_left()
        elif pressed[pygame.K_d]:
            self.player.move_right()
        
        if pressed[pygame.K_i]:
            if not self.inventory_key_pressed:
                self.inventory_key_pressed = True
                self.inventory_visible = not self.inventory_visible
        else:
            self.inventory_key_pressed = False

    def update(self):
        self.map_manager.update()

    def game_over_screen(self):
        self.screen.fill((20, 20, 20)) 

        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", True, (150, 0, 24))
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)

        restart_text = font.render("Appuyez sur R pour rejouer", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(400, 350))
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def draw_inventory(self):
         if self.inventory_visible:
            self.player.inventory.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.player.update_health_bar(self.screen)
            self.npc_hostile.update_health_bar(self.screen)
            self.draw_inventory()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collision(self.dialog_box)


            if self.player.is_dead():
                self.game_over_screen()
                self.player.animate_death()
                self.game_over = True

                if self.game_over:

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
        
                            if event.key == pygame.K_r:
                                self.game_over = False
                                self.player = Player()
                                self.map_manager = MapManager(self.screen, self.player)
                                self.dialog_box = DialogBox()

            clock.tick(60)
        pygame.quit()
