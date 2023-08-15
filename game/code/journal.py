import pygame
import settings
from overlay import Button
from tools import ImgEditor


class Journal:
    def __init__(self):
        self.quests = [
            Quest('Что происходит?', None, 'Расспросить Ксюшу'),
            Quest('Нужно полить цветы', ('drum stick', 1), 'Полить цветы', 'Вернуться к Артёму'),
            Quest('Потерянные палочки', ('money', 5), 'Найти барабанные палочки'),
            Quest('Дайте деняк', None, 'Одолжить Артёму 30 монет'),
            Quest('Таинственный торговец', ('drum stick', 1), 'Расспросить Артёма', 'Поговорить с Ксюшей',
                  'Вернуться к торговцу'),
        ]
        # general
        self.is_opened = False
        self.pages = 1
        self.current_page = 0
        self.quest_count = 0  # showed quests
        self.journal_group = pygame.sprite.Group()
        self.journal_background = ImgEditor.enhance_image(
            ImgEditor.load_image('overlay/journal_window.png', colorkey=-1), 4)

        # buttons
        self.back = Button(ImgEditor.enhance_image(ImgEditor.load_image('overlay/cross.png', colorkey=-1), 4),
                           (1190, 1440),
                           self.journal_group)
        self.left = Button(ImgEditor.enhance_image(ImgEditor.load_image('overlay/left.png', colorkey=-1), 4),
                           (1190, 1440),
                           self.journal_group)
        self.right = Button(ImgEditor.enhance_image(ImgEditor.load_image('overlay/right.png', colorkey=-1), 4),
                            (1190, 1440),
                            self.journal_group)
        self.journal_btn = Button(ImgEditor.enhance_image(ImgEditor.load_image('overlay/journal.png'), 4),
                                  (1490, 150),
                                  self.journal_group)

        # fonts
        self.font = pygame.font.Font(settings.FONT, 47)
        self.step_font = pygame.font.Font(settings.FONT, 40)

    def show_quest(self, id, coords, screen):
        quest = self.quests[id]
        # exclamation mark
        screen.blit(settings.QUEST_IMAGE, (coords[0], coords[1] - 10))
        # name
        screen.blit(self.font.render(quest.name, False, settings.TEXT_COLOR), (coords[0] + 60, coords[1] - 30))
        # step
        screen.blit(self.step_font.render(quest.steps[quest.current_step], False, settings.TEXT_COLOR),
                    (coords[0] + 60, coords[1] + 5))

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
            self.back.rect.center = (517, 1500)
            self.left.rect.center = (600, 1500)
            self.right.rect.center = (600, 1500)
        if self.journal_btn.is_clicked:
            if self.is_opened:
                self.back.rect.center = (517, 1500)
                self.left.rect.center = (600, 1500)
                self.right.rect.center = (600, 1500)
                self.is_opened = False
                self.current_page = 0
                settings.window_opened = False
            elif not settings.window_opened and not settings.dialogue_run:
                self.back.rect.center = (517, 200)
                self.left.rect.center = (740, 690)
                self.right.rect.center = (810, 690)
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
                        self.back.rect.center = (517, 1500)
                        self.left.rect.center = (600, 1500)
                        self.right.rect.center = (600, 1500)
                        self.is_opened = False
                        settings.window_opened = False
                    elif not settings.window_opened and not settings.dialogue_run:
                        self.back.rect.center = (517, 200)
                        self.left.rect.center = (740, 690)
                        self.right.rect.center = (810, 690)
                        self.is_opened = True
                        settings.window_opened = True
                        settings.new_quest = False

        self.journal_group.draw(screen)
        if settings.new_quest:
            screen.blit(settings.QUEST_IMAGE, (1430, 127))
        if self.is_opened:
            it = 0
            quest_it = 0
            for quest in self.quests:
                if self.current_page * 5 <= quest_it < (self.current_page + 1) * 5:
                    if quest.is_showed:
                        self.show_quest(it,
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
