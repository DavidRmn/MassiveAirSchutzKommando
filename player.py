import pygame

from math import floor
from utils import GameData, SpriteAnimation

class Player(pygame.sprite.Sprite):
    def __init__(self, group, controller_index: int = None):
        super().__init__(group)

        self.display_surf = pygame.display.get_surface()

        self.angle_increment = 0.05
        self.rotation_center = pygame.math.Vector2(640, 655)
        self.goal = pygame.math.Vector2(640, 615)

        self.initial_position = pygame.math.Vector2(self.display_surf.get_width() / 2, self.display_surf.get_height() * 0.65)

        self.image = pygame.image.load(GameData.player_sprite_path + 'IDLE_0.png')
        self.rect = self.image.get_rect(midbottom=self.initial_position)

        if controller_index is not None:
            self.controller = pygame.joystick.Joystick(controller_index)
        else:
            self.controller = False

        self.stick_pos = self.controller.get_axis(0)

        self.animations = SpriteAnimation(path=GameData.player_sprite_path, animations={'IDLE': 1, 'FIRE': 2})

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
            if 0 <= angle <= 210 or 340 <= angle <= 360:
                if self.stick_pos > 0.25:
                    self.rotate()
                elif self.stick_pos < -0.25:
                    self.rotate()
            # shift to the left
            elif angle > 270:
                self.rotate(delta_angle=int(angle - 340 + 5))
            # shift to the right
            elif angle < 270:
                self.rotate(delta_angle=-1 *  int(210 - angle + 5))

            if self.controller.get_button(5):
                self.animations.set_animation(1)
            else:
                self.animations.set_animation(0)

            self.animations.animation_index = 15 - floor(angle / 22.5)

    def update(self):
        self.get_input()
        self.move()
        self.image = self.animations.update_animation()