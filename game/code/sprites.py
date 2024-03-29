from core import InteractiveSprite, BaseSprite
from dialogues import Dialogue, DialogueLine
from tools import ImgEditor
import settings
import pygame


class DialogueSprite(InteractiveSprite):
    def __init__(self, name, is_person, img, pos, cursor, layer, *groups, **kwargs):
        super().__init__(img, pos, layer, *groups)
        # general
        self.name = name
        self.id = -1
        if 'id' in kwargs.keys():
            self.id = kwargs['id']
        self.cursor_image = f'{cursor}_cursor.png'
        self.is_person = is_person
        # dialogue
        self.was_opened = False
        cap_name = name.capitalize()
        if len(name.split()) > 1:
            cap_name = name.split()[0].capitalize() + ' ' + ' '.join(name.split()[1:])
        description = [DialogueLine('base', f'Это {name}.'),
                       DialogueLine('base', f'Вот это да! Это {name}.'),
                       DialogueLine('base', f'Это просто {name}.'),
                       DialogueLine('base', f'Перед тобой {name}.'),
                       DialogueLine('base', f'Выглядит как {name}.'),
                       DialogueLine('base', f'Это {name}, ничего интересного.'),
                       DialogueLine('base', f'{cap_name}.')]
        if is_person:
            self.dialogue = Dialogue(self.name, groups[0])
        else:
            if self.id != -1:
                self.dialogue = Dialogue(self.name, groups[0], description, kwargs['id'])
            else:
                self.dialogue = Dialogue(self.name, groups[0], description)

    def update(self, dt, events, player_pos, screen, *args, **kwargs):
        super().update(dt, events, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_on() and not settings.dialogue_run:
                    self.dialogue.run()
                    if not self.was_opened:
                        self.was_opened = True
                        if self.is_person:
                            settings.talked_characters += 1
                        else:
                            settings.seen_objects += 1
                if self.dialogue.is_shown and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.dialogue.run()

        self.dialogue.update(dt, screen)


class Door(InteractiveSprite):  # just door sprite
    def __init__(self, img, pos, layer, scene, next_scene, next_music, player_pos, player_status, *groups):
        super().__init__(img, pos, layer, *groups)
        self.cursor_image = 'arrow_cursor.png'
        self.next_scene = next_scene
        self.next_music = next_music
        self.scene = scene
        self.player_pos = player_pos
        self.player_status = player_status

    def update(self, dt, events, player_pos, *args, **kwargs):  # will be called ONE time
        super().update(dt, events, player_pos)
        if self.is_accessible(self.get_distance(player_pos)):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_mouse_on() and not self.scene.appearing:
                        self.scene.disappear(self.next_scene, self.next_music, self.player_pos, self.player_status)


class InvisibleDoor(BaseSprite):  # passage to another scene, also a door, but invisible and not interactive (by mouse)
    def __init__(self, pos, scene, next_scene, next_music, player_pos, player_status, direction='h', *groups):
        super().__init__(ImgEditor.load_image(f'invisible_door_{direction}.png', 1), pos, settings.LAYERS['main'],
                         *groups)
        self.scene = scene
        self.next_scene = next_scene
        self.next_music = next_music
        self.player_pos = player_pos
        self.player_status = player_status

    def update(self, dt, events, player_pos, *args, **kwargs):  # will be called MULTIPLE times
        if self.get_distance(player_pos) <= settings.DOOR_DISTANCE and not self.scene.appearing:
            self.scene.disappear(self.next_scene, self.next_music, self.player_pos, self.player_status)
