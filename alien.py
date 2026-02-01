import random
import uuid
import pygame
from pygame import Vector2
from math import floor
from utils import GameData

class Alien(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, target: Vector2, col_radius : float, speed: float, hp: int, animations):
        super().__init__()
        self.id = uuid.uuid4()
        self.surf = pygame.transform.scale_by(pygame.image.load(GameData.alien_sprite_path + 'ALIEN_0.png'), 2)
        self.surf_render = self.surf
        self.rect = self.surf.get_frect(center=position)
        self.position: Vector2 = position
        self.direction : Vector2 = Vector2.normalize(Vector2(random.uniform(-1, 1), random.uniform(-1, 1)))
        self.col_radius = col_radius
        self.speed = speed
        self.hp = hp
        self.attack_timer_limit = random.uniform(10, 20)
        self.attack_timer = 0
        GameData.aliens_list.append(self)
        self.is_attacking = False
        
        #behavior
        self.group_range = 65
        self.group_factor = 0.015
        self.align_range = 50
        self.align_factor = 0.05
        self.avoid_range = 20
        self.avoid_factor = 0.2
        
        self.group_sum : Vector2 = Vector2(0,0)
        self.group_count = 0
        self.align_sum : Vector2 = Vector2(0,0)
        self.align_count = 0
        self.avoid_sum : Vector2 = Vector2(0,0)
        self.avoid_count = 0
        
        self.group_vec : Vector2 = Vector2(0,0)
        self.align_vec : Vector2 = Vector2(0,0)
        self.avoid_vec : Vector2 = Vector2(0,0)
        self.target_vec : Vector2 = Vector2(0,0)

        self.target : Vector2 = target
        self.target_factor_x = 0.00003
        self.target_factor_y = 0.00035
        
        self.final_vec : Vector2 = Vector2(0,0)
        
        self.ded = False

        self.animations = animations

        pass
        
    def on_hit(self, dmg: int, player: int):
        #print(f"on hit {dmg}")
        self.update_hp(dmg, player)
        GameData.particle_engine.new_system(self.position, GameData.alien_dmg_particle_sprite_path, 5, 0, 0.25, False, (6, 6), 0.25, 25, 80, 0, 0.75, "white", (0, 2) )
        pass
    
    def attack(self):
        if self.is_attacking: return
        self.target = Vector2(GameData.width / 2, GameData.height - 64)
        self.target_factor_x = 0.0035
        self.target_factor_y = 0.0035
        self.is_attacking = True
        self.align_factor *= 2
    
    def update_hp(self, amount: int, player: int):
        self.hp -= amount
        if self.hp <= 0:
            self.is_ded(player)
    
    def is_ded(self, player: int):
        if self.ded: return
        self.kill()
        GameData.particle_engine.new_system(self.position, GameData.alien_dmg_particle_sprite_path, 10, 0, 0.25, False, (16, 16), 0.25, 60, 120, 0, 0.5, "white", (0, 0) )
        GameData.aliens_list.remove(self)
        self.ded = True
        GameData.alien_count -= 1
        if player == 1:
            GameData.player_1_kills += 1
        if player == 2:
            GameData.player_2_kills += 1

    def update(self, dt: float):
        self.attack_timer += dt
        if self.attack_timer >= self.attack_timer_limit:
            #self.attack()
            pass
        
        # tower logic is here
        if self.is_attacking and self.position.distance_squared_to(self.target) < 32*32:
            GameData.tower_life -= 1
            self.is_ded(0)
        
        self.position = Vector2(self.rect.center)
        self.rect.center += self.direction * self.speed * dt
        #self.check_bounds()

        self.animations.animation_index = 15 - floor((self.direction.angle + 180) / 22.5)
        self.surf = self.animations.update_animation()
        
    def check_bounds(self):
        if self.position.x > GameData.width - 20:
            self.direction.x *= -1
        if self.position.x < 20:
            self.direction.x *= -1
        if self.position.y > GameData.height - 50:
            self.direction.y *= -1
        if self.position.y < 20:
            self.direction.y *= -1
    
    def draw(self, screen: pygame.Surface):
        #pygame.draw.line(screen, "white", self.rect.center, self.rect.center + self.final_vec * 20, 2)
        #pygame.draw.line(screen, "green", self.rect.center, self.rect.center + self.direction * 20, 2)
        #pygame.draw.line(screen, "yellow", self.rect.center, self.rect.center + Vector2(self.align_vec) * 20, 3)
        #pygame.draw.line(screen, "pink", self.rect.center, self.rect.center + Vector2(self.group_vec) * 20, 3)
        #pygame.draw.line(screen, "red", self.rect.center, self.rect.center + Vector2(self.target_vec) * 20, 3)
        #pygame.draw.circle(screen, "blue", self.target, 5, 3)
        screen.blit(self.surf, self.rect)
        
    
    def simulation_reset(self):
        self.group_sum : Vector2 = Vector2(0,0)
        self.group_count = 0
        self.group_vec : Vector2 = Vector2(0,0)
        
        self.align_sum : Vector2 = Vector2(0,0)
        self.align_count = 0
        self.align_vec : Vector2 = Vector2(0,0)
        
        self.avoid_sum : Vector2 = Vector2(0,0)
        self.avoid_count = 0
        self.avoid_vec : Vector2 = Vector2(0,0)
        
        self.target_vec : Vector2 = Vector2(0,0)
        
    
    def simulate(self, others, index):
        self.simulation_reset()
        start = index
        for i in range(index, len(others)):
            if self is others[i]: continue
            #if self.direction.dot(other.direction) > -0.5: return
            dist = self.position.distance_squared_to(others[i].position)
            
            if dist < self.group_range * self.group_range:
                self.group_sum += others[i].position
                self.group_count += 1
            else:
                continue 
    
            if dist < self.align_range * self.align_range:
                self.align_sum += others[i].direction
                self.align_count += 1
                
            if dist < self.avoid_range * self.avoid_range:
                self.avoid_sum += others[i].position
                self.avoid_count += 1
            
        if self.group_count > 0:
            self.group_vec = Vector2.normalize(self.group_sum / self.group_count - self.position) * self.group_factor

        if self.align_count > 0:
            self.align_vec = Vector2.normalize(self.align_sum / self.align_count) * self.align_factor
            
        if self.avoid_count > 0:
            self.avoid_vec = -Vector2.normalize(self.avoid_sum / self.avoid_count - self.position) * self.avoid_factor

        self.target_vec = Vector2((self.target - self.position).x * self.target_factor_x, (self.target - self.position).y * self.target_factor_y)

        self.final_vec = self.group_vec + self.align_vec + self.avoid_vec + self.target_vec
        
        if self.final_vec.magnitude_squared() > 0.000001:
            self.direction = Vector2.normalize(self.direction + self.final_vec)
           
