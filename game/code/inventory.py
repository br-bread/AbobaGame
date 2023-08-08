import pygame
import settings
from overlay import Button
from tools import ImgEditor


class Inventory:
    def __init__(self):
        self.items = {
            'money': Item('Мелочь', 5, 'Несколько монет, лежащих в кармане',
                          ImgEditor.enhance_image(ImgEditor.load_image('item/money.png', colorkey=-1), 4)),
            'keyD': Item('Ключ', 1, 'Ключ от комнаты Дениса',
                         ImgEditor.enhance_image(ImgEditor.load_image('item/keyD.png', colorkey=-1), 4)),
            'candy': Item('Конфета', 0, 'В её честь даже назвали собаку!',
                          ImgEditor.enhance_image(ImgEditor.load_image('item/candy.png', colorkey=-1), 4)),
            'chocolate': Item('Шоколадка', 0, 'Плитка молочного шоколада',
                              ImgEditor.enhance_image(ImgEditor.load_image('item/chocolate.png', colorkey=-1), 4))
        }
        self.is_opened = False
        self.inventory_group = pygame.sprite.Group()
        self.back = Button(ImgEditor.enhance_image(ImgEditor.load_image('overlay/cross.png', colorkey=-1), 4),
                           (1190, 1440),
                           self.inventory_group)
        self.inventory_background = ImgEditor.enhance_image(
            ImgEditor.load_image('overlay/inventory_window.png', colorkey=-1), 4)
        self.font = pygame.font.Font(settings.FONT, 47)
        self.description_font = pygame.font.Font(settings.FONT, 40)

    def show_item(self, name, coords, screen):
        item = self.items[name]
        # image
        screen.blit(item.image, coords)
        # name
        screen.blit(self.font.render(item.name, False, settings.TEXT_COLOR), (coords[0] + 80, coords[1] - 20))
        # count
        screen.blit(self.font.render('x' + str(item.count), False, settings.TEXT_COLOR),
                    (coords[0] + 475, coords[1] - 20))
        # description
        screen.blit(self.description_font.render(item.description, False, settings.TEXT_COLOR),
                    (coords[0] + 80, coords[1] + 16))

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
        if self.is_opened:
            it = 0
            for key, val in self.items.items():
                if val.count > 0:
                    self.show_item(key,
                                   (settings.ITEM_COORDS[0],
                                    settings.ITEM_COORDS[1] + it * settings.ITEM_OFFSET), screen)
                    it += 1
        self.inventory_group.update(dt, events)


class Item:
    def __init__(self, name, count, description='', img=None):
        self.name = name
        self.count = count
        self.description = description
        self.image = img

    def add(self, count=1):
        self.count += count

    def remove(self, count=1):
        self.count -= count
