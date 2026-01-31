import pygame
from pygame import Vector2
from utils import GameData

class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, position: Vector2, col_radius : float, speed: float, dmg: int):
        super().__init__(group)
        self.surf = pygame.image.load("")
        self.rect = self.surf.get_frect(center=(0,0))
        self.position = position
        self.direction : Vector2 = Vector2(0, 0)
        self.col_radius = col_radius
        self.speed = speed
        self.dmg = dmg
        self.surf = pygame.transform.rotate(self.surf, self.direction.angle)
        GameData.bullet_list.append(self)
        # max distance
        pass
    
    def on_hit(self):
        self.is_ded()
        pass
    
    def is_ded(self):
        GameData.bullet_list.remove(self)
    
    def update(self, dt: float):
        self.rect.center += self.direction * self.speed * dt
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)
        
        