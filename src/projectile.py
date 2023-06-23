import pygame 
import pyscroll
import pytmx

class Projectile(pygame.sprite.Sprite) :
    def __init__(self, image, direction, position, speed):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.direction = direction
        self.speed = speed

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def check_collision_with_npc(self, npc):
        if pygame.sprite.collide_rect(self, npc):
            npc.damage(50)
            self.kill()