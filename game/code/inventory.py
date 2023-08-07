import pygame
import settings
from overlay import Button
from tools import ImgEditor


class Inventory:
    def __init__(self):
        self.items = {
            'money': Item('Мелочь', 5, 'Несколько монет, лежащих в кармане'),
            'keyD': Item('Ключ', 1, 'Ключ от комнаты Дениса'),
            'candy': Item('Конфета', 0, 'Довольно вкусная'),
            'chocolate': Item('Шоколадка', 0, 'Стандартная плитка молочного шоколада')
        }
        self.is_opened = False
        self.inventory_group = pygame.sprite.Group()
        self.back = Button(ImgEditor.enhance_image(ImgEditor.load_image('overlay/cross.png', colorkey=-1), 4),
                           (1190, 1440),
                           self.inventory_group)
        self.inventory_background = ImgEditor.enhance_image(
            ImgEditor.load_image('overlay/inventory_window.png', colorkey=-1), 4)

    def run(self, screen, dt, events):
        if self.is_opened:
            screen.blit(self.inventory_background,
                        (settings.CENTER[0] - self.inventory_background.get_width() // 2,
                         settings.CENTER[1] - self.inventory_background.get_height() // 2))
        if self.back.is_clicked:
            settings.window_opened = False
            self.is_opened = False
            self.back.rect.center = (517, 1500)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.is_opened:
                        self.back.rect.center = (517, 1500)
                        self.is_opened = False
                        settings.window_opened = False
                    else:
                        self.back.rect.center = (517, 200)
                        self.is_opened = True
                        settings.window_opened = True

        self.inventory_group.draw(screen)
        self.inventory_group.update(dt, events)


class Item:
    def __init__(self, name, count, description='', img=None):
        self.name = name
        self.count = count
        self.description = description
        self.img = img

    def add(self, count=1):
        self.count += count

    def remove(self, count=1):
        self.count -= count


inventory = Inventory()
