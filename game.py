import pygame
import collision_manager
import level
import simulation_manager
from enum import Enum
from button import Button
from utils import GameData

STATE = Enum('STATE', [('MAIN', 1), ('GAME', 2), ('PAUSE', 3), ('RESET', 4), ("GAMEOVER", 5)])

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GameData.title)
        self.screen = pygame.display.set_mode((GameData.width, GameData.height))
        self.rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.delta_time = 0.016
        self.level = level.Level()
        self.aliens = []

        self.music = pygame.Sound(GameData.music)
        self.music.set_volume(GameData.volume)

        self.controller = []
        for controller in range(pygame.joystick.get_count()):
            self.controller.append(pygame.joystick.Joystick(controller))

        self.state = STATE.MAIN

        self.offset = (self.rect.topleft[1],
                       (self.rect.topleft[0] - (GameData.width - GameData.height)))

        self.font = pygame.font.Font(GameData.font_path, 50)

        self.start_button = Button(
            x=int(GameData.width * 0.2 + 300 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='START GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.continue_button = Button(
            x=int(GameData.width * 0.2 + 300 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='CONTINUE GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.back_to_main_button = Button(
            x=int(GameData.width * 0.8 - 300 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='BACK TO MAIN', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.85,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.end_button = Button(
            x=int(GameData.width * 0.8 - 300 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='END GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.buttons = pygame.sprite.Group()

        self.buttons.add(self.start_button)
        self.buttons.add(self.end_button)

        self.debounce_time = 20
        self.debounce = self.debounce_time

        self.pos_right = (int(GameData.width * 0.8 - 300 / 2) + 50, int(GameData.height * 0.8 - 150 / 2) + 50)
        self.pos_left = (int(GameData.width * 0.2 + 300 / 2) + 50, int(GameData.height * 0.8 - 150 / 2) + 50)

    def run(self):
        while GameData.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameData.is_running = False

            for controller in self.controller:
                d_pad = controller.get_hat(0)[0]
                if controller.get_button(7) and self.state != STATE.PAUSE:
                    self.state = STATE.PAUSE
                    self.buttons.empty()
                    self.buttons.add(self.continue_button)
                    self.buttons.add(self.back_to_main_button)

                # right
                if d_pad == 1 and self.debounce < 0:
                    #print('dpad right')
                    #pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(self.pos_right)
                    self.debounce = self.debounce_time

                if self.state == STATE.MAIN and controller.get_button(0) and pygame.mouse.get_pos() == self.pos_right and self.debounce < 0:
                    #print('END GAME')
                    GameData.is_running = False

                if self.state == STATE.PAUSE and controller.get_button(0) and pygame.mouse.get_pos() == self.pos_right and self.debounce < 0:
                    #print('BACK TO MENU')
                    self.state = STATE.RESET
                    self.debounce = self.debounce_time

                # left
                if d_pad == -1 and self.debounce < 0:
                    #print('dpad left')
                    #pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(self.pos_left)
                    self.debounce = self.debounce_time

                if self.state == STATE.MAIN and controller.get_button(0) and pygame.mouse.get_pos() == self.pos_left and self.debounce < 0:
                    #print('START GAME')
                    self.state = STATE.GAME
                    self.debounce = self.debounce_time

                if self.state == STATE.PAUSE and controller.get_button(0) and pygame.mouse.get_pos() == self.pos_left and self.debounce < 0:
                    #print('CONTINUE GAME')
                    self.state = STATE.GAME
                    self.debounce = self.debounce_time

            if self.debounce > -1:
                self.debounce -= 1
                #print(self.debounce)

            background = pygame.transform.scale_by(
                pygame.image.load(GameData.background_layer_path).convert_alpha(),
                GameData.width / 480
            )
            
            game_logo = pygame.transform.scale_by(
                pygame.image.load(GameData.game_logo_path).convert_alpha(),
                (GameData.width / 480) * 2
            )

            self.screen.blit(background, self.offset)

            if self.state == STATE.GAME:
                self.music.play(loops=-1)
                # sim and collision
                simulation_manager.simulation_engine()
                collision_manager.check()
                GameData.alien_count = 0
                self.level.update()
                self.level.custom_update(self.delta_time)
                self.level.custom_draw(self.delta_time)

                GameData.particle_engine.engine(self.screen, self.delta_time)

            if self.state == STATE.MAIN:
                self.music.stop()
                self.screen.blit(game_logo,
                                 (GameData.width / 2 - game_logo.width / 2, GameData.height / 2 - game_logo.height))
                self.buttons.update()
                self.buttons.draw(self.screen)

            if self.state == STATE.PAUSE:
                self.music.stop()
                self.screen.blit(game_logo,
                                 (GameData.width / 2 - game_logo.width / 2, GameData.height / 2 - game_logo.height))
                self.buttons.update()
                self.buttons.draw(self.screen)

            if self.state == STATE.RESET:
                GameData.alien_count = 0
                self.state = STATE.MAIN
                self.buttons.empty()
                self.buttons.add(self.start_button)
                self.buttons.add(self.end_button)
                for alien in GameData.aliens_list:
                    alien.is_ded()
                for bullet in GameData.bullet_list:
                    bullet.is_ded()
                GameData.aliens_list = []
                GameData.bullet_list = []
                
            if self.state == STATE.GAMEOVER:
                GameData.aliens_list = []
                GameData.bullet_list = []
                GameData.alien_count = 0
                self.state = STATE.MAIN
                self.buttons.empty()
                self.buttons.add(self.start_button)
                self.buttons.add(self.end_button)
                

            if self.end_button.action_ready:
                GameData.is_running = False

            if self.start_button.action_ready:
                self.state = STATE.GAME
                self.start_button.reset()

            if self.continue_button.action_ready:
                self.state = STATE.GAME
                self.continue_button.reset()

            if self.back_to_main_button.action_ready:
                self.state = STATE.RESET
                self.back_to_main_button.reset()
                
            # game over check
            if GameData.tower_life <= 0:
                self.state = STATE.GAMEOVER
            
            pygame.display.flip()
            self.delta_time = self.clock.tick(120) / 1000

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()