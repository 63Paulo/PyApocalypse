import pygame
import pytmx
import pyscroll
from pygame.locals import *
from map import MapManager


from player import Player
from dialog import DialogBox



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('PyApocalypse')

        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()


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

    def update(self):
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()

        running = True

        while running:
            
            self.player.all_projectiles.draw(self.screen)
            
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.player.update_health_bar(self.screen)
            pygame.display.flip()

            for event  in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collision(self.dialog_box)
                        self.player.launch_projectile()

            clock.tick(60)
        



        pygame.quit()
