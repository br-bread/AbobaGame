import pygame
from random import choice
import settings
from tools import ImgEditor


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect(center=pos)
        self.game_layer = layer

    def is_mouse_on(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        if self.rect.x + self.rect[2] >= pos_x >= self.rect.x and self.rect.y + self.rect[3] >= pos_y >= self.rect.y:
            return True
        else:
            return False

    def update(self, *args, **kwargs):
        if self.is_mouse_on():
            settings.current_cursor = ImgEditor.enhance_image(ImgEditor.load_image('cursors/magnifier_cursor.png'), 4)


class InteractiveSprite(BaseSprite):
    def __init__(self, name, img, pos, *groups):
        super().__init__(img, pos, *groups)
        self.name = name
        self.description = choice([f"Это {name}.", f"Это просто {name}.", f"Выглядит как {name}.",
                                   f"Это {name}, ничего интересного.", f"{name.capitalize()}."])
        self.cursor_image = ""


class BaseScene:
    def __init__(self, background, background_pos=(0, 0)):
        self.screen = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.background = BaseSprite(background, background_pos, settings.LAYERS['background'])

    def run(self, delta_time):
        self.screen.blit(self.background.image, self.background.rect)
        self.visible_sprites.draw_sprites()
        self.visible_sprites.update(delta_time)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.screen = pygame.display.get_surface()

    def draw_sprites(self):
        for layer in settings.LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                if sprite.game_layer == layer:
                    self.screen.blit(sprite.image, sprite.rect)
