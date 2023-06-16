import pygame
from random import choice


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos, *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect(center=pos)


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
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.background = BaseSprite(background, background_pos, self.visible_sprites)

    def run(self, delta_time):
        self.visible_sprites.draw(self.screen)
        self.visible_sprites.update(delta_time)
