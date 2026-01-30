import pygame
from debug import debug
from utils import GameData

class Level(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        pygame.init()

        self.display_surf = pygame.display.get_surface()
        self.display_rect = self.display_surf.get_rect()

        self.offset = (self.display_rect.topleft[1], (self.display_rect.topleft[0] - (GameData.width - GameData.height)))

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

        self.tower_layer_surf = pygame.transform.scale_by(
            pygame.image.load(GameData.tower_layer_path).convert_alpha(), GameData.width / 480)
        self.level_surf.append((self.tower_layer_surf, self.offset))

    def custom_draw(self, delta_time: float):

        self.display_surf.blits(self.level_surf)

        for sprite in self.sprites():
            self.display_surf.blit(sprite.image, sprite.rect)

        debug(f'{delta_time}')