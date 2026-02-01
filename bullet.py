from os import kill

import pygame
from pygame import Vector2
from utils import GameData

class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, position: Vector2, direction: Vector2, col_radius : float, speed: float, dmg: int, life_time: float, player: int):
        super().__init__(group)
        self.image = pygame.transform.rotate(pygame.image.load(GameData.bullet_sprite_path), -direction.angle - 90)
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_frect(center=Vector2(position))
        self.position: Vector2 = Vector2(position)
        self.direction = Vector2.normalize(direction)
        self.col_radius = col_radius
        self.speed = speed
        self.dmg = dmg
        self.life_time = life_time
        self.life_timer = 0
        GameData.bullet_list.append(self)
        self.ded = False
        self.player = player
    
    def on_hit(self):
        self.is_ded()
    
    def is_ded(self):
        if self.ded: return
        GameData.bullet_list.remove(self)
        self.kill()
        self.ded = True
    
    def custom_update(self, dt: float):
        self.position = Vector2(self.rect.center)
        self.life_timer += dt
        if self.life_timer >= self.life_time:
            self.is_ded()
        self.rect.center += self.direction * self.speed * dt

    #def draw(self, screen: pygame.Surface):
     #   screen.blit(self.image, self.rect)
