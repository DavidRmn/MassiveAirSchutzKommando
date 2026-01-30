import pygame

class Game:
    def __init__(self, caption, width, height):
        self.width = width
        self.height = height
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.init()

    def run(self):

        run = True
        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.screen.fill('#d6ebf7')
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game('Massive Air Schutz Kommando', 1280, 720)
    game.run()