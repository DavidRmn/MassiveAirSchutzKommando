import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, group, spawn_x, spawn_y):
        super().__init__(group)
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        pass