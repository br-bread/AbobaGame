import pygame
import sys
import settings
from tools import ImgEditor
from menu import Menu
from first_street_scene import FirstStreetScene
from home_scene import HomeScene
from home_upscene import HomeUpScene
from inventory import Inventory
from journal import Journal
from environment import Sun


class Game:
    def __init__(self):
        # general
        pygame.init()
        pygame.display.set_caption(settings.NAME)
        pygame.display.set_icon(settings.ICON)

        # screen
        self.screen = pygame.display.set_mode((1920, 1080))
        monitor = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode(monitor, pygame.FULLSCREEN)

        # cursor
        settings.current_cursor = ImgEditor.enhance_image(ImgEditor.load_image('cursors/base_cursor.png'), 4)
        pygame.mouse.set_visible(False)

        # scenes
        self.scenes = {
            'menu': Menu(),
            'first_street_scene': FirstStreetScene(
                ImgEditor.enhance_image(ImgEditor.load_image('/backgrounds/first_street_scene.png'), 4),
                pygame.mask.from_surface(
                    ImgEditor.enhance_image(ImgEditor.load_image('first_street_scene/collisions.png'), 4)),
                settings.CENTER),
            'home_scene': HomeScene(ImgEditor.enhance_image(ImgEditor.load_image('/backgrounds/home_scene.png'), 4),
                                    pygame.mask.from_surface(
                                        ImgEditor.enhance_image(
                                            ImgEditor.load_image('home_scene/collisions.png'), 4)),
                                    settings.CENTER),
            'home_upscene': HomeUpScene(ImgEditor.enhance_image(ImgEditor.load_image('/backgrounds/home_upscene.png'), 4),
                                    pygame.mask.from_surface(
                                        ImgEditor.enhance_image(
                                            ImgEditor.load_image('home_upscene/collisions.png'), 4)),
                                    settings.CENTER)
        }
        settings.inventory = Inventory()
        settings.journal = Journal()
        self.sun = Sun()
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            delta_time = self.clock.tick() / 1000

            self.screen.fill('black')
            self.scenes[settings.scene].run(delta_time, events)

            self.screen.blit(settings.current_cursor, pygame.mouse.get_pos())
            settings.current_cursor = ImgEditor.enhance_image(ImgEditor.load_image('cursors/base_cursor.png'), 4)

            self.sun.display(delta_time)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
