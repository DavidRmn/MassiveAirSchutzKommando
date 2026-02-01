import pygame
import collision_manager
import level
import simulation_manager
from enum import Enum
from button import Button
from utils import GameData
from debug import debug

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

        pygame.mixer.music.load(GameData.music)
        pygame.mixer.music.set_volume(GameData.volume)
        pygame.mixer.music.play(loops=-1)

        self.controller = []
        for controller in range(pygame.joystick.get_count()):
            self.controller.append(pygame.joystick.Joystick(controller))

        self.state = STATE.MAIN

        self.offset = (self.rect.topleft[1],
                       (self.rect.topleft[0] - (GameData.width - GameData.height)))

        self.font = pygame.font.Font(GameData.font_path, 50)

        self.start_button = Button(
            x=int(GameData.width * 0.2 + 350 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='START GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.continue_button = Button(
            x=int(GameData.width * 0.2 + 350 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='CONTINUE GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.back_to_main_button = Button(
            x=int(GameData.width * 0.8 - 350 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='BACK TO MAIN', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.85,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.end_button = Button(
            x=int(GameData.width * 0.8 - 350 / 2), y=int(GameData.height * 0.8 - 150 / 2), width=350, height=150,
            text='END GAME', text_color=GameData.text_color, text_font=GameData.font_path,
            text_size=24, text_length=0.65,
            button_color=GameData.button_color, hover_color=GameData.hover_color, click_color=GameData.click_color,
            accent_color=GameData.accent_color, outline_width=5
        )

        self.retry_button = Button(
            x=int(GameData.width / 2), y=int(GameData.height / 2), width=350, height=150,
            text='RETRY', text_color=GameData.text_color, text_font=GameData.font_path,
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
        self.pos_up = (int(GameData.width / 2), int(GameData.height / 2))

        pygame.mouse.set_visible(False)

    def run(self):
        while GameData.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameData.is_running = False

            for controller in self.controller:
                mouse_pos = pygame.mouse.get_pos()
                d_pad = controller.get_hat(0)[0]
                e_pad = controller.get_hat(0)[1]
                if controller.get_button(7) and self.state != STATE.PAUSE:
                    self.state = STATE.PAUSE
                    self.buttons.empty()
                    self.buttons.add(self.continue_button)
                    self.buttons.add(self.back_to_main_button)

                # right
                if e_pad == 1 and self.debounce < 0:
                    #print('dpad right')
                    #pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(self.pos_up)
                    self.debounce = self.debounce_time

                # right
                if d_pad == 1 and self.debounce < 0:
                    #print('dpad right')
                    #pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(self.pos_right)
                    self.debounce = self.debounce_time

                if self.state == STATE.MAIN and controller.get_button(0) \
                        and self.end_button.rect.left < mouse_pos[0] < self.end_button.rect.right \
                        and self.end_button.rect.top < mouse_pos[1] < self.end_button.rect.bottom and self.debounce < 0:
                    #print('END GAME')
                    GameData.is_running = False

                if self.state == STATE.PAUSE and controller.get_button(0) \
                        and self.back_to_main_button.rect.left < mouse_pos[0] < self.back_to_main_button.rect.right \
                        and self.back_to_main_button.rect.top < mouse_pos[1] < self.back_to_main_button.rect.bottom and self.debounce < 0:
                    #print('BACK TO MENU')
                    self.state = STATE.RESET
                    self.debounce = self.debounce_time

                # left
                if d_pad == -1 and self.debounce < 0:
                    #print('dpad left')
                    #pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(self.pos_left)
                    self.debounce = self.debounce_time

                if self.state == STATE.MAIN and controller.get_button(0) \
                        and self.start_button.rect.left < mouse_pos[0] < self.start_button.rect.right \
                        and self.start_button.rect.top < mouse_pos[1] < self.start_button.rect.bottom and self.debounce < 0:
                    #print('START GAME')
                    self.state = STATE.GAME
                    self.debounce = self.debounce_time

                if self.state == STATE.PAUSE and controller.get_button(0) \
                        and self.continue_button.rect.left < mouse_pos[0] < self.continue_button.rect.right \
                        and self.continue_button.rect.top < mouse_pos[1] < self.continue_button.rect.bottom and self.debounce < 0:
                    #print('CONTINUE GAME')
                    self.state = STATE.GAME
                    self.debounce = self.debounce_time

                if self.state == STATE.GAMEOVER and controller.get_button(0) \
                        and self.retry_button.rect.left < mouse_pos[0] < self.retry_button.rect.right \
                        and self.retry_button.rect.top < mouse_pos[1] < self.retry_button.rect.bottom and self.debounce < 0:
                    #print('RETRY')
                    self.state = STATE.RESET
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
                # sim and collision
                simulation_manager.simulation_engine()
                collision_manager.check()
                GameData.alien_count = 0
                self.level.update()
                self.level.custom_update(self.delta_time)
                self.level.custom_draw(self.delta_time)

                GameData.particle_engine.engine(self.screen, self.delta_time)

            if self.state == STATE.MAIN:

                self.screen.blit(game_logo,
                                 (GameData.width / 2 - game_logo.width / 2, GameData.height / 2 - game_logo.height))
                self.buttons.update()
                self.buttons.draw(self.screen)

            if self.state == STATE.PAUSE:

                self.screen.blit(game_logo,
                                 (GameData.width / 2 - game_logo.width / 2, GameData.height / 2 - game_logo.height))
                self.buttons.update()
                self.buttons.draw(self.screen)

            if self.state == STATE.RESET:

                for alien in GameData.aliens_list:
                    alien.is_ded(0)
                for bullet in GameData.bullet_list:
                    bullet.is_ded()
                GameData.aliens_list = []
                GameData.bullet_list = []
                GameData.player_1_kills = 0
                GameData.player_2_kills = 0
                GameData.alien_count = 0
                GameData.tower_life = 3

                self.state = STATE.MAIN
                self.buttons.empty()
                self.buttons.add(self.start_button)
                self.buttons.add(self.end_button)
                
            if self.state == STATE.GAMEOVER:
                game_over_surf = self.font.render("GAME OVER", True, '#ffffff')
                game_over_rect = game_over_surf.get_rect(
                    center=(GameData.width / 2, GameData.height / 2 - 150))
                self.screen.blit(game_over_surf, game_over_rect)

                highscore_surf = self.font.render(f"High Score: {GameData.player_1_kills + GameData.player_2_kills}", True, '#ffffff')
                highscore_rect = highscore_surf.get_rect(
                    center=(GameData.width / 2, GameData.height / 2 + 150))
                self.screen.blit(highscore_surf, highscore_rect)

                if GameData.player_2_kills > 0:
                    player_one_surf = self.font.render(f"P1K: {GameData.player_1_kills}", True, '#ffffff')
                    player_one_rect = player_one_surf.get_rect(
                        center=(GameData.width / 2 - 200, GameData.height / 2 + 250))
                    self.screen.blit(player_one_surf, player_one_rect)

                    player_two_surf = self.font.render(f"P2K: {GameData.player_2_kills}", True, '#ffffff')
                    player_two_rect = player_two_surf.get_rect(
                        center=(GameData.width / 2 + 200, GameData.height / 2 + 250))
                    self.screen.blit(player_two_surf, player_two_rect)

                self.buttons.empty()
                self.buttons.add(self.retry_button)
                self.buttons.update()
                self.buttons.draw(self.screen)
                

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

            if self.retry_button.action_ready:
                self.state = STATE.RESET
                self.retry_button.reset()
                
            # game over check
            if GameData.tower_life <= 0 and self.state != STATE.GAMEOVER:
                pygame.mouse.set_pos(GameData.width / 2, GameData.height / 2)
                self.state = STATE.GAMEOVER

            #debug(f'{pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]}', pos_x=400)
            #debug(f'{self.end_button.rect.left, self.end_button.rect.right}', pos_x=400, pos_y=400)

            pygame.display.flip()
            self.delta_time = self.clock.tick(120) / 1000

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()