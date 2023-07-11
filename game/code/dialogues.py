import itertools
import pygame
from random import choice
from tools import ImgEditor, blit_text
import settings
from core import BaseSprite


class DialogueLine:
    id_iter = itertools.count()

    def __init__(self, kind, text, is_locked=False, *events):
        self.id = next(self.id_iter)  # to lock/unlock particular line
        self.kind = kind  # character and mood (denis-neutral)
        self.text = text  # dialogue text (blah blah blah)
        self.events = events  # what will happen after line has been shown (add item apple)
        self.is_locked = is_locked  # if dialogue can be shown or not

    def run_events(self):
        for event in self.events:
            event = event.split()
            if event[0] == 'go_to':
                pass
            elif event[0] == 'unlock':
                pass
            elif event[0] == 'lock':
                pass
            elif event[0] == 'add':
                pass
            elif event[0] == 'remove':
                pass
            elif event[0] == 'next_step':
                pass
            elif event[0] == 'nothing':
                pass


class Dialogue:
    def __init__(self, name, group, descriptions=None):
        self.name = name
        self.descriptions = descriptions

        self.font = pygame.font.Font(settings.FONT, 65)
        self.talk = [[]]  # current talk
        self.current_talk = []  # current part of talk
        self.current_text = ''
        self.kind = ''  # base dialogue or someone's (kind of current text)

        self.stage = 0
        self.is_shown = False

        self.dialogue = BaseSprite(ImgEditor.load_image(f'empty.png'),
                                   settings.DIALOGUE_POS,
                                   settings.LAYERS['dialogue'], group)

        # animation
        self.speed = 800  # appearing & disappearing speed
        # text animation
        self.text_frame = 0
        self.text_speed = 23

    def run(self, is_mouse_on):
        if not self.is_shown and is_mouse_on:
            settings.dialogue_run = True
            self.is_shown = True
            self.stage = 0

            # choosing random talk which is not locked
            talks = dialogues[self.name]
            while True:
                self.talk = choice(talks)
                if not self.talk[0][0].is_locked:
                    break

        elif self.is_shown:
            self.stage += 1
            self.text_frame = 0
            if self.stage == len(self.current_talk):
                # end of the dialogue
                settings.dialogue_run = False
                self.is_shown = False
                self.current_text = ''

        if self.is_shown:
            self.current_talk = self.talk[0]
            self.current_talk = [choice(self.descriptions)] + self.current_talk
            self.current_text = self.current_talk[self.stage].text
            self.kind = self.current_talk[self.stage].kind
            img = ImgEditor.enhance_image(ImgEditor.load_image(f'/dialogues/{self.kind}_dialogue.png'), 4)
            self.dialogue.image = img
            self.dialogue.rect = self.dialogue.image.get_rect(center=(settings.DIALOGUE_POS[0], 1000))

    def animate(self, delta_time, screen):
        if self.stage == 0:  # appearing
            if self.dialogue.rect.centery > settings.DIALOGUE_POS[1]:
                self.dialogue.rect.centery -= self.speed * delta_time
        elif self.stage == len(self.current_talk):  # disappearing
            if self.dialogue.rect.centery < 1000:
                self.dialogue.rect.centery += self.speed * delta_time
        else:
            self.dialogue.rect.centery = settings.DIALOGUE_POS[1]

        # text
        if self.kind != 'base':
            pos = (600, 90 + self.dialogue.rect.y)
        else:
            pos = (475, 110 + self.dialogue.rect.y)
        text = self.current_text[:int(self.text_frame)]
        if self.text_frame < len(self.current_text):
            self.text_frame += self.text_speed * delta_time
        blit_text(screen, pos, 1210, text, self.font, settings.TEXT_COLOR, (True, (self.kind == 'base')))

    def update(self, dt, screen):
        self.animate(dt, screen)


dialogues = {
    'пугало': [
        [[DialogueLine('denis', 'Это пугало как будто говорит воронам: "Страдай или вали".'),
          DialogueLine('denis', 'Зачем ставить пугало рядом с клумбой?')]],
    ],
    'указатель': [
        [[DialogueLine('base', '"Торговец".'),
          DialogueLine('denis', 'Надпись почти не разобрать.')]],
    ],
    'корзинка для пикника': [
        [[DialogueLine('denis', 'Блин, пустая.')]],
    ],
    'клумба': [
        [[DialogueLine('denis', 'Не могу узнать ни один цветок.'),
          DialogueLine('denis', 'Земля ещё сырая. Кто-то за ней ухаживает... Интересно, кто.')]],
        [[DialogueLine('denis', 'Это клумба что-ли?'),
          DialogueLine('artem', 'Да, это типа такая клумба.')]]
    ],
    'окно': [
        [[DialogueLine('denis', 'Ничего не видно.')]]
    ],
    'почтовый ящик': [
        [[DialogueLine('denis', 'Хм... пусто.')]]
    ],
    'коврик': [
        [[DialogueLine('denis', 'Под ковриком лежат ключи... Один от двери, от чего другие?', False, 'unlock')]]
    ],
}

# going through the dialogue strings to find out if some parts are too long
for name, talks in dialogues.items():
    new_talks = []
    for talk in talks:
        new_talk = []
        for part in talk:
            new_part = []
            for line in part:
                if len(line.text) > settings.MAX_DIALOGUE_LENGTH:
                    part = ''
                    for word in line.text.split():
                        if len(part) + len(word) <= settings.MAX_DIALOGUE_LENGTH:
                            part += word + ' '
                        else:
                            new_part.append(DialogueLine(line.kind, part))
                            part = word + ' '
                    new_part.append(DialogueLine(line.kind, part, False, line.events))
                else:
                    new_part.append(line)
            new_talk.append(new_part)
        new_talks.append(new_talk)
    dialogues[name] = new_talks

# looking for id of particular line

# for i in dialogues['клумба']:
#     for j in i:
#         print(*[k.id for k in j])
