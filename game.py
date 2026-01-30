import pygame
import level
import tower
import player
import aliens
import debug

from random import randint
from utils import GameData

class Game:
    def __init__(self):
        pygame.display.set_caption(GameData.title)
        self.screen = pygame.display.set_mode((GameData.width, GameData.height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.016

        self.level = level.Level()

        self.tower = tower.Tower(self.level)

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

            self.screen.fill('#f0eee9')

            self.level.update()
            self.level.custom_draw(delta_time=self.delta_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()