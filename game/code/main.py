import pygame
import sys
import settings
from tools import ImgEditor
from menu import Menu
from first_street_scene import FirstStreetScene
from second_street_scene import SecondStreetScene
from home_scene import HomeScene
from home_upscene import HomeUpScene
from denis_room import DenisRoom
from artem_room import ArtemRoom
from inventory import Inventory
from journal import Journal
from achievements import Achieves
from menu_window import MenuWindow
from music import MusicPlayer
from environment import Sun
from dialogues import artem_dialogues


class Game:
    def __init__(self):
        # general
        pygame.init()
        pygame.display.set_caption(settings.NAME)
        pygame.display.set_icon(settings.ICON)

        # screen
        monitor = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.screen = pygame.display.set_mode(monitor, pygame.FULLSCREEN)

        # cursor
        settings.current_cursor = ImgEditor.load_image('cursors/base_cursor.png', settings.SCALE_K)
        pygame.mouse.set_visible(False)

        # scenes
        self.scenes = {
            'menu': Menu(),
            'first_street_scene': FirstStreetScene(
                ImgEditor.load_image('/backgrounds/first_street_scene.png', settings.SCALE_K),
                pygame.mask.from_surface(
                    ImgEditor.load_image('first_street_scene/collisions.png', settings.SCALE_K)),
                'street_day.mp3',
                settings.CENTER),
            'second_street_scene': SecondStreetScene(
                ImgEditor.load_image('/backgrounds/second_street_scene.png', settings.SCALE_K),
                pygame.mask.from_surface(
                    ImgEditor.load_image('second_street_scene/collisions.png', settings.SCALE_K)),
                'street_day.mp3',
                settings.CENTER),
            'home_scene': HomeScene(
                ImgEditor.load_image('/backgrounds/home_scene.png', settings.SCALE_K),
                pygame.mask.from_surface(
                    ImgEditor.load_image('home_scene/collisions.png', settings.SCALE_K)),
                'home_day.mp3',
                settings.CENTER),
            'home_upscene': HomeUpScene(
                ImgEditor.load_image('/backgrounds/home_upscene.png', settings.SCALE_K),
                pygame.mask.from_surface(
                    ImgEditor.load_image('home_upscene/collisions.png', settings.SCALE_K)),
                'home_day.mp3',
                settings.CENTER),
            'denis_room': DenisRoom(
                ImgEditor.load_image('/backgrounds/denis_room.png', settings.SCALE_K),
                pygame.mask.from_surface(
                    ImgEditor.load_image('denis_room/collisions.png', settings.SCALE_K)),
                'denis.mp3',
                settings.CENTER),
            'artem_room': ArtemRoom(
                ImgEditor.load_image('/backgrounds/artem_room.png', settings.SCALE_K),
                pygame.mask.from_surface(
                    ImgEditor.load_image('artem_room/collisions.png', settings.SCALE_K)),
                'artem.mp3',
                settings.CENTER)
        }
        settings.ADD_SOUND = pygame.mixer.Sound('..\\assets\\audio\\add.mp3')
        settings.inventory = Inventory()
        settings.journal = Journal()
        settings.achieves = Achieves()
        settings.menu_window = MenuWindow()
        settings.music_player = MusicPlayer()
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
            settings.current_cursor = ImgEditor.load_image('cursors/base_cursor.png', settings.SCALE_K)

            if 'menu' not in settings.scene:
                self.sun.display(delta_time)

            pygame.display.update()
            if settings.player == 'artem' and settings.inventory.artem_items['nut_chocolate'].count == 1 and \
                    settings.journal.artem_quests[4].is_showed:
                for talk in artem_dialogues['Джефф']:
                    for part in talk:
                        for line in part:
                            if line.id == 503:
                                line.unlock()

                            elif line.id == 501:
                                line.lock()




if __name__ == '__main__':
    game = Game()
    game.run()
