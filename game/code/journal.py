import pygame
import settings
from overlay import Button
from tools import ImgEditor


class Journal:
    def __init__(self):
        self.quests = [
            Quest('Что происходит?', None, 'Расспросить Ксюшу'),
            Quest('Комната Дениса', None, 'Найти ключ'),
        ]
        # general
        self.is_opened = False
        self.pages = 1
        self.current_page = 0
        self.quest_count = 0  # showed quests
        self.journal_group = pygame.sprite.Group()
        self.journal_background = ImgEditor.load_image('overlay/journal_window.png', settings.SCALE_K, colorkey=-1)

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
        quest = self.quests[id]
        # exclamation mark
        screen.blit(settings.QUEST_IMAGE, (coords[0], coords[1] - 3 * settings.SCALE_K))
        # name
        screen.blit(self.font.render(quest.name, False, settings.TEXT_COLOR),
                    (coords[0] + 16 * settings.SCALE_K, coords[1] - 8 * settings.SCALE_K))
        # step
        screen.blit(self.step_font.render(quest.steps[quest.current_step], False, settings.TEXT_COLOR),
                    (coords[0] + 16 * settings.SCALE_K, coords[1] + 1 * settings.SCALE_K))

    def run(self, screen, dt, events):
        self.pages = self.quest_count // 5 + bool(self.quest_count % 5)
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
                settings.new_quest = False

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
                        settings.new_quest = False

        self.journal_group.draw(screen)
        if settings.new_quest:
            screen.blit(settings.QUEST_IMAGE, (358 * settings.SCALE_K, 32 * settings.SCALE_K))
        if self.is_opened:
            it = 0
            quest_it = 0
            for quest in self.quests:
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
        self.is_done = False

    def next_step(self):
        self.current_step += 1

    def unlock(self):
        self.is_showed = True

    def lock(self):
        self.is_showed = False
