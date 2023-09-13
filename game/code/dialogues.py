import pygame
from random import choice
from tools import ImgEditor, blit_text
import settings
from core import BaseSprite

pygame.init()


class DialogueLine:

    def __init__(self, kind, text, id=0, priority=0, is_locked=False, *events):
        self.kind = kind  # character and mood (denis-neutral)
        self.text = text  # dialogue text (blah blah blah)
        self.id = id  # to lock/unlock particular line
        self.priority = priority
        self.is_locked = is_locked  # if dialogue can be shown or not
        self.events = list(events)  # what will happen after line has been shown (add item apple)

    def lock(self):
        self.is_locked = True

    def unlock(self):
        self.is_locked = False

    def run_events(self):
        for event in self.events:
            event = event.split()
            if event[0] == 'go_to':
                pass
            elif event[0] == 'unlock':  # unlock quest id
                if event[1] == 'quest':
                    if not settings.journal.quests[int(event[2])].is_showed:
                        settings.journal.quests[int(event[2])].unlock()
                        settings.journal.quest_count += 1
                        settings.new_quest = True
                        settings.ADD_SOUND.play()
                else:  # unlock name id
                    for talk in dialogues[event[1]]:
                        for part in talk:
                            for line in part:
                                if line.id == int(event[2]):
                                    line.unlock()
                                    break
            elif event[0] == 'lock':  # lock quest id
                if event[1] == 'quest':
                    settings.journal.quests[int(event[2])].lock()
                    settings.journal.quest_count -= 1
                else:  # lock name id
                    for talk in dialogues[event[1]]:
                        for part in talk:
                            for line in part:
                                if line.id == int(event[2]):
                                    line.lock()
                                    break
            elif event[0] == 'add':  # add item count
                settings.ADD_SOUND.play()
                settings.inventory.items[event[1]].add(int(event[2]))
                if settings.inventory.items[event[1]].count == 1:
                    settings.inventory.item_count += 1
            elif event[0] == 'remove':  # remove item count
                settings.inventory.items[event[1]].remove(int(event[2]))
                if settings.inventory.items[event[1]].count == 0:
                    settings.inventory.item_count -= 1
            elif event[0] == 'next_step':  # next_step id
                settings.journal.quests[int(event[1])].next_step()
            # for talk in dialogues['Артём']:
            #     for part in talk:
            #         for line in part:
            #             print(line.text, line.id, line.is_locked)


class Dialogue:
    def __init__(self, name, group, descriptions=None):
        self.name = name
        self.descriptions = descriptions

        self.pos = list(settings.DIALOGUE_POS)
        self.font = pygame.font.Font(settings.FONT, 16 * settings.SCALE_K)
        self.talk = [[]]  # current talk
        self.current_talk = []  # current part of talk
        self.current_text = ''
        self.kind = ''  # base dialogue or someone's (kind of current text)

        self.stage = 0
        self.is_shown = False

        self.dialogue = BaseSprite(ImgEditor.load_image(f'empty.png', 1),
                                   settings.DIALOGUE_POS,
                                   settings.LAYERS['dialogue'], group)

        # animation
        self.speed = 200 * settings.SCALE_K  # appearing & disappearing speed
        # text animation
        self.text_frame = 0
        self.text_speed = 23

    def run(self):
        if not self.is_shown and not settings.window_opened:  # first opening
            settings.dialogue_run = True
            self.is_shown = True
            self.stage = 0

            # choosing random talk which is not locked
            talks = dialogues[self.name]
            while True:
                self.talk = choice(talks)
                if not self.talk[0][0].is_locked:
                    break

            self.current_talk = self.talk[0]
            if self.descriptions:
                self.current_talk = [choice(self.descriptions)] + self.current_talk
            else:
                self.current_talk = self.current_talk
            self.pos[1] = 250 * settings.SCALE_K
            self.current_text = self.current_talk[self.stage].text
            self.kind = self.current_talk[self.stage].kind
            img = ImgEditor.load_image(f'/dialogues/{self.kind}_dialogue.png', settings.SCALE_K)
            self.dialogue.image = img
            self.dialogue.rect = self.dialogue.image.get_rect(center=self.pos)
            self.current_talk[self.stage].run_events()

        elif self.is_shown and self.text_frame >= len(self.current_text):  # next step
            self.stage += 1
            self.text_frame = 0
            if self.stage == len(self.current_talk):
                # end of the dialogue
                settings.dialogue_run = False
                self.is_shown = False
                self.talk = [[]]
                self.current_text = ''
            else:
                self.current_text = self.current_talk[self.stage].text
                self.kind = self.current_talk[self.stage].kind
                img = ImgEditor.load_image(f'/dialogues/{self.kind}_dialogue.png', settings.SCALE_K)
                self.dialogue.image = img
                self.dialogue.rect = self.dialogue.image.get_rect(center=self.pos)
                self.current_talk[self.stage].run_events()

        elif self.is_shown and self.text_frame < len(self.current_text):
            self.text_frame = len(self.current_text)

    def animate(self, delta_time, screen):
        if self.stage == 0:  # appearing
            if self.dialogue.rect.centery > settings.DIALOGUE_POS[1]:
                self.dialogue.rect.centery -= self.speed * delta_time
        elif self.stage == len(self.current_talk):  # disappearing
            if self.dialogue.rect.centery < 250 * settings.SCALE_K:
                self.dialogue.rect.centery += self.speed * delta_time
        else:
            self.dialogue.rect.centery = settings.DIALOGUE_POS[1]
        self.pos = list(self.dialogue.rect.center)

        # text
        if self.kind != 'base':
            pos = (150 * settings.SCALE_K, 22 * settings.SCALE_K + self.dialogue.rect.y)
        else:
            pos = (118 * settings.SCALE_K, 27 * settings.SCALE_K + self.dialogue.rect.y)
        text = self.current_text[:int(self.text_frame)]
        if self.text_frame < len(self.current_text):
            self.text_frame += self.text_speed * delta_time
        blit_text(screen, pos, 302 * settings.SCALE_K, text, self.font, settings.TEXT_COLOR, settings.SCALE_K,
                  (True, (self.kind == 'base')))

    def update(self, dt, screen):
        self.animate(dt, screen)


