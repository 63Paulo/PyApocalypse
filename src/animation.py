import pygame
from pygame.sprite import AbstractGroup

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"sprite/{name}.png")
        self.death_sprite_sheet = pygame.image.load("sprite/player/death.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down' : self.get_images(0),
            'up' : self.get_images(32),
            'right' : self.get_images(64),
            'left' : self.get_images(96)
        }
        self.death_animations = {
            'down': self.get_death_animation(0),
            'up': self.get_death_animation(32),
            'right': self.get_death_animation(64),
            'left': self.get_death_animation(96)
        }
        self.speed = 2.05

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(0, 0)
        self.clock += self.speed * 8

        if self.clock >= 100 :
            #passer a l'image suivante
            self.animation_index += 1

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            
            self.clock = 0

    def get_images(self, y ):
        images = []

        for i in range (0, 3):
            x = i*32
            image = self.get_image(x, y)
            images.append(image)

        return images

    def get_image(self,x,y):
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image

    def get_death_animation(self, direction_index):
        images = []
        sprite_width = self.death_sprite_sheet.get_width() // 4
        sprite_height = self.death_sprite_sheet.get_height() // 4

        for i in range(4):
            x = i * sprite_width
            y = direction_index * sprite_height
            image = pygame.Surface([sprite_width, sprite_height])
            image.blit(self.death_sprite_sheet, (0, 0), (x, y, sprite_width, sprite_height))
            images.append(image)

        return images
    
    def animate_death(self):
        direction = 'up'
        death_animation = self.death_animations[direction]

        for image in death_animation:
            self.image = image
            self.image.set_colorkey(0, 0)
            pygame.display.flip()
            pygame.time.wait(100)  