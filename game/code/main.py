import pygame
import sys
from settings import *
from tools import ImgEditor
from main_level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('AbobaGame')
        pygame.display.set_icon(ImgEditor.load_image("icon.png", colorkey=-1))

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(SIZE)
        monitor = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode(monitor, pygame.FULLSCREEN)

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_time = self.clock.tick() / 1000
            print(delta_time)

            self.screen.fill('black')
            self.level.run(delta_time)
            pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()
