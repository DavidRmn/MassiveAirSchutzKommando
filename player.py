import pygame
from debug import debug
from game import GameData

class Player(pygame.sprite.Sprite):
    def __init__(self, group, controller_index: int = 0):
        super().__init__(group)

        self.image = pygame.Surface((GameData.width, GameData.height))
        self.rect = self.image.get_rect(center=(GameData.width / 2, GameData.height / 2))

        self.axis = pygame.joystick.Joystick(controller_index)

        self.speed = 1
        self.direction = pygame.math.Vector2()

        self.animations = {
            'IDLE': 1,
            'FIRE': 3
        }

        self.locked_animations = []

        self.animation_frames = self.__load_animations()

        self.current_animation = 'IDLE'
        self.animation_cooldown = GameData.player_animation_cooldown
        self.time_since_last_frame = 0
        self.current_animation_frame = 0
        self.animation_locked = False

    @staticmethod
    def __load_image(image_path):
        image = pygame.transform.scale_by(pygame.image.load(image_path).convert_alpha(), GameData.width / 480)
        return image

    def __load_animations(self):
        animations = {}

        for animation, frames in self.animations.items():
            current_animation = []

            for frame_index in range(frames):
                frame = self.__load_image(
                    GameData.player_sprite_path + animation + '_' + str(frame_index) + '.png')
                current_animation.append(frame)

            animations[animation] = current_animation

        return animations

    def set_animation(self, animation: str):
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

            if self.current_animation_frame >= self.animations[self.current_animation]:
                self.current_animation_frame = 0
                if self.animation_locked:
                    self.animation_locked = False

        self.image = self.animation_frames[self.current_animation][self.current_animation_frame]

    def move(self):
        self.rect.x += self.direction.x * self.speed

    def get_input(self):
        if self.axis.get_axis(0) > 0.5:
            self.direction.x = 1
        elif self.axis.get_axis(0) < -0.5:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.axis.get_button(5):
            self.set_animation('FIRE')
        else:
            self.set_animation('IDLE')

    def update(self):
        self.update_animation()
        self.get_input()
        self.move()
