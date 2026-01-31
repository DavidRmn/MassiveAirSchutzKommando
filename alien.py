import random
import uuid
import pygame
from pygame import Vector2
from utils import GameData

class Alien(pygame.sprite.Sprite):
    def __init__(self, position: Vector2, target: Vector2, col_radius : float, speed: float, hp: int):
        super().__init__()
        self.id = uuid.uuid4()
        self.surf = pygame.image.load(GameData.alien_sprite_path)
        self.surf_render = self.surf
        self.rect = self.surf.get_frect(center=position)
        self.position = position
        self.direction : Vector2 = Vector2.normalize(Vector2(random.uniform(-1, 1), random.uniform(-1, 1)))
        self.col_radius = col_radius
        self.speed = speed
        self.hp = hp
        self.attack_timer_limit = random.uniform(10, 20)
        self.attack_timer = 0
        GameData.aliens_list.append(self)
        self.is_attacking = False
        
        #behavior
        self.group_range = 50
        self.group_factor = 0.015
        self.align_range = 40
        self.align_factor = 0.0225
        self.avoid_range = 25
        self.avoid_factor = 0.03
        
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
        self.target_factor_x = 0.00015
        self.target_factor_y = 0.0004
        
        self.final_vec : Vector2 = Vector2(0,0)
        pass
        
    def on_hit(self, dmg: int):
        self.update_hp(dmg)
        pass
    
    def attack(self):
        if self.is_attacking: return
        self.target = Vector2(GameData.width / 2, GameData.height - 160)
        self.target_factor_x = 0.005
        self.target_factor_y = 0.005
        self.is_attacking = True
        self.align_factor *= 4
    
    def update_hp(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.is_ded()
    
    def is_ded(self):
        self.kill()
        GameData.aliens_list.remove(self)

    def update(self, dt: float):
        self.attack_timer += dt
        if self.attack_timer >= self.attack_timer_limit:
            self.attack()
        
        if self.is_attacking and self.position.distance_squared_to(self.target) < 32*32:
            self.is_ded()
        
        self.position = Vector2(self.rect.center)
        self.rect.center += self.direction * self.speed * dt
        #self.check_bounds()
        
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
        pygame.draw.line(screen, "white", self.rect.center, self.rect.center + self.final_vec * 20, 2)
        pygame.draw.line(screen, "green", self.rect.center, self.rect.center + self.direction * 20, 2)
        pygame.draw.line(screen, "yellow", self.rect.center, self.rect.center + Vector2(self.align_vec) * 20, 3)
        pygame.draw.line(screen, "pink", self.rect.center, self.rect.center + Vector2(self.group_vec) * 20, 3)
        pygame.draw.line(screen, "red", self.rect.center, self.rect.center + Vector2(self.target_vec) * 20, 3)
        pygame.draw.circle(screen, "blue", self.target, 5, 3)
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
           
