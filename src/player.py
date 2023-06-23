
import pygame
from inventory import Inventory

from animation import AnimateSprite
from projectile import Projectile

class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.health = 100
        self.max_health = 100
        self.inventory = Inventory(capacity=10)
        self.projectiles = pygame.sprite.Group()

    def update_health_bar(self, surface):
        bar_color = (79, 152, 0)
        back_bar_color = (255, 0, 0)
        bar_position = [self.rect.x, self.rect.y, self.health, 5]
        back_bar_position = [self.rect.x, self.rect.y, self.max_health, 5]

        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def damage(self, amount):
        #Infliger les dégats
        self.health -= amount

    def is_dead(self):
        return self.health <= 0

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self): 
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self): 
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self): 
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self) : 
        self.change_animation("down")
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def launch_projectile(self):
        projectile = Projectile('sprite/player/Bullet.png', self.rect.center, [1,0], 5)
        self.projectiles.add(projectile)
    
class Player(Entity):
    def __init__(self):
        super().__init__("player", 0, 0)


class NPC(Entity):
    def __init__(self, name, nb_points, dialog):
        super().__init__(name, 0, 0)
        self.dialog = dialog
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.speed = 1
        self.current_point = 0

    def move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3 :
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3 :
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3 :
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3 :
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point


    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()
    
    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


class NPCHostile(NPC):
    def __init__(self, name, nb_points, dialog):
        super().__init__(name, nb_points, dialog)
        self.speed = 0.5

    def pursue_player(self):
        player_position = self.player.position
        npc_position = self.position

        if player_position[0] < npc_position[0]:
            self.move_left()
        elif player_position[0] > npc_position[0]:
            self.move_right()

        if player_position[1] < npc_position[1]:
            self.move_up()
        elif player_position[1] > npc_position[1]:
            self.move_down()

    def update(self):
        super().update()
        self.check_collision_with_player()
        self.pursue_player()

    def check_collision_with_player(self):
        if self.rect.colliderect(self.player.rect):
            self.player.damage(0.5)
    
    def update_health_bar(self, surface):
        bar_color = (130,30 , 0)
        back_bar_color = (30, 30, 30)
        bar_position = [self.rect.x, self.rect.y, self.health, 5]
        back_bar_position = [self.rect.x, self.rect.y, self.max_health, 5]

        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def damage(self, amount):
        #Infliger les dégats
        self.health -= amount
    
