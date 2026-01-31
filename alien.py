import pygame
from utils import GameData

class Alien(pygame.sprite.Sprite):
    def __init__(self, group, position: pygame.Vector2, col_radius : float, speed: float, hp: int):
        super().__init__(group)
        self.surf = pygame.image.load("")
        self.surf_render = self.surf
        self.rect = self.surf.get_frect(center=(0,0))
        self.position = position
        self.direction : pygame.Vector2 = pygame.Vector2(0, 0)
        self.col_radius = col_radius
        self.speed = speed
        self.hp = hp
        GameData.aliens_list.append(self)
        pass
        
    def on_hit(self, dmg: int):
        self.update_hp(dmg)
        pass
    
    def update_hp(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.is_ded()
    
    def is_ded(self):
        self.kill()
        GameData.aliens_list.remove(self)

    def move(self, dt: float):
        self.get_wobble(dt)
        self.rect.center += self.direction * self.speed * dt
        self.surf = pygame.transform.rotate(self.surf, self.direction.angle)
        pass

    def get_wobble(self, dt: float):
        pass
    
    def draw(self):
        pass