import pygame
import settings
from tools import ImgEditor


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
