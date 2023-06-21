from dataclasses import dataclass
import pygame
import pytmx
import pyscroll
from pygame.locals import *

from player import NPC, NPCHostile

@dataclass
class Portal:
    from_world : str
    origin_point : str
    target_world : str
    teleport_point : str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals : list[Portal]
    npcs : list[NPC]
    hostile_npcs: list[NPC]

class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = 'world'

        self.register_map('world', portals=[
            Portal(from_world='world', origin_point='enter_spawnhouse', target_world='spawn_house', teleport_point='enterspawn_spawnhouse')
        ], hostile_npcs=[
            NPCHostile('player1', nb_points=2, dialog=["aaeezzdzfffzefzazfaf"])
        ])
        self.register_map('spawn_house', portals=[
            Portal(from_world='spawn_house', origin_point='exit_spawnhouse', target_world='world', teleport_point='exitspawn_spawnhouse'),
            Portal(from_world='spawn_house', origin_point='enter_level1', target_world='map_levelone', teleport_point='enterspawn_level1')
        ],
        npcs=[
            NPC('spawnnpc', nb_points=4, dialog=["Ne bougez plus ! Vous êtes quoi, un zombie ?", "Oh, un survivant !", "Ca alors, je ne m'attendais pas a en voir de si tôt"])
        ]
        )
        self.register_map('map_levelone', portals=[
            Portal(from_world='map_levelone', origin_point='enter_spawnhouse_fromlvl1', target_world='spawn_house', teleport_point='exitspawn_level1'),
            Portal(from_world='map_levelone', origin_point='enterhouse1_lvl1', target_world='house1_lvl1', teleport_point='enterspawn_house1_lvl1'),
            Portal(from_world='map_levelone', origin_point='enter2_house1_lvl1', target_world='house1_lvl1', teleport_point='enterspawn2_house1_lvl1'),
            Portal(from_world='map_levelone', origin_point='enterhouse2_lvl1', target_world='house2_lvl1', teleport_point='enterspawn_house2_lvl1'),
            Portal(from_world='map_levelone', origin_point='enterhouse3_lvl1', target_world='house3_lvl1', teleport_point='enterspawn_house3_lvl1'),
            Portal(from_world='map_levelone', origin_point='enterbunker_lvl1', target_world='bunker_lvl1', teleport_point='enterspawn_bunker_lvl1'),
        ])
        self.register_map('house1_lvl1', portals=[
            Portal(from_world='house1_lvl1', origin_point='exithouse1_lvl1', target_world='map_levelone', teleport_point='spawnexit_house1_lvl1'),
            Portal(from_world='house1_lvl1', origin_point='exit2_house1_lvl1', target_world='map_levelone', teleport_point='spawnexit2_house1_lvl1'),
        ])
        self.register_map('house2_lvl1', portals=[
            Portal(from_world='house2_lvl1', origin_point='exit_house2_lvl1', target_world='map_levelone', teleport_point='spawnexit_house2_lvl1'),
        ])
        self.register_map('house3_lvl1', portals=[
            Portal(from_world='house3_lvl1', origin_point='exithouse3_lvl1', target_world='map_levelone', teleport_point='exitspawn_house3_lvl1'),
        ])
        self.register_map('bunker_lvl1', portals=[
            Portal(from_world='bunker_lvl1', origin_point='exit_bunker_lvl1', target_world='map_levelone', teleport_point='exitspawn_bunker_lvl1'),
        ])

        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collision(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        #portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)


        for sprite in self.get_group().sprites():

            if type(sprite) is NPC :
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else :
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()


    def register_map(self, name, portals=[], npcs=[], hostile_npcs=[]):
         
        tmx_data = pytmx.util_pygame.load_pygame(f"map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        group.add(self.player)

        #récupérer les npcs pour les ajouter au groupe

        for npc in npcs:
            group.add(npc)

        for hostile_npc in hostile_npcs:
            group.add(hostile_npc)

            hostile_npc.player = self.player

        #créer objet map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, hostile_npcs)

    def get_map(self):
        return self.maps[self.current_map]

    
    def get_group(self):
        return self.get_map().group
    
    def get_walls(self):
        return self.get_map().walls
    
    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)
    
    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            hostile_npcs = map_data.hostile_npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

            for hostile_npc in hostile_npcs:
                hostile_npc.load_points(map_data.tmx_data)
                hostile_npc.teleport_spawn()
    
    
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()
        for hostile_npc in self.get_map().hostile_npcs:
            hostile_npc.move()