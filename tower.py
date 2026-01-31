import pygame
from utils import GameData

class Tower(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("Images/Tower.png")
        self.rect = self.image.get_rect(midbottom=(GameData.width / 2, GameData.height))