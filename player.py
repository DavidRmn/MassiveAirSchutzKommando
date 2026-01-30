import pygame
from debug import debug
from game import GameData

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.image.load(GameData.player_sprite_path).convert_alpha()
        self.rect = self.image.get_rect()

    def move(self):
        pass

    @staticmethod
    def get_input():
        i = pygame.joystick.get_count()
        debug(f'{i}')

    def update(self):
        self.get_input()
        self.move()