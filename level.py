import pygame
import tower
import player
import alien_spawner
from debug import debug
from utils import GameData
import time

import math

class Level(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        pygame.init()
        
        self.spawner = alien_spawner.AlienSpawner([(int(GameData.width / 8), int(GameData.height / 3)), 
                                                   (int(GameData.width / 8 * 2), int(GameData.height / 4)),
                                                   (int(GameData.width / 8 * 3), int(GameData.height / 4)),
                                                   (int(GameData.width / 8 * 4), int(GameData.height / 4)),
                                                   (int(GameData.width / 8 * 5), int(GameData.height / 4)),
                                                   (int(GameData.width / 8 * 6), int(GameData.height / 4)),
                                                   (int(GameData.width / 8 * 7), int(GameData.height / 3))
                                                   ])

        self.display_surf = pygame.display.get_surface()
        self.display_rect = self.display_surf.get_rect()

        self.offset = (self.display_rect.topleft[1],
                       (self.display_rect.topleft[0] - (GameData.width - GameData.height)))

        self.level_surf: list[tuple[pygame.Surface, tuple[int, int]]] = []

        self.background_layer_surf = pygame.transform.scale_by(
            pygame.image.load(GameData.background_layer_path).convert_alpha(), GameData.width / 480)
        self.level_surf.append((self.background_layer_surf, self.offset))

        self.depth_layer_one_surf = pygame.transform.scale_by(
            pygame.image.load(GameData.depth_layer_one_path).convert_alpha(), GameData.width / 480)
        self.level_surf.append((self.depth_layer_one_surf, self.offset))

        self.depth_layer_two_surf = pygame.transform.scale_by(
            pygame.image.load(GameData.depth_layer_two_path).convert_alpha(), GameData.width / 480)
        self.level_surf.append((self.depth_layer_two_surf, self.offset))

        self.foreground_layer_surf = pygame.transform.scale_by(
            pygame.image.load(GameData.foreground_layer_path).convert_alpha(), GameData.width / 480)
        self.level_surf.append((self.foreground_layer_surf, self.offset))

        self.tower = tower.Tower(self)

        self.players = {}

        for player_count in range(pygame.joystick.get_count()):
            self.players[f'Player_{player_count}'] = player.Player(self, controller_index=player_count)

    def custom_update(self, delta_time: float):
        self.spawner.update(delta_time)
        
        #players
        for name, player in self.players.items():
            player.custom_update(delta_time)

        # update aliens
        for alien in GameData.aliens_list:
            alien.update(delta_time)
        
        # update bullet
        for bullet in GameData.bullet_list:
            bullet.custom_update(delta_time)

    def custom_draw(self, delta_time: float):
        # draw backgrounds
        self.display_surf.blits(self.level_surf)
        
        # draw player stuff
        for sprite in self.sprites():
            self.display_surf.blit(sprite.image, sprite.rect)

        # draw aliens
        for alien in GameData.aliens_list:
            alien.draw(self.display_surf)
            
        # draw bullet
        #for bullet in GameData.bullet_list:
          #  bullet.draw(self.display_surf)

        debug(f'{pygame.mouse.get_pos()}', pos_x=400)
        debug(f'FPS: {(1.0 / delta_time):.0f}')