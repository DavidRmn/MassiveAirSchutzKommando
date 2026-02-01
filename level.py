import pygame
import tower
import player
import alien_spawner
from debug import debug
from utils import GameData

class Level(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        pygame.init()
        
        self.spawner = alien_spawner.AlienSpawner([(int(GameData.width / 4), int(GameData.height / 3)), 
                                                   (int(GameData.width / 4 * 2), int(GameData.height / 4)),
                                                   (int(GameData.width / 4 * 3), int(GameData.height / 3))
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

        self.icon_border_offset = 25
        self.hp_icon_surf = pygame.image.load(GameData.hp_icon_path).convert_alpha()
        self.hp_icon_rect = self.hp_icon_surf.get_rect()
        self.skull_icon_surf = pygame.image.load(GameData.skull_icon_path).convert_alpha()
        self.skull_icon_rect = self.skull_icon_surf.get_rect()

        self.level_surf.append((self.skull_icon_surf, (0 + self.icon_border_offset,
                                                   GameData.height - self.hp_icon_rect.height - self.icon_border_offset * 2)))

        self.level_surf.append((self.skull_icon_surf, (GameData.width - self.hp_icon_rect.width - self.icon_border_offset,
                                                   GameData.height - self.hp_icon_rect.height - self.icon_border_offset * 2)))

        self.players = {}

        self.font = pygame.font.Font(GameData.font_path, 25)

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

        for life in range(GameData.tower_life):
            self.display_surf.blit(self.hp_icon_surf, (int(GameData.width / 2 - 60) + self.icon_border_offset * life * 2,
                                                       GameData.height - self.hp_icon_rect.height - self.icon_border_offset + 10))

        for player, _ in enumerate(self.players):
            kills = [GameData.player_1_kills, GameData.player_2_kills]
            text = self.font.render(text=f'{kills[player]}', antialias=True, color='#ffffff')
            if player == 0:
                text_rect = text.get_rect(topleft=(0 + self.hp_icon_rect.width + self.icon_border_offset * 2,
                                                       GameData.height - self.hp_icon_rect.height - self.icon_border_offset * 2))
            else:
                text_rect = text.get_rect(topleft=(GameData.width - self.hp_icon_rect.width - self.icon_border_offset * 2.5,
                                                       GameData.height - self.hp_icon_rect.height - self.icon_border_offset * 2))
            self.display_surf.blit(text, text_rect)


        # draw bullet
        #for bullet in GameData.bullet_list:
          #  bullet.draw(self.display_surf)

        #debug(f'{pygame.mouse.get_pos()}', pos_x=400)
        debug(f'FPS: {(1.0 / delta_time):.0f}')