import pygame
from bullet import Bullet
from alien import Alien
from utils import GameData

clock = pygame.Clock()

def bullet_collision(bullet: Bullet, alien: Alien):
    if bullet.position.distance_squared_to(alien.position) <= bullet.col_radius * bullet.col_radius + alien.col_radius * alien.col_radius:
        return True
    return False

while GameData.is_running:
    for bul in GameData.bullet_list:
        for ali in GameData.aliens_list:
            if bullet_collision(bul, ali):
                bul.on_hit()
                ali.on_hit(bul.dmg)
    clock.tick(60)
    
