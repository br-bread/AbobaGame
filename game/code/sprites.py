from core import BaseSprite, InteractiveSprite, Dialogue
from random import choice
import settings
import pygame


class DialogueSprite(InteractiveSprite):
    def __init__(self, name, img, pos, layer, *groups):
        super().__init__(img, pos, layer, *groups)
        # general
        self.name = name
        self.cursor_image = 'magnifier_cursor.png'
        # dialogue
        description = choice([f"base_Это {name}.", f"base_Это просто {name}.", f"base_Выглядит как {name}.",
                              f"base_Это {name}, ничего интересного.", f"base_{name.capitalize()}."])
        self.dialogue = Dialogue(groups[0], description, *settings.DIALOGUES[name])

    def update(self, dt, player_pos, events, screen, *args, **kwargs):
        super().update(dt, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_on():
                        self.dialogue.run(is_mouse_on=True)
                    else:
                        self.dialogue.run(is_mouse_on=False)

        self.dialogue.animate(dt, screen)


class Door(InteractiveSprite):
    def __init__(self, img, pos, layer, next_scene, *groups):
        super().__init__(img, pos, layer, *groups)
        self.cursor_image = 'arrow_cursor.png'
        self.next_scene = next_scene

    def update(self, dt, player_pos, events, *args, **kwargs):
        super().update(dt, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_on():
                        settings.scene = self.next_scene
