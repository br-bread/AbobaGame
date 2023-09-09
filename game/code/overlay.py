import pygame
import sys
import settings
from tools import ImgEditor
from saving_manager import SavingManager


class Daytime:
    time_board = ImgEditor.load_image('overlay/time_board.png', settings.SCALE_K, colorkey=-1)

    @staticmethod
    def run(screen):
        hours = int(settings.time['hours'])
        if hours < 10:
            hours = '0' + str(hours)
        minutes = int(settings.time['minutes'])
        curr_time = str(hours) + ':' + str(minutes) + '0'
        time_surf = pygame.font.Font(settings.FONT, 16 * settings.SCALE_K).render(curr_time, False, settings.TEXT_COLOR)
        screen.blit(Daytime.time_board, settings.TIME_BOARD_COORDS)
        screen.blit(time_surf, settings.TIME_COORDS)


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
            scene.disappear('menu', scene.player.pos, 'down_idle')
        if self.exit.is_clicked:
            pygame.quit()
            sys.exit()
        self.overlay_group.update(dt, events)
        self.overlay_group.draw(screen)


class Button(pygame.sprite.Sprite):
    def __init__(self, img, pos, *groups):
        super().__init__(*groups)
        self.true_image = img
        self.pressed_image = ImgEditor.multiply_image(self.true_image, (185, 166, 161))  # darker image
        self.image = self.true_image

        self.rect = self.image.get_rect(center=pos)
        self.is_clicked = False  # mouse up
        self.is_pressed = False  # mouse down
        self.cursor_image = 'pointer_cursor.png'
        self.sound = pygame.mixer.Sound('..\\assets\\audio\\button.mp3')

    def is_mouse_on(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        if self.rect.x + self.rect[2] >= pos_x >= self.rect.x and self.rect.y + self.rect[3] >= pos_y >= self.rect.y:
            return True
        else:
            return False

    def change_image(self, image):
        self.true_image = image
        self.pressed_image = ImgEditor.multiply_image(self.true_image, (185, 166, 161))
        self.image = self.true_image

    def update(self, dt, events):
        self.is_clicked = False
        if self.is_mouse_on():
            settings.current_cursor = ImgEditor.load_image(f'cursors/{self.cursor_image}', settings.SCALE_K - 2)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_on() and not self.is_pressed:
                self.is_pressed = True
                self.sound.play()
            if event.type == pygame.MOUSEBUTTONUP and self.is_pressed:
                self.is_pressed = False
                self.is_clicked = True
        if self.is_pressed:
            self.image = self.pressed_image
        else:
            self.image = self.true_image
