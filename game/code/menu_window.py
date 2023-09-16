import pygame
import sys
import settings
from overlay import Button
from tools import ImgEditor
from saving_manager import SavingManager
from dialogues import denis_dialogues, artem_dialogues


class MenuWindow:
    def __init__(self):
        self.overlay_group = pygame.sprite.Group()
        self.menu = Button(ImgEditor.load_image('overlay/menu.png', settings.SCALE_K),
                           (373 * settings.SCALE_K, 10 * settings.SCALE_K),
                           self.overlay_group)
        self.back = Button(ImgEditor.load_image('overlay/cross.png', settings.SCALE_K),
                           (298 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.overlay_group)
        self.main_menu = Button(ImgEditor.load_image('overlay/main_menu.png', settings.SCALE_K),
                                (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                                self.overlay_group)
        self.exit = Button(ImgEditor.load_image('overlay/exit.png', settings.SCALE_K),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.overlay_group)
        self.save = Button(ImgEditor.load_image('overlay/save.png', settings.SCALE_K),
                           (373 * settings.SCALE_K, 370 * settings.SCALE_K),
                           self.overlay_group)

        self.saving_manager = SavingManager()

        self.menu_background = ImgEditor.load_image('overlay/menu_window.png', settings.SCALE_K, colorkey=-1)
        self.is_opened = False

    def run(self, screen, dt, events, scene):
        if self.is_opened:
            screen.blit(self.menu_background,
                        (settings.CENTER[0] - self.menu_background.get_width() // 2,
                         settings.CENTER[1] - self.menu_background.get_height() // 2))

        if self.menu.is_clicked and not settings.window_opened and not settings.dialogue_run:
            settings.window_opened = True
            self.is_opened = True
            self.back.rect.center = (140 * settings.SCALE_K, 75 * settings.SCALE_K)
            self.main_menu.rect.center = (193 * settings.SCALE_K, 90 * settings.SCALE_K)
            self.exit.rect.center = (193 * settings.SCALE_K, 130 * settings.SCALE_K)
            self.save.rect.center = (193 * settings.SCALE_K, 110 * settings.SCALE_K)

        if self.back.is_clicked:
            settings.window_opened = False
            self.is_opened = False
            self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.main_menu.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.exit.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.save.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)

        if self.main_menu.is_clicked:
            self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.main_menu.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.exit.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.save.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            settings.window_opened = False
            self.is_opened = False
            settings.next_music = settings.music_player.music_name
            scene.disappear('menu', 'menu.mp3', scene.player.pos, 'down_idle')

        if self.exit.is_clicked:
            pygame.quit()
            sys.exit()

        if self.save.is_clicked:
            self.saving_manager.save_game_data([
                settings.time, settings.time_color, settings.next_time,
                settings.denis_new_quest, settings.artem_new_quest,
                [i.is_showed for i in settings.journal.denis_quests],
                [i.current_step for i in settings.journal.denis_quests],
                [i.is_showed for i in settings.journal.artem_quests],
                [i.current_step for i in settings.journal.artem_quests],
                settings.new_achieve,
                'menu', settings.scene,
                scene.player.pos.xy, settings.music_player.music_name,
                [v.count for k, v in settings.inventory.artem_items.items()],
                [v.count for k, v in settings.inventory.denis_items.items()],
                [i.is_locked for i in settings.achieves.achieves],
                denis_dialogues, artem_dialogues],
                ['time', 'time_color', 'next_time_index',
                 'denis_new_quest', 'artem_new_quest',
                 'denis_journal_locks', 'denis_journal_steps',
                 'artem_journal_locks', 'artem_journal_steps',
                 'new_achieve', 'scene', 'previous_scene',
                 'player_pos', 'next_music',
                 'artem_inventory', 'denis_inventory',
                 'achieves', 'denis_dialogues', 'artem_dialogues'])

        self.overlay_group.update(dt, events)
        self.overlay_group.draw(screen)
