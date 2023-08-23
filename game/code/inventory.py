import pygame
import settings
from overlay import Button
from tools import ImgEditor


class Inventory:
    def __init__(self):
        self.items = {
            'money': Item('Мелочь', 5, 'Несколько монет, лежащих в кармане',
                          ImgEditor.load_image('item/money.png', settings.SCALE_K, colorkey=-1)),
            'keyD': Item('Ключ', 1, 'Ключ от комнаты Дениса',
                         ImgEditor.load_image('item/keyD.png', settings.SCALE_K, colorkey=-1)),
            'candy': Item('Конфета', 0, 'В её честь даже назвали собаку!',
                          ImgEditor.load_image('item/candy.png', settings.SCALE_K, colorkey=-1)),
            'chocolate': Item('Шоколадка', 0, 'Плитка молочного шоколада',
                              ImgEditor.load_image('item/chocolate.png', settings.SCALE_K, colorkey=-1)),
            'drum stick': Item('Барабанная палочка', 0, 'От одной маловато толку',
                               ImgEditor.load_image('item/chocolate.png', settings.SCALE_K, colorkey=-1)),
        }
        self.is_opened = False
        self.pages = 1
        self.current_page = 0
        self.item_count = 1  # items in inventory which count > 0
        self.inventory_group = pygame.sprite.Group()

        # buttons
        self.back = Button(ImgEditor.load_image('overlay/cross.png', settings.SCALE_K, colorkey=-1),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.inventory_group)
        self.left = Button(ImgEditor.load_image('overlay/left.png', settings.SCALE_K, colorkey=-1),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.inventory_group)
        self.right = Button(ImgEditor.load_image('overlay/right.png', settings.SCALE_K, colorkey=-1),
                            (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                            self.inventory_group)
        self.inventory_btn = Button(ImgEditor.load_image('overlay/inventory.png', settings.SCALE_K),
                                    (373 * settings.SCALE_K, 24 * settings.SCALE_K),
                                    self.inventory_group)

        self.inventory_background = ImgEditor.load_image('overlay/inventory_window.png', settings.SCALE_K, colorkey=-1)

        # fonts
        self.font = pygame.font.Font(settings.FONT, 12 * settings.SCALE_K)
        self.description_font = pygame.font.Font(settings.FONT, 10 * settings.SCALE_K)

    def show_item(self, name, coords, screen):
        item = self.items[name]
        # image
        screen.blit(item.image, coords)
        # name
        screen.blit(self.font.render(item.name, False, settings.TEXT_COLOR),
                    (coords[0] + 20 * settings.SCALE_K, coords[1] - 5 * settings.SCALE_K))
        # count
        screen.blit(self.font.render('x' + str(item.count), False, settings.TEXT_COLOR),
                    (coords[0] + 119 * settings.SCALE_K, coords[1] - 5 * settings.SCALE_K))
        # description
        screen.blit(self.description_font.render(item.description, False, settings.TEXT_COLOR),
                    (coords[0] + 20 * settings.SCALE_K, coords[1] + 4 * settings.SCALE_K))

    def run(self, screen, dt, events):
        self.pages = self.item_count // 5 + bool(self.item_count % 5)
        if self.is_opened:
            screen.blit(self.inventory_background,
                        (settings.CENTER[0] - self.inventory_background.get_width() // 2,
                         settings.CENTER[1] - self.inventory_background.get_height() // 2))
        if self.back.is_clicked:
            settings.window_opened = False
            self.is_opened = False
            self.current_page = 0
            self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.left.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.right.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
        if self.inventory_btn.is_clicked:
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
                if event.key == pygame.K_i:
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

        self.inventory_group.draw(screen)
        if self.is_opened:
            it = 0
            item = 0
            for key, val in self.items.items():
                if self.current_page * 5 <= item < (self.current_page + 1) * 5:
                    if val.count > 0:
                        self.show_item(key,
                                       (settings.ITEM_COORDS[0],
                                        settings.ITEM_COORDS[1] + it * settings.ITEM_OFFSET), screen)
                        it += 1
                item += 1
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
        if self.count < 0:
            self.count = 0
