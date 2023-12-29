import pygame
import settings
from overlay import Button
from tools import ImgEditor
from core import BaseAnimatedSprite


class Achieves:
    def __init__(self):
        self.achieves = [Achievement('Долой носки', 'Убрать все носки', 3),
                         Achievement('Ты проставляешься', 'Найти еду для праздника', 3),
                         Achievement('Орехи', 'Принести Джеффу шоколадку', 0),
                         Achievement('Харизма', 'Пообщаться со всеми персонажами', 5),
                         Achievement('Микро-путешествие', 'Побывать во всех игровых локациях', 5),
                         Achievement('Пиксель-хантер', 'Осмотреть все предметы', 10),
                         Achievement('18+', 'Украсть яблочный сидр', 3),
                         Achievement('Секретная локация', 'Попасть в комнату Ксюши', 5),
                         Achievement('И жили они долго и счастливо', 'Встретить Яну с Артёмом', 3)]
        achieves_locks = settings.saving_manager.load_data('achieves',
                                                           [True, True, True, True, True, True, True, True, True])
        for i in range(len(self.achieves)):
            self.achieves[i].is_locked = achieves_locks[i]
            if self.achieves[i].cost == 3:
                self.achieves[i].description += f' ({self.achieves[i].cost} монеты)'
            else:
                self.achieves[i].description += f' ({self.achieves[i].cost} монет)'

        self.is_opened = False
        self.pages = 1
        self.current_page = 0
        self.achieve_count = len(self.achieves)
        self.achieves_group = pygame.sprite.Group()

        self.new_achieve = BaseAnimatedSprite(ImgEditor.load_image('overlay/exclamation_mark.png', settings.SCALE_K),
                                              (363 * settings.SCALE_K, 52 * settings.SCALE_K),
                                              3, 2, 1, settings.LAYERS['overlay'], self.achieves_group)

        # buttons
        self.back = Button(ImgEditor.load_image('overlay/cross.png', settings.SCALE_K, colorkey=-1),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.achieves_group)
        self.left = Button(ImgEditor.load_image('overlay/left.png', settings.SCALE_K, colorkey=-1),
                           (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                           self.achieves_group)
        self.right = Button(ImgEditor.load_image('overlay/right.png', settings.SCALE_K, colorkey=-1),
                            (373 * settings.SCALE_K, 360 * settings.SCALE_K),
                            self.achieves_group)
        self.achieves_btn = Button(ImgEditor.load_image('overlay/achieves.png', settings.SCALE_K),
                                   (373 * settings.SCALE_K, 52 * settings.SCALE_K),
                                   self.achieves_group)

        self.achieves_background = ImgEditor.load_image('overlay/achieves_window.png', settings.SCALE_K, colorkey=-1)

        # fonts
        self.font = pygame.font.Font(settings.FONT, 12 * settings.SCALE_K)
        self.description_font = pygame.font.Font(settings.FONT, 10 * settings.SCALE_K)

    def show_achieve(self, id, coords, is_locked, screen):
        achieve = self.achieves[id]
        # achievement icon
        if not is_locked:
            screen.blit(settings.ACHIEVE_IMAGE, (coords[0], coords[1] - 3 * settings.SCALE_K))
        else:
            screen.blit(settings.LOCKED_ACHIEVE_IMAGE, (coords[0], coords[1] - 3 * settings.SCALE_K))
        # name
        screen.blit(self.font.render(achieve.name, False, settings.TEXT_COLOR),
                    (coords[0] + 20 * settings.SCALE_K, coords[1] - 8 * settings.SCALE_K))
        # description
        if not is_locked:
            screen.blit(self.description_font.render(achieve.description, False, settings.TEXT_COLOR),
                        (coords[0] + 20 * settings.SCALE_K, coords[1] + 1 * settings.SCALE_K))

    def run(self, screen, dt, events):
        if settings.talked_characters == 5 and self.achieves[3].is_locked:
            self.achieves[3].unlock()
            self.achieve_count += 1
            settings.new_achieve = True
            settings.ADD_SOUND.play()
        if settings.seen_objects == 41 and self.achieves[5].is_locked:
            self.achieves[5].unlock()
            self.achieve_count += 1
            settings.new_achieve = True
            settings.ADD_SOUND.play()
        if settings.visited_scenes == 6 and self.achieves[4].is_locked:
            self.achieves[4].unlock()
            self.achieve_count += 1
            settings.new_achieve = True
            settings.ADD_SOUND.play()
        self.pages = self.achieve_count // 5 + bool(self.achieve_count % 5)
        if self.is_opened:
            screen.blit(self.achieves_background,
                        (settings.CENTER[0] - self.achieves_background.get_width() // 2,
                         settings.CENTER[1] - self.achieves_background.get_height() // 2))
        if self.back.is_clicked:
            settings.window_opened = False
            self.is_opened = False
            self.current_page = 0
            self.back.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.left.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
            self.right.rect.center = (373 * settings.SCALE_K, 360 * settings.SCALE_K)
        if self.achieves_btn.is_clicked:
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
                settings.new_achieve = False
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
                if event.key == pygame.K_k:
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
                        settings.new_achieve = False
                        settings.window_opened = True

        self.achieves_group.draw(screen)
        if settings.new_achieve:
            self.new_achieve.add(self.achieves_group)
        else:
            self.new_achieve.kill()

        if self.is_opened:
            it = 0
            achieve_it = 0
            for achieve in self.achieves:
                if self.current_page * 5 <= achieve_it < (self.current_page + 1) * 5:
                    if not achieve.is_locked:
                        self.show_achieve(achieve_it,
                                          (settings.ACHIEVE_COORDS[0],
                                           settings.ACHIEVE_COORDS[1] + it * settings.ACHIEVE_OFFSET), False, screen)
                        it += 1
                achieve_it += 1
            achieve_it = 0
            for achieve in self.achieves:
                if self.current_page * 5 <= achieve_it < (self.current_page + 1) * 5:
                    if achieve.is_locked:
                        self.show_achieve(achieve_it,
                                          (settings.ACHIEVE_COORDS[0],
                                           settings.ACHIEVE_COORDS[1] + it * settings.ACHIEVE_OFFSET), True, screen)
                        it += 1
                achieve_it += 1

        self.achieves_group.update(dt, events)


class Achievement:
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost
        self.is_locked = False

    def unlock(self):
        self.is_locked = False
        settings.inventory.artem_items['money'].add(self.cost)

    def lock(self):
        self.is_locked = True
