import os
import sys
import pygame


class ImgEditor:
    @staticmethod
    def load_image(path, colorkey=None):
        fullname = '..\\assets\graphics\\' + path
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname)
        if colorkey is not None:
            # image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    @staticmethod
    def enhance_image(img, val):
        return pygame.transform.scale(img, (img.get_rect()[2] * val, img.get_rect()[3] * val))

    @staticmethod
    def cut_sheet(sheet, columns, rows):
        frames = []
        rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                           sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

        return frames

    @staticmethod
    def multiply_image(surface, color):
        new_image = surface.copy()
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                rr, gg, bb, a = surface.get_at((x, y))

                new_image.set_at((x, y), pygame.Color(rr * r // 255, gg * g // 255, bb * b // 255, a))
        return new_image


def blit_text(screen, pos, size, text, font, color, is_dialogue=(False, False)):
    words = text.split(' ')
    space = font.size(' ')[0]  # The width of a space.
    max_width = size
    pos = [*pos]
    x, y = pos
    if not is_dialogue[1] and len(text) * space >= max_width - x:  # tabulation on first line
        words[0] = ' ' + words[0]
    for word in words:
        word_surface = font.render(word, False, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            # start on a new row
            if is_dialogue[0]:  # if it's dialogue
                # diagonal end of line
                max_width -= 80
            if is_dialogue[1]:  # if it's base dialogue
                # diagonal beginning of line
                pos[0] -= 50
                # diagonal end of line (should be different)
                max_width -= 10

            x = pos[0]
            y += 40

        screen.blit(word_surface, (x, y))
        x += word_width + space
