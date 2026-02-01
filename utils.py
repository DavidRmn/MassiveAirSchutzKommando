import pygame
from dataclasses import dataclass
import particle

class SpriteAnimation:
    def __init__(self, path: str, animations: dict, animation_cooldown: int, angle_offset: float):

        self.path = path
        self.animations = animations
        self.animation_list: list[list[list[pygame.surface.Surface]]] = []

        self.angle_offset = angle_offset

        for animation, frames in self.animations.items():
            self.animation_list.append(self.__load_animations(animation, frames))

        print(self.animation_list)

        self.current_animation: int = 0

        self.locked_animations = []

        self.animation_cooldown = animation_cooldown
        self.time_since_last_frame = 0
        self.current_animation_frame = 0
        self.animation_locked = False
        self.animation_index = 0


    @staticmethod
    def __load_image(image_path: str, angle: float = None):
        image = pygame.image.load(image_path).convert_alpha()
        if angle is not None:
            image = pygame.transform.rotate(image, angle)
        return image

    def __load_animations(self, animation: str, frames: int):
        animations: list[list[pygame.surface.Surface]] = []
        for angle_step in range(16):
            current_animation = []

            for frame_index in range(frames):
                frame = self.__load_image(
                    self.path + animation + '_' + str(frame_index) + '.png', self.angle_offset)
                current_animation.append(frame)

            self.angle_offset += 360 / 16

            animations.append(current_animation)

        return animations

    def set_animation(self, animation: int):
        if self.animation_locked:
            return

        if animation != self.current_animation:
            self.current_animation = animation
            self.current_animation_frame = 0
            self.time_since_last_frame = pygame.time.get_ticks()

            if animation in self.locked_animations:
                self.animation_locked = True

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.time_since_last_frame >= self.animation_cooldown:
            self.current_animation_frame += 1
            self.time_since_last_frame = current_time

        if self.current_animation_frame >= len(self.animation_list[self.current_animation][self.animation_index]):
            self.current_animation_frame = 0
            if self.animation_locked:
                self.animation_locked = False

        return  self.animation_list[self.current_animation][self.animation_index][self.current_animation_frame]


@dataclass
class GameData:
    title: str = 'Massive Air Schutz Kommando'
    width: int = 1280
    height: int = 720

    # states
    is_running = True

    music = 'Audio/mask_ost.wav'
    volume = 0.5

    font_path: str = 'Font/EDITIA__.TTF'
    text_color: str = '#ffffff'
    button_color: str = '#260d34'
    hover_color: str = '#452459'
    click_color: str = '#fe6c90'
    accent_color: str = '#ffffff'
    click_volume = 0
    hover_volume = 0.5

    game_logo_path: str = 'Images/Logo.png'
    background_layer_path: str = 'Images/Background1.png'
    depth_layer_one_path: str = 'Images/Background2.png'
    depth_layer_two_path: str = 'Images/Background3.png'
    foreground_layer_path: str = 'Images/Ground.png'
    tower_layer_path: str = 'Images/Tower.png'

    player_sprite_path: str = 'Images/Turret/'
    player_animation_cooldown: int = 85

    alien_sprite_path: str = 'Images/Alien/'
    alien_animation_cooldown: int = 85
    
    bullet_sprite_path: str = "Images/Bullet.png"
    alien_dmg_particle_sprite_path: str = "Images/Alien_Dmg_Particle.png"

    hp_icon_path: str = 'Images/HP.png'
    skull_icon_path: str = 'Images/Skull.png'
    
    # lists
    aliens_list = []
    bullet_list = []
    drops_list = []
    
    particle_engine = particle.ParticleEngine()
    
    #stats
    player_1_kills = 0
    player_2_kills = 0
    tower_life = 3

    alien_count = 0
        