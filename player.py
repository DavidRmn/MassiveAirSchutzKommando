import pygame
from math import floor
from game import GameData

class Player(pygame.sprite.Sprite):
    def __init__(self, group, controller_index: int = None):
        super().__init__(group)

        self.display_surf = pygame.display.get_surface()

        self.angle_increment = 0.05
        self.rotation_center = pygame.math.Vector2(640, 550)
        self.goal = pygame.math.Vector2(640, 450)

        self.initial_position = pygame.math.Vector2(self.display_surf.get_width() / 2, self.display_surf.get_height() * 0.65)

        self.image = pygame.image.load(GameData.player_sprite_path + 'IDLE_0.png')
        self.rect = self.image.get_rect(midbottom=self.initial_position)

        if controller_index is not None:
            self.controller = pygame.joystick.Joystick(controller_index)
        else:
            self.controller = False

        self.stick_pos = self.controller.get_axis(0)

        self.animation_index = 0
        self.idle_animations_frames = self.__load_animations('IDLE', 1)
        self.fire_animations_frames = self.__load_animations('FIRE', 2)

        self.current_animation = 'IDLE'

        self.locked_animations = []

        self.animation_cooldown = GameData.player_animation_cooldown
        self.time_since_last_frame = 0
        self.current_animation_frame = 0
        self.animation_locked = False

    @staticmethod
    def __load_image(image_path: str, angle: float = None):
        image = pygame.image.load(image_path).convert_alpha()
        if angle is not None:
            print(image_path)
            print(angle)
            image = pygame.transform.rotate(image, angle)
        return image

    def __load_animations(self, animation: str, frames: int):
        animations = []
        angle = 112.5
        for angle_step in range(16):
            current_animation = []

            for frame_index in range(frames):
                frame = self.__load_image(
                    GameData.player_sprite_path + animation + '_' + str(frame_index) + '.png', angle)
                current_animation.append(frame)

            angle += 360 / 16

            animations.append(current_animation)

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

        if self.current_animation == 'IDLE':
            if self.current_animation_frame >= len(self.idle_animations_frames[self.animation_index]):
                self.current_animation_frame = 0
                if self.animation_locked:
                    self.animation_locked = False
            self.image = self.idle_animations_frames[self.animation_index][self.current_animation_frame]

        elif self.current_animation == 'FIRE':
            if self.current_animation_frame >= len(self.fire_animations_frames[self.animation_index]):
                self.current_animation_frame = 0
                if self.animation_locked:
                    self.animation_locked = False
            self.image = self.fire_animations_frames[self.animation_index][self.current_animation_frame]

    def move(self):
        self.rect.center = self.goal

    def rotate(self, delta_angle: int = None):
        if delta_angle is None:
            delta_angle = self.goal.angle
            delta_angle *= self.angle_increment
            offset = self.goal - self.rotation_center
            self.goal = self.rotation_center + offset.rotate(delta_angle  * self.stick_pos)
        else:
            offset = self.goal - self.rotation_center
            self.goal = self.rotation_center + offset.rotate(delta_angle)

    def get_input(self):
        if self.controller:
            self.stick_pos = self.controller.get_axis(0)
            angle = (self.goal - self.rotation_center).angle + 180
            if 0 <= angle <= 250 or 290 <= angle <= 360:
                if self.stick_pos > 0.25:
                    self.rotate()
                elif self.stick_pos < -0.25:
                    self.rotate()
            # shift to the left
            elif angle > 270:
                self.rotate(delta_angle=int(angle - 290 + 5))
            # shift to the right
            elif angle < 270:
                self.rotate(delta_angle=-1 *  int(250 - angle + 5))

            if self.controller.get_button(5):
                self.set_animation('FIRE')
            else:
                self.set_animation('IDLE')

            self.animation_index = 15 - floor(angle / 22.5)

    def update(self):
        self.get_input()
        self.move()
        self.update_animation()