import pygame
from debug import debug
from game import GameData

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.image.load(GameData.player_sprite_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.axis = pygame.joystick.Joystick(0)

        self.direction = pygame.math.Vector2()

        self.animations = {
            'FIRE': 3
        }

    def get_image(self):
        pass

    def move(self):
        self.rect.x += self.direction.x

    def get_input(self):
        if abs(self.axis.get_axis(0)) > 0.5:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def update(self):
        self.get_input()
        self.move()