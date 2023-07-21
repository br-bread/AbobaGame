from core import InteractiveSprite
from dialogues import Dialogue, DialogueLine
import settings
import pygame


class DialogueSprite(InteractiveSprite):
    def __init__(self, name, img, pos, layer, *groups):
        super().__init__(img, pos, layer, *groups)
        # general
        self.name = name
        self.cursor_image = 'magnifier_cursor.png'
        # dialogue
        description = [DialogueLine('base', f'Это {name}.'),
                       DialogueLine('base', f'Это просто {name}.'),
                       DialogueLine('base', f'Выглядит как {name}.'),
                       DialogueLine('base', f'Это {name}, ничего интересного.'),
                       DialogueLine('base', f'{name.capitalize()}.')]
        self.dialogue = Dialogue(self.name, groups[0], description)

    def update(self, dt, player_pos, events, screen, *args, **kwargs):
        super().update(dt, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_on():
                        self.dialogue.run(is_mouse_on=True)
                    else:
                        self.dialogue.run(is_mouse_on=False)

        self.dialogue.update(dt, screen)


class Door(InteractiveSprite):
    def __init__(self, img, pos, layer, scene, next_scene, *groups):
        super().__init__(img, pos, layer, *groups)
        self.cursor_image = 'arrow_cursor.png'
        self.next_scene = next_scene
        self.scene = scene

    def update(self, dt, player_pos, events, *args, **kwargs):
        super().update(dt, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_on():
                        self.scene.disappear(self.next_scene)
