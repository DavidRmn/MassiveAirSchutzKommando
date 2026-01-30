import pygame
from utils import GameData

class Level(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        pygame.init()

        self.display_surf = pygame.display.get_surface()
        self.background_layer_surf = pygame.image.load(GameData.background_layer_path).convert_alpha()
        self.background_layer_rect = self.background_layer_surf.get_rect()
        self.depth_layer_one_surf = pygame.image.load(GameData.depth_layer_one_path).convert_alpha()
        self.depth_layer_one_rect = self.depth_layer_one_surf.get_rect()
        self.depth_layer_two_surf = pygame.image.load(GameData.depth_layer_two_path).convert_alpha()
        self.depth_layer_two_rect = self.depth_layer_two_surf.get_rect()
        self.foreground_layer_surf = pygame.image.load(GameData.foreground_layer_path).convert_alpha()
        self.foreground_layer_rect = self.foreground_layer_surf.get_rect()

        self.display_surf.blit(self.background_layer_surf, self.background_layer_rect)
        self.display_surf.blit(self.depth_layer_one_surf, self.depth_layer_one_rect)
        self.display_surf.blit(self.depth_layer_two_surf, self.depth_layer_two_rect)
        self.display_surf.blit(self.foreground_layer_surf, self.foreground_layer_rect)

    def custom_draw(self):
        for sprite in self.sprites():
            print(sprite.image)
            self.display_surf.blit(sprite.image, sprite.rect)