from core import InteractiveSprite, BaseSprite
from dialogues import Dialogue, DialogueLine
from tools import ImgEditor
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


class Door(InteractiveSprite):  # just door sprite
    def __init__(self, img, pos, layer, scene, next_scene, player_pos, player_status, *groups):
        super().__init__(img, pos, layer, *groups)
        self.cursor_image = 'arrow_cursor.png'
        self.next_scene = next_scene
        self.scene = scene
        self.player_pos = player_pos
        self.player_status = player_status

    def update(self, dt, player_pos, events, *args, **kwargs):  # will be called ONE time
        super().update(dt, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_on():
                        self.scene.disappear(self.next_scene, self.player_pos, self.player_status)


class InvisibleDoor(BaseSprite):  # passage to another scene, also a door, but invisible and not interactive (by mouse)
    def __init__(self, pos, scene, next_scene, player_pos, player_status, *groups):
        super().__init__(ImgEditor.load_image('invisible_door.png'), pos, settings.LAYERS['main'], *groups)
        self.scene = scene
        self.next_scene = next_scene
        self.player_pos = player_pos
        self.player_status = player_status

    def update(self, dt, player_pos, *args, **kwargs):  # will be called MULTIPLE times
        if self.get_distance(player_pos) <= settings.DOOR_DISTANCE:
            self.scene.disappear(self.next_scene, self.player_pos, self.player_status)
