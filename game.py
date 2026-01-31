import pygame

import collision_manager
import level
import simulation_manager
from utils import GameData

class Game:
    def __init__(self):
        pygame.display.set_caption(GameData.title)
        self.screen = pygame.display.set_mode((GameData.width, GameData.height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.016

        self.level = level.Level()

        self.aliens = []


        pygame.init()

    def run(self):

        while GameData.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameData.is_running = False

            self.screen.fill('#f0eee9')

            # sim and collision
            simulation_manager.simulation_engine()
            collision_manager.check()

            self.level.update()
            self.level.custom_update(self.delta_time)
            self.level.custom_draw(self.delta_time)

            
            pygame.display.flip()
            self.delta_time = self.clock.tick(120) / 1000

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()