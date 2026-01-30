import pygame
import level
import player
import aliens
import debug

from random import randint
from utils import GameData

class Game:
    def __init__(self, caption, width, height):
        self.width = width
        self.height = height
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.level = level.Level()

        self.player_one = player.Player(self.level)
        self.player_two = player.Player(self.level)

        self.aliens = []

        pygame.init()

    def run(self):

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if len(self.aliens) < 10:
                alien_spawn_x = randint(0, self.width - 10)
                alien_spawn_y = randint(0, self.height - 10)
                self.aliens.append(aliens.Alien(self.level, alien_spawn_x, alien_spawn_y))

            self.screen.fill('#f0eee9')

            debug.debug('Awesome Debug Message')

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game(caption=GameData.title, width=GameData.width, height=GameData.height)
    game.run()