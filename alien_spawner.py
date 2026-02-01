import random
import alien
from pygame import Vector2
from utils import GameData, SpriteAnimation

class AlienSpawner:
    def __init__(self, positions: list[tuple[int, int]]):
        self.positions = positions
        self.spawn_timer: float = 0.0
        self.spawn_interval: float = 0.1
        self.aliens_max = 200
        self.alien_count = 0

        self.alien_animations = SpriteAnimation(path=GameData.alien_sprite_path,
                                                animations={'ALIEN': 3},
                                                animation_cooldown=85,
                                                angle_offset=90.0)
        
    def update(self, dt: float):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and self.aliens_max > self.alien_count:
            index = random.randint(0, len(self.positions) - 1)
            rand_x = self.positions[index][0] + random.uniform(-10, 10)
            rand_y = self.positions[index][1] + random.uniform(-10, 10)
            alien.Alien(Vector2(rand_x, rand_y), Vector2(rand_x, rand_y), 12, 150, 100, self.alien_animations)
            self.spawn_timer = 0
            self.alien_count += 1
        pass