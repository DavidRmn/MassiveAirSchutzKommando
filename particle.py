import random

import pygame
from pygame import Surface


class ParticleEngine:
    particleSystems = []

    def engine(self, screen: Surface, dt):
        for ps in self.particleSystems:
            if not ps.engine(screen, dt):
                self.particleSystems.remove(ps)
    
    def new_system(self, pos: (float, float), image: str, count: int, emit_time: float, duration :float, loop :bool, size: (float, float), life_time: float, speed_min: float, speed_max: float, drag: float, size_over_time: float, color, direction: (float, float)):
        newSystem = ParticleSystem(pos, image, count, emit_time, duration, loop, size, life_time, speed_min, speed_max, drag, size_over_time, color, direction)
        self.particleSystems.append(newSystem)
        return newSystem

class ParticleSystem:
    def __init__(self, pos: (float, float), image, count: int, emit_time: float, duration :float, loop :bool, size: (float, float), life_time: float, speed_min: float, speed_max: float, drag: float, size_over_time: float, color, direction: (float, float)):
        self.pos = pos
        self.image = image
        self.count = count
        self.emit_time = emit_time
        self.duration = duration
        self.loop = loop
        self.size = size
        self.life_time = life_time
        self.speed_min = speed_min
        self.speed_max = speed_max
        self.drag = drag
        self.size_over_time = size_over_time
        self.color = color
        self.direction = direction

        # setup data
        self.duration_timer = 0
        self.emission_timer = 0
        self.particles = []

        # initial spawn
        for i in range(self.count):
            self.particles.append(Particle(self.pos, self.image, self.size, self.life_time, self.speed_min, self.speed_max, self.drag, self.size_over_time, self.color, self.direction))
        
    def emission(self, dt: float):
        if self.emit_time <= 0: return
        self.emission_timer += dt
        if self.emission_timer >= self.emit_time:
            self.emission_timer = 0
            for i in range(self.count):
                self.particles.append(Particle(self.pos, self.image, self.size, self.life_time, self.speed_min, self.speed_max, self.drag, self.size_over_time, self.color, self.direction))
        
    def engine(self, screen: Surface, dt: float) -> bool:
        self.emission(dt)
        self.duration_timer += dt
        for p in self.particles:
            if not p.engine(screen, dt):
                self.particles.remove(p)
            if self.duration_timer >= self.duration:
                if self.loop: self.duration_timer = 0
                else: return False
        return True
    
    def update_position(self, pos: (float, float)):
        self.pos = pos
        
    def update_color(self, color):
        self.color = color

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos: (float, float), image, size: (float, float), life_time: float, speed_min: float, speed_max: float, drag: float, size_over_time: float, color, direction: (float, float)):
        super().__init__()
        self.original_image = pygame.image.load(image).convert_alpha()
        self.size = size
        self.surf = self.original_image
        self.surf.fill(color, None, pygame.BLEND_RGBA_MULT)
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_frect(center = (pos[0], pos[1]))
        self.startPos = (pos[0], pos[1])
        self.life_time = life_time
        self.speed = random.uniform(speed_min, speed_max)
        self.drag = drag
        self.size_over_time = size_over_time
        self.direction = pygame.Vector2.normalize(pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()) + pygame.Vector2(direction[0], direction[1])
        self.life_timer = 0
        self.size_over_time_timer = 0
        self.scale_step = (size_over_time - 1) / life_time
        self.scale_interation = 0


    def engine(self, screen: Surface, dt: float) -> bool:
        self.life_timer += dt
        self.apply_drag(dt)
        self.apply_size_over_time(dt)
        self.rect.center += self.direction * self.speed * dt
        self.draw(screen)
        if self.life_timer >= self.life_time:
            return False
        return True
    
    def draw(self, screen):
        screen.blit(self.surf, self.rect)
    
    def apply_drag(self, dt: float):
        if self.speed > 0:
            self.speed -= self.drag * dt
        else:
            self.speed = 0
            
    def apply_size_over_time(self, dt: float):
        self.size_over_time_timer += dt
        size = (self.size[0] + self.size[0] * self.scale_step * self.size_over_time_timer, self.size[1] + self.size[1] * self.scale_step * self.size_over_time_timer)
        self.surf = pygame.transform.smoothscale(self.surf, size)