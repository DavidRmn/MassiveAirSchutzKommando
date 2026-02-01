import pygame
import collision_manager
import level
import simulation_manager
from enum import Enum
from button import Button
from utils import GameData

STATE = Enum('STATE', [('MAIN', 1), ('GAME', 2), ('PAUSE', 3), ('END', 4)])

class Game:
    def __init__(self):
        pygame.display.set_caption(GameData.title)
        self.screen = pygame.display.set_mode((GameData.width, GameData.height))
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.delta_time = 0.016
        self.level = level.Level()
        self.aliens = []

        self.state = STATE.MAIN

        self.offset = (self.rect.topleft[1],
                       (self.rect.topleft[0] - (GameData.width - GameData.height)))

        self.font = pygame.font.Font(GameData.font_path, 52)

        start_button = Button(
            x=int(GameData.width * 0.2 + 300 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=300, height=150,
            text='START GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        continue_button = Button(
            x=int(GameData.width * 0.3), y=int(GameData.height * 0.8), width=300, height=150,
            text='CONTINUE GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        back_to_main_button = Button(
            x=640, y=520, width=150, height=50,
            text='BACK TO MAIN', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.85,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        end_button = Button(
            x=int(GameData.width * 0.8 - 300 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=300, height=150,
            text='END GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.buttons = pygame.sprite.Group()

        self.buttons.add(start_button)
        self.buttons.add(end_button)

        pygame.init()

    def run(self):
        while GameData.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameData.is_running = False


            background = pygame.transform.scale_by(
                pygame.image.load(GameData.background_layer_path).convert_alpha(),
                GameData.width / 480
            )
            self.screen.blit(background, self.offset)

            if self.state == STATE.GAME:
                # sim and collision
                simulation_manager.simulation_engine()
                collision_manager.check()

                self.level.update()
                self.level.custom_update(self.delta_time)
                self.level.custom_draw(self.delta_time)

                GameData.particle_engine.engine(self.screen, self.delta_time)
            else:
                self.buttons.update()
                self.buttons.draw(self.screen)
            
            pygame.display.flip()
            self.delta_time = self.clock.tick(120) / 1000

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()