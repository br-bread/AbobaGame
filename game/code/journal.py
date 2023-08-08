import pygame
import settings
from overlay import Button
from tools import ImgEditor


class Journal:
    def __init__(self):
        self.quests = {
        }
        self.is_opened = False
        self.journal_group = pygame.sprite.Group()
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
        self.journal_background = ImgEditor.enhance_image(
            ImgEditor.load_image('overlay/inventory_window.png', colorkey=-1), 4)
        self.font = pygame.font.Font(settings.FONT, 47)
        self.description_font = pygame.font.Font(settings.FONT, 40)

    def show_quest(self, name, coords, screen):
        quest = self.quests[name]
        # name
        # screen.blit(self.font.render(item.name, False, settings.TEXT_COLOR), (coords[0] + 80, coords[1] - 20))

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
            elif not settings.window_opened:
                self.back.rect.center = (517, 200)
                self.left.rect.center = (740, 690)
                self.right.rect.center = (810, 690)
                self.is_opened = True
                settings.window_opened = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    if self.is_opened:
                        self.back.rect.center = (517, 1500)
                        self.left.rect.center = (600, 1500)
                        self.right.rect.center = (600, 1500)
                        self.is_opened = False
                        settings.window_opened = False
                    elif not settings.window_opened:
                        self.back.rect.center = (517, 200)
                        self.left.rect.center = (740, 690)
                        self.right.rect.center = (810, 690)
                        self.is_opened = True
                        settings.window_opened = True

        self.journal_group.draw(screen)
        if self.is_opened:
            it = 0
            for key, val in self.quests.items():
                if val.count > 0:
                    self.show_quest(key,
                                    (settings.ITEM_COORDS[0],
                                     settings.ITEM_COORDS[1] + it * settings.ITEM_OFFSET), screen)
                    it += 1
        self.journal_group.update(dt, events)


class Quest:
    def __init__(self, name, reward, *steps):
        self.name = name
        self.reward = reward
        self.steps = steps
        self.current_step = 0
        self.is_showed = 0
        self.is_done = 0

    def next_step(self):
        self.current_step += 1
