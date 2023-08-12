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
        if self.is_opened:
            screen.blit(self.journal_background,
                        (settings.CENTER[0] - self.journal_background.get_width() // 2,
                         settings.CENTER[1] - self.journal_background.get_height() // 2))
        if self.back.is_clicked:
            settings.window_opened = False
            self.is_opened = False
            self.back.rect.center = (517, 1500)
            self.left.rect.center = (600, 1500)
            self.right.rect.center = (600, 1500)
        if self.journal_btn.is_clicked:
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
            for quest in self.quests:
                if quest.is_showed:
                    self.show_quest(it,
                                    (settings.QUEST_COORDS[0],
                                     settings.QUEST_COORDS[1] + it * settings.QUEST_OFFSET), screen)
                    it += 1
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
