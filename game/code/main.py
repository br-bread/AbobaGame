import pygame
import sys
from settings import *
from tools import ImgEditor
from main_scene import MainScene
from first_street_scene import FirstStreetScene


class Game:
    def __init__(self):
        # general
        pygame.init()
        pygame.display.set_caption('AbobaGame')
        pygame.display.set_icon(ImgEditor.load_image("icon.png", colorkey=-1))

        # screen
        self.screen = pygame.display.set_mode((1920, 1080))
        monitor = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        print(monitor)
        self.screen = pygame.display.set_mode(monitor, pygame.FULLSCREEN)
        print(self.screen)

        self.clock = pygame.time.Clock()
        self.main_scene = MainScene()
        self.first_street_scene = FirstStreetScene(
            ImgEditor.enhance_image(ImgEditor.load_image("/backgrounds/first_street_scene.png"), 4), CENTER)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_time = self.clock.tick() / 1000

            self.screen.fill('black')
            self.first_street_scene.run(delta_time)
            self.main_scene.run(delta_time)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