# id
# Артём - 1**
# Ксюша - 2**
# rest - 0
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
    ],
    'окно': [
        [[DialogueLine('denis', 'Ничего не видно.')]]
    ],
    'почтовый ящик': [
        [[DialogueLine('denis', 'Хм... пусто.')]]
    ],
    'коврик': [
        [[DialogueLine('denis', 'Под ковриком лежат ключи... Один от двери, от чего другие?', 1)]],
        [[DialogueLine('denis', 'Наверное, это ключ от моей комнаты.', 2, 0, True, 'add keyD 1', 'lock коврик 2',
                       'unlock коврик 3', 'lock quest 1')]],
        [[DialogueLine('denis', 'Под ковриком лежат ключи.', 3, 0, True)]],
    ],
    'Боб': [
        [[DialogueLine('base', 'Его зовут Боб, и он не папоротник, он боб. Его же так и зовут!'),
          DialogueLine('base', 'Что не понятного? Это Боб!')]],
    ],
    'коробка из-под роллов': [
        [[DialogueLine('denis', '"Томми Фиш".'),
          DialogueLine('denis-grudge', '"Оригами" лучше.')]],
    ],
    'консервы': [
        [[DialogueLine('denis-grudge', 'А где нож?')]],
    ],
    'сундук': [
        [[DialogueLine('denis', 'Пластинок нет.')]],
    ],
    'барабанная установка': [
        [[DialogueLine('denis', 'Почему она стоит в доме?')]],
    ],
    'холодильник': [
        [[DialogueLine('base', 'Внутри лежит багет с ветчиной.'),
          DialogueLine('denis-surprized', 'О, хрючево!'),
          DialogueLine('artem-thinking', 'Ты свой уже съел. Это Ксюшин.'),
          DialogueLine('denis-angry', '...'),
          ]],
    ],
    'записки': [
        [[DialogueLine('base', 'Артём: помыть посуду'),
          DialogueLine('base', 'Денис: пропылесосить'),
          DialogueLine('base', 'Ксюша: собрать установку'),
          DialogueLine('denis-angry', 'Чё?? Не честно.'),
          DialogueLine('artem', 'Ты так и не пылесосил.'),
          DialogueLine('denis-angry', 'Пошёл нахуй.'),
          ]],
    ],
    'салат': [
        [[DialogueLine('denis', 'Сколько уже он тут стоит?...')]],
    ],
    'коробка с чаем': [
        [[DialogueLine('denis-grudge', 'Остался только "Сочное яблоко".')]],
    ],
    'фикус': [
        [[DialogueLine('denis', 'Они размножаются со скоростью света.')]]
    ],
    'книги': [
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('denis', '"451 по Фаренгейту". Не, уже читал.')]],
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('denis', '"Преступление и наказание". Не, уже читал.')]],
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('denis', '"1984". Не, уже читал.')]],
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('denis', '"Мёртвые души 2 том". Не, уже читал.'),
          DialogueLine('denis-surprized', 'Стоп, что?'),
          DialogueLine('base', 'Книга сгорела на ваших глазах подобно фениксу.')]],
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('denis', '"Мартин Иден". Не, в другой раз.'),
          DialogueLine('ksusha-grudge', 'Да можешь уже и не читать в принципе.')]],
    ],
    'вязаный Почита': [
        [[DialogueLine('denis-surprized', 'Почита? Ты тоже тут?')]]
    ],
    'комната Ксюши': [
        [[DialogueLine('denis', 'Не думаю, что стоит заходить без разрешения.')]]
    ],
    'комната Артёма': [
        [[DialogueLine('denis', 'Не думаю, что стоит заходить без разрешения.')]]
    ],
    'комната Дениса': [
        [[DialogueLine('denis', 'Закрыто. Нужно найти ключ.', 0, 0, False, 'unlock quest 1', 'lock коврик 1',
                       'unlock коврик 2')]]
    ],
    'тапочки': [
        [[DialogueLine('denis-surprized', 'Мои тапочки-динозавры!')]]
    ],
    'диплом': [
        [[DialogueLine('denis', 'Мой диплом it-школы cасунг.')]]
    ],
    'плакат': [
        [[DialogueLine('denis', 'Дота... Лучшая игра.')]]
    ],
    'тумбочка': [
        [[DialogueLine('denis', 'Внутри пусто.')]]
    ],
    'носок': [
        [[DialogueLine('denis', 'Надо бы как-нибудь прибраться.')]]
    ],
    'Артём': [
        [[DialogueLine('artem', 'Привет, Денис! С днём рождения! Это тебе.', 100),
          DialogueLine('base', 'Вы получили шоколадку.', 0, 0, False, 'add chocolate 1'),
          DialogueLine('denis', 'Спасибо.'),
          DialogueLine('artem', 'Что-то случилось?'),
          DialogueLine('denis', 'Я что-то запутался... Что это за место?'),
          DialogueLine('artem-thinking', 'В смысле?'),
          DialogueLine('denis-angry',
                       'Ты дурак блять? Что это за место? Где мы находимся? Что это за дом? Всё, '
                       'что я помню - мы вместе сидели и праздновали мой день рождения, а теперь я нахуй здесь.'),
          DialogueLine('artem-thinking', '(У него точно всё хорошо?..) Ладно, если ты ничего не помнишь, '
                                         'спроси у Ксюши. Обычно, если происходит что-то '
                                         'странное, она всегда в курсе.'),
          DialogueLine('denis', 'Что? Почему?'),
          DialogueLine('artem-thinking', 'Не знаю. Если что, она наверху.', 0, 0, False,
                       'unlock quest 0', 'unlock Артём 101', 'lock Артём 100'),
          ]],
        [[DialogueLine('artem', 'Чё, Денис? Тебе что-то нужно?', 101, 0, True),
          DialogueLine('denis', 'Да нет, я просто подошёл.'),
          DialogueLine('artem', 'Ок.')]]
    ],
    'Ксюша': [
        [[DialogueLine('ksusha', 'Денис! С днём рождения!! У меня есть для тебя подарок!', 200),
          DialogueLine('base', 'Вы получили конфету.', 0, 0, False, 'add candy 1'),
          DialogueLine('denis', 'Спасибо.'),
          DialogueLine('ksusha', 'Кстати, ты можешь открыть инвентарь, нажав i.'),
          DialogueLine('ksusha-left', 'А для журнала заданий j.'),
          DialogueLine('denis', 'Что ты имеешь ввиду?'),
          DialogueLine('ksusha', '...'),
          DialogueLine('ksusha-left', 'Это же игра, Денис.'),
          DialogueLine('denis', 'А как отсюда выйти-то? Как мне вернуться?'),
          DialogueLine('ksusha', 'Это не так просто! Ты уверен, что справишься?'),
          DialogueLine('denis', '...'),
          DialogueLine('denis-grudge', 'Я блять на лоха похож?'),
          DialogueLine('ksusha',
                       'Это будет твоя главная цель игры! Для начала тебе нужно найти кого-то, '
                       'кто даст тебе квест. Это должен быть кто-то очень серьёзный! '
                       'Главный босс. Кто-то, кто знает больше остальных. '
                       'Кто-то, кто знает, по каким правилам работает этот мир.'),
          DialogueLine('denis-grudge', 'Разве это не ты?'),
          DialogueLine('ksusha', '...'),
          DialogueLine('ksusha-left', 'Ну да.'),
          DialogueLine('denis-angry', 'Ну и чё бля?'),
          DialogueLine('ksusha', 'Видишь кнопку в правом верхнем углу?'),
          DialogueLine('denis', 'Ну.'),
          DialogueLine('ksusha-left', 'Нажми на неё.'),
          DialogueLine('denis-grudge', 'Ничего не происходит.'),
          DialogueLine('ksusha',
                       'Потому что ты в диалоге, гений. Когда нажмёшь на неё, '
                       'у тебя появится кнопка "Выход". Вот и всё.'),
          DialogueLine('denis', '...'),
          DialogueLine('denis-grudge', 'И? Ты можешь нахуй закрыть диалог?'),
          DialogueLine('ksusha', '...'),
          DialogueLine('ksusha-sad', '...'),
          DialogueLine('denis-grudge', 'Чё с лицом?'),
          DialogueLine('ksusha-sad', '....'),
          DialogueLine('ksusha-sad', '.....'),
          DialogueLine('ksusha-sad', '......'),
          DialogueLine('denis-grudge', 'Ты же в курсе, что я всё скипаю?'),
          DialogueLine('ksusha-sad', 'И что потом?'),
          DialogueLine('ksusha-grudge', 'Всю игру проскипаешь?'),
          DialogueLine('ksusha-grudge', 'Просто выйдешь и всё?'),
          DialogueLine('denis', 'Я не знаю. Как пойдёт.'),
          DialogueLine('ksusha-sad', 'Я старалась.'),
          DialogueLine('denis', 'Ок.'),
          DialogueLine('ksusha-sad', 'Не выходи сразу, пожалуйста.'),
          DialogueLine('denis', 'Ок.'),
          DialogueLine('ksusha-sad', 'Тут пока нет сохранений.'),
          DialogueLine('denis', 'Ок.'),
          DialogueLine('ksusha-sad', 'Если выйдешь, придётся болтать со мной заново.'),
          DialogueLine('denis', '...Ок.'),
          DialogueLine('ksusha-sad', '...'),
          DialogueLine('ksusha-sad', 'Ладно, я тебя выпускаю.'),
          DialogueLine('denis-grudge', 'Делай чё хочешь, мне насрать.'),
          DialogueLine('ksusha', 'Хорошей игры!'),
          DialogueLine('denis', 'Ок. Спасибо.', 0, 0, False, 'lock quest 0', 'lock Ксюша 200', 'unlock Ксюша 201',
                       'unlock Артём 101', 'lock Артём 100'),
          ]],
        [[DialogueLine('ksusha', 'м? Что-то случилось?', 201, 0, True),
          DialogueLine('denis', 'Да нет, я просто подошёл.'),
          DialogueLine('ksusha', 'Хорошо.')]]
    ],
}

dialogues = settings.saving_manager.load_data('dialogues', dialogues)

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
                    new_part.append(DialogueLine(line.kind, part, False, *line.events))
                else:
                    new_part.append(line)
            new_talk.append(new_part)
        new_talks.append(new_talk)
    dialogues[name] = new_talks

# looking for id of particular line

# for i in dialogues['Ксюша']:
#     for j in i:
#         print(*[k.id for k in j])
