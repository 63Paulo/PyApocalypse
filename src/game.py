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
        self.game_over = False

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

    def game_over_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            game_over_text = pygame.font.Font(None, 36).render("Game Over", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(400, 300))
            self.screen.blit(game_over_text, game_over_rect)

            restart_text = pygame.font.Font(None, 24).render("Press R to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(400, 350))
            self.screen.blit(restart_text, restart_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return

    def run(self):
        clock = pygame.time.Clock()
        running = True
  

        while running:
            
            for projectile in self.player.all_projectiles:
                projectile.move()

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
                    if self.player.is_dead():
                        self.game_over()

            clock.tick(60)
        



        pygame.quit()
