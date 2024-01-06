import pygame
import settings
from overlay import Button
from tools import ImgEditor
from core import BaseAnimatedSprite


class Journal:
    def __init__(self):
        self.artem_quests = [
            Quest('Комната Артёма', None, 'Найти ключ'),
            Quest('Ты проставляешься', None, 'Найти еду'),
            Quest('И попить', None, 'Найти попить'),
            Quest('Генеральная уборка', None, 'Собрать все носки в доме'),
            Quest('Шоколад для Джесс', 'money 15', 'Найти ореховый шоколад'),
        ]
        self.denis_quests = [
            Quest('Комната Дениса', None, 'Найти ключ'),
        ]
        denis_quest_locks = settings.saving_manager.load_data('denis_journal_locks', [False])
        for i in range(len(self.denis_quests)):
            self.denis_quests[i].is_showed = denis_quest_locks[i]

        artem_quest_locks = settings.saving_manager.load_data('artem_journal_locks',
                                                              [False, False, False, False, False])
        for i in range(len(self.artem_quests)):
            self.artem_quests[i].is_showed = artem_quest_locks[i]

        denis_quest_steps = settings.saving_manager.load_data('denis_journal_steps', [0])
        for i in range(len(self.denis_quests)):
            self.denis_quests[i].current_step = denis_quest_steps[i]

        artem_quest_steps = settings.saving_manager.load_data('artem_journal_steps', [0, 0, 0, 0, 0])
        for i in range(len(self.artem_quests)):
            self.artem_quests[i].current_step = artem_quest_steps[i]

        # general
        self.is_opened = False
        self.pages = 1
        self.current_page = 0

        self.denis_quest_count = 0  # showed quests
        for i in self.denis_quests:
            if i.is_showed:
                self.denis_quest_count += 1

        self.artem_quest_count = 0  # showed quests
        for i in self.artem_quests:
            if i.is_showed:
                self.artem_quest_count += 1

        self.journal_group = pygame.sprite.Group()
        self.journal_background = ImgEditor.load_image('overlay/journal_window.png', settings.SCALE_K, colorkey=-1)

        self.new_quest = BaseAnimatedSprite(ImgEditor.load_image('overlay/exclamation_mark.png', settings.SCALE_K),
                                            (363 * settings.SCALE_K, 37 * settings.SCALE_K),
                                            3, 2, 1, settings.LAYERS['overlay'], self.journal_group)

        # buttons
        self.back = Button(ImgEditor.load_image('overlay/cross.png', settings.SCALE_K, colorkey=-1),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.journal_group)
        self.left = Button(ImgEditor.load_image('overlay/left.png', settings.SCALE_K, colorkey=-1),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.journal_group)
        self.right = Button(ImgEditor.load_image('overlay/right.png', settings.SCALE_K, colorkey=-1),
                            (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                            self.journal_group)
        self.journal_btn = Button(ImgEditor.load_image('overlay/journal.png', settings.SCALE_K),
                                  (373 * settings.SCALE_K, 38 * settings.SCALE_K),
                                  self.journal_group)

        # fonts
        self.font = pygame.font.Font(settings.FONT, 12 * settings.SCALE_K)
        self.step_font = pygame.font.Font(settings.FONT, 10 * settings.SCALE_K)

    def show_quest(self, id, coords, screen):
        if settings.player == 'denis':
            quests = self.denis_quests
        else:
            quests = self.artem_quests
        quest = quests[id]
        # exclamation mark
        screen.blit(settings.QUEST_IMAGE, (coords[0], coords[1] - 3 * settings.SCALE_K))
        # name
        screen.blit(self.font.render(quest.name, False, settings.TEXT_COLOR),
                    (coords[0] + 16 * settings.SCALE_K, coords[1] - 8 * settings.SCALE_K))
        # step
        screen.blit(self.step_font.render(quest.steps[quest.current_step], False, settings.TEXT_COLOR),
                    (coords[0] + 16 * settings.SCALE_K, coords[1] + 1 * settings.SCALE_K))

    def run(self, screen, dt, events):
        if settings.cleaned_socks == 7 and self.artem_quests[3].is_showed:
            settings.journal.artem_quests[3].lock()
            settings.journal.artem_quest_count -= 1
            if settings.journal.artem_quest_count == 0:
                settings.artem_new_quest = False
        if settings.player == 'artem':
            self.pages = self.artem_quest_count // 5 + bool(self.artem_quest_count % 5)
        else:
            self.pages = self.denis_quest_count // 5 + bool(self.denis_quest_count % 5)
        if self.is_opened:
            screen.blit(self.journal_background,
                        (settings.CENTER[0] - self.journal_background.get_width() // 2,
                         settings.CENTER[1] - self.journal_background.get_height() // 2))
        if self.back.is_clicked:
            settings.window_opened = False
            self.is_opened = False
            self.current_page = 0
            self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.left.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.right.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
        if self.journal_btn.is_clicked:
            if self.is_opened:
                self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
                self.left.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
                self.right.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
                self.is_opened = False
                self.current_page = 0
                settings.window_opened = False
            elif not settings.window_opened and not settings.dialogue_run:
                self.back.rect.center = (129 * settings.SCALE_K, 50 * settings.SCALE_K)
                self.left.rect.center = (185 * settings.SCALE_K, 173 * settings.SCALE_K)
                self.right.rect.center = (203 * settings.SCALE_K, 173 * settings.SCALE_K)
                self.is_opened = True
                settings.window_opened = True
                if settings.player == 'artem':
                    settings.artem_new_quest = False
                else:
                    settings.denis_new_quest = False

        if self.right.is_clicked:
            self.current_page += 1
            if self.current_page > self.pages - 1:
                self.current_page = self.pages - 1
        if self.left.is_clicked:
            self.current_page -= 1
            if self.current_page < 0:
                self.current_page = 0

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    if self.is_opened:
                        self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
                        self.left.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
                        self.right.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
                        self.is_opened = False
                        settings.window_opened = False
                    elif not settings.window_opened and not settings.dialogue_run:
                        self.back.rect.center = (129 * settings.SCALE_K, 50 * settings.SCALE_K)
                        self.left.rect.center = (185 * settings.SCALE_K, 173 * settings.SCALE_K)
                        self.right.rect.center = (203 * settings.SCALE_K, 173 * settings.SCALE_K)
                        self.is_opened = True
                        settings.window_opened = True
                        if settings.player == 'artem':
                            settings.artem_new_quest = False
                        else:
                            settings.denis_new_quest = False

        self.journal_group.draw(screen)
        if (settings.denis_new_quest and settings.player == 'denis') or (
                settings.artem_new_quest and settings.player == 'artem'):
            self.new_quest.add(self.journal_group)
        else:
            self.new_quest.kill()

        if self.is_opened:
            it = 0
            quest_it = 0
            if settings.player == 'denis':
                quests = self.denis_quests
            else:
                quests = self.artem_quests
            for quest in quests:
                if self.current_page * 5 <= quest_it < (self.current_page + 1) * 5:
                    if quest.is_showed:
                        self.show_quest(quest_it,
                                        (settings.QUEST_COORDS[0],
                                         settings.QUEST_COORDS[1] + it * settings.QUEST_OFFSET), screen)
                        it += 1
                quest_it += 1
        self.journal_group.update(dt, events)


class Quest:
    def __init__(self, name, reward, *steps):
        self.name = name
        self.reward = reward
        self.steps = steps
        self.current_step = 0
        self.is_showed = False

    def next_step(self):
        self.current_step += 1

    def unlock(self):
        self.is_showed = True

    def lock(self):
        self.is_showed = False
        if self.name == 'Ты проставляешься' or self.name == 'И попить':
            settings.finished_quests += 1
