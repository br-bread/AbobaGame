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
                    if settings.player == 'denis':
                        if not settings.journal.denis_quests[int(event[2])].is_showed:
                            settings.journal.denis_quests[int(event[2])].unlock()
                            settings.journal.denis_quest_count += 1
                            settings.denis_new_quest = True
                            settings.ADD_SOUND.play()
                    else:
                        if not settings.journal.artem_quests[int(event[2])].is_showed:
                            settings.journal.artem_quests[int(event[2])].unlock()
                            settings.journal.artem_quest_count += 1
                            settings.artem_new_quest = True
                            settings.ADD_SOUND.play()
                elif event[1] == 'achieve':  # unlock achieve id
                    if settings.achieves.achieves[int(event[2])].is_locked:
                        settings.achieves.achieves[int(event[2])].unlock()
                        settings.achieves.achieve_count += 1
                        settings.new_achieve = True
                        settings.ADD_SOUND.play()
                else:  # unlock name id
                    if settings.player == 'denis':
                        dialogues = denis_dialogues
                    else:
                        dialogues = artem_dialogues
                    for talk in dialogues[event[1]]:
                        for part in talk:
                            for line in part:
                                if line.id == int(event[2]):
                                    line.unlock()
                                    break
            elif event[0] == 'lock':  # lock quest id
                if event[1] == 'quest':
                    if settings.player == 'denis':
                        settings.journal.denis_quests[int(event[2])].lock()
                        settings.journal.denis_quest_count -= 1
                        if settings.journal.denis_quest_count == 0:
                            settings.denis_new_quest = False
                    else:
                        settings.journal.artem_quests[int(event[2])].lock()
                        settings.journal.artem_quest_count -= 1
                        if settings.journal.artem_quest_count == 0:
                            settings.artem_new_quest = False

                elif event[1] == 'achieve':
                    settings.achieves.achieve[int(event[2])].lock()
                    settings.achieves.achieve_count -= 1
                    if settings.achieves.achieve_count == 0:
                        settings.new_achieve = False
                else:  # lock name id
                    if settings.player == 'denis':
                        dialogues = denis_dialogues
                    elif settings.player == 'artem':
                        dialogues = artem_dialogues
                    for talk in dialogues[event[1]]:
                        for part in talk:
                            for line in part:
                                if line.id == int(event[2]):
                                    line.lock()
                                    break
            elif event[0] == 'add':  # add item count
                settings.ADD_SOUND.play()
                if settings.player == 'artem':
                    settings.inventory.artem_items[event[1]].add(int(event[2]))
                    if settings.inventory.artem_items[event[1]].count == 1:
                        settings.inventory.artem_item_count += 1
                else:
                    settings.inventory.denis_items[event[1]].add(int(event[2]))
                    if settings.inventory.denis_items[event[1]].count == 1:
                        settings.inventory.denis_item_count += 1
            elif event[0] == 'remove':  # remove item count
                if settings.player == 'artem':
                    settings.inventory.artem_items[event[1]].remove(int(event[2]))
                    if settings.inventory.artem_items[event[1]].count == 0:
                        settings.inventory.artem_item_count -= 1
                else:
                    settings.inventory.denis_items[event[1]].remove(int(event[2]))
                    if settings.inventory.denis_items[event[1]].count == 0:
                        settings.inventory.denis_item_count -= 1
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
            if settings.player == 'denis':
                talks = denis_dialogues[self.name]
            elif settings.player == 'artem':
                talks = artem_dialogues[self.name]
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
# Денис - 3**
# rest - 0
artem_dialogues = {
    'пугало': [
        [[DialogueLine('artem', 'Где-то я это уже видел...'),
          DialogueLine('artem', 'Зачем ставить пугало рядом с клумбой?')]],
    ],
    'указатель': [
        [[DialogueLine('base', '"Торговец".'),
          DialogueLine('artem', 'Надпись почти не разобрать.')]],
    ],
    'корзинка для пикника': [
        [[DialogueLine('artem', 'Внутри ничего нет... *вздыхает*')]],
    ],
    'клумба': [
        [[DialogueLine('artem', 'Земля ещё сырая, я недавно поливал.')]],
    ],
    'окно': [
        [[DialogueLine('artem', 'Ничего не видно.')]]
    ],
    'почтовый ящик': [
        [[DialogueLine('artem', 'Новой почты нет.')]]
    ],
    'коврик': [
        [[DialogueLine('artem', 'Под ковриком лежат ключи... Один от двери, другие от наших комнат.', 1)]],
        [[DialogueLine('artem', 'А вот и он.', 2, 0, True, 'add keyA 1', 'lock коврик 2',
                       'unlock коврик 3', 'lock quest 1')]],
        [[DialogueLine('base', 'Под ковриком лежат ключи.', 3, 0, True)]],
    ],
    'Боб': [
        [[DialogueLine('base', 'Его зовут Боб, и он не папоротник, он боб. Его же так и зовут!'),
          DialogueLine('base', 'Что не понятного? Это Боб!')]],
    ],
    'коробка из-под роллов': [
        [[DialogueLine('artem', '"Томми Фиш".'),
          DialogueLine('denis-grudge', '"Оригами" лучше.'),
          DialogueLine('artem-thinking', 'Для меня все роллы одинаковые.')]],
    ],
    'консервы': [
        [[DialogueLine('artem-thinking', 'А где нож?')]],
    ],
    'сундук': [
        [[DialogueLine('artem', 'Пластинок нет.')]],
    ],
    'барабанная установка': [
        [[DialogueLine('artem', 'Это у Ксюши.')]],
    ],
    'холодильник': [
        [[DialogueLine('base', 'Внутри лежит багет с ветчиной.'),
          DialogueLine('artem', 'Ксюшин багет...'),
          DialogueLine('artem-thinking', 'Когда она уже его съест?'),
          ]],
    ],
    'записки': [
        [[DialogueLine('base', 'Артём: помыть посуду'),
          DialogueLine('base', 'Денис: пропылесосить'),
          DialogueLine('base', 'Ксюша: собрать установку'),
          DialogueLine('artem', 'Денис так и не пылесосил.'),
          DialogueLine('denis-angry', 'Пошёл нахуй.'),
          ]],
    ],
    'салат': [
        [[DialogueLine('artem', 'Сколько уже он тут стоит?...')]],
    ],
    'коробка с чаем': [
        [[DialogueLine('artem-thinking', 'Остался только "Сочное яблоко".')]],
    ],
    'фикус': [
        [[DialogueLine('artem', 'Они размножаются со скоростью света.')]]
    ],
    'книги': [
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('artem', '"Преступление и наказание". Не, уже читал.')]],
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('artem', '"Обломов". Не, уже читал.')]],
        [[DialogueLine('base', 'Вы берёте случайную книгу.'),
          DialogueLine('artem', '"Мёртвые души 2 том". Не, уже читал.'),
          DialogueLine('artem-surprized', 'Стоп, что?'),
          DialogueLine('base', 'Книга сгорела на ваших глазах подобно фениксу.')]],
    ],
    'вязаный Почита': [
        [[DialogueLine('artem', 'Почита Дениса.')]]
    ],
    'комната Ксюши': [
        [[DialogueLine('artem', 'Не думаю, что стоит заходить без разрешения.')]]
    ],
    'комната Артёма': [
        [[DialogueLine('artem', 'Чёрт, забыл взять ключи. Они должны быть внизу под ковриком.', 0, 0, False,
                       'unlock quest 0', 'lock коврик 1',
                       'unlock коврик 2')]]
    ],
    'комната Дениса': [
        [[DialogueLine('artem', 'Не думаю, что стоит заходить без разрешения.')]]
    ],
    'тапочки': [
        [[DialogueLine('denis-surprized', 'Мои тапочки-динозавры!')]]
    ],
    'диплом': [
        [[DialogueLine('artem', 'Мой диплом it-школы cамсунг.')]]
    ],
    'плакат': [
        [[DialogueLine('artem', 'Это Рик!')]]
    ],
    'тумбочка': [
        [[DialogueLine('artem-surprized', 'Ореховая шоколадка! Откуда она здесь?', 10, 0, False, 'lock тумбочка 10',
                       'unlock тумбочка 11'),
          DialogueLine('base', 'Вы получили ореховую шоколадку.', 0, 0, False, 'add nut_chocolate 1')]],
        [[DialogueLine('artem-thinking', 'Внутри пусто.', 11, 0, True)]]
    ],
    'носок': [
        [[DialogueLine('artem', 'Надо бы как-нибудь прибраться.')]]
    ],
    'Артём': [
        [[DialogueLine('artem', 'Ксюша лохушка у неё забаговалась игра.')]]
    ],
    'Денис': [
        [[DialogueLine('denis', 'С днём рождения, лошара.', 300),
          DialogueLine('base', 'Вы получили шоколадку.', 0, 0, False, 'add chocolate 1'),
          DialogueLine('artem', 'Спасибо, Денис!'),
          DialogueLine('denis-grudge', 'Чё, ты в курсе что ты проставляешься?'),
          DialogueLine('artem-surprized', 'Эээ... Нет.'),
          DialogueLine('denis', 'Ну вот. Мы сегодня празднуем, с тебя еда.', 0, 0, False, 'unlock quest 1',
                       'unlock quest 2'),
          DialogueLine('artem', 'Ладно, что-нибудь придумаю.'),
          DialogueLine('denis-grudge',
                       'А ещё должна приехать Яна, и надо подготовить дом к её приезду. '
                       'Каждый убирается в своей комнате.', 0, 0, False, 'unlock quest 3'),
          DialogueLine('artem-thinking', 'Да блин. Ладно.', 0, 0, False, 'lock Денис 300', 'unlock Денис 301')]],
        [[DialogueLine('denis', 'Чё, Тём? Тебе что-то нужно?', 301, 0, True),
          DialogueLine('artem', 'Да нет, я просто подошёл.'),
          DialogueLine('denis', 'Ок.')]]
    ],
    'Ксюша': [
        [[DialogueLine('ksusha', 'Артём! С днём рождения!! У меня есть для тебя подарок!', 200),
          DialogueLine('base', 'Вы получили конфету.', 0, 0, False, 'add candy 1'),
          DialogueLine('artem', 'Спасибо!'),
          DialogueLine('ksusha', 'Кстати, ты можешь открыть инвентарь, нажав i.'),
          DialogueLine('ksusha-left', 'А для журнала заданий j.'),
          DialogueLine('artem', 'Да, я уже знаю.'),
          DialogueLine('ksusha', '...'),
          DialogueLine('ksusha-left', 'Ну да. Ты-то уже в курсе, что это игра.'),
          DialogueLine('ksusha', '...'),
          DialogueLine('ksusha-sad', '...'),
          DialogueLine('ksusha-sad', '....'),
          DialogueLine('ksusha-sad', '.....'),
          DialogueLine('ksusha-sad', '......'),
          DialogueLine('artem-thinking', 'Ты же в курсе, что я всё скипаю?'),
          DialogueLine('ksusha-sad', 'И что потом?'),
          DialogueLine('ksusha-grudge', 'Всю игру проскипаешь?'),
          DialogueLine('ksusha-grudge', 'Просто выйдешь и всё?'),
          DialogueLine('artem-thinking', 'Тут диалог как у Дениса, кринжовая. Я не хочу это всё опять читать.'),
          DialogueLine('ksusha-sad', 'Я старалась.'),
          DialogueLine('ksusha-sad', 'Не выходи сразу, пожалуйста.'),
          DialogueLine('ksusha', 'Но теперь тут уже есть сохранения!'),
          DialogueLine('artem', 'Круто!'),
          DialogueLine('ksusha', 'Спасибо!'),
          DialogueLine('ksusha-sad', '...'),
          DialogueLine('ksusha-sad', 'Ладно, я тебя выпускаю.'),
          DialogueLine('ksusha', 'Хорошей игры!'),
          DialogueLine('artem', 'Спасибо!', 0, 0, False, 'lock Ксюша 200', 'unlock Ксюша 201'),
          ]],
        [[DialogueLine('ksusha', 'м? Что-то случилось?', 201, 0, True),
          DialogueLine('artem', 'Да нет, я просто подошёл.'),
          DialogueLine('ksusha', 'Хорошо.')]]
    ],
    'Джесс': [
        [[DialogueLine('jess', 'Рады вас видеть в местном баре "Дж"!... Только мы пока закрыты.', 400),
          DialogueLine('artem', 'А что случилось?'),
          DialogueLine('jess',
                       'Думаем сворачивать бизнес. Клиентов настолько мало, '
                       'что мы работаем в минус... '),
          DialogueLine('artem', 'Ты тут работаешь?'),
          DialogueLine('jess', 'Да, я местный бармен. Была, по крайней мере. Больше я ничего не умею... '
                               'Не знаю, где теперь найти деньги.'),
          DialogueLine('artem', 'Почему? Тут же есть торговец, и вроде зарабатывает.'),
          DialogueLine('jess', 'Когда-нибудь у меня тоже будет своя лавка, но только не здесь. '
                               'Тут слишком мало людей для торговли.'),
          DialogueLine('artem', 'Ну, как знаешь.', 0, 0, False,
                       'unlock Джесс 401', 'lock Джесс 400'),
          ]],
        [[DialogueLine('jess', 'Тебе что-то нужно?', 401, 0, True),
          DialogueLine('artem', 'Нет, просто мимо проходил.'),
          DialogueLine('jess', 'Хорошо.')]]
    ],
    'Джефф': [
        [[DialogueLine('jeff', 'Мы закрыты.', 500),
          DialogueLine('artem', 'Ты тут работаешь?'),
          DialogueLine('jeff', 'Обычно да.'),
          DialogueLine('artem', 'Ты бармен?'),
          DialogueLine('jeff', 'Нет. Джесс пыталась научить меня, но пока ещё не вышло.'
                               ' А так, я официант.'),
          DialogueLine('artem', 'А Джесс - твоя сестра?'),
          DialogueLine('jeff', 'Да, мы типа двойняшки.'),
          DialogueLine('artem', 'Круто! У вас типа семейный бизнес?'),
          DialogueLine('jeff', 'Вроде того.', 0, 0, False,
                       'unlock Джефф 502', 'lock Джефф 500'),
          ]],
        [[DialogueLine('jeff', 'Ты не мог бы оказать мне одну услугу?', 502, 0, True),
          DialogueLine('artem', 'Что-то случилось?'),
          DialogueLine('jeff',
                       'Моя сестра очень расстраивается из-за проблем с баром.'
                       ' Мне бы хотелось порадовать её.'),
          DialogueLine('artem', 'Нужно с чем-то помочь?'),
          DialogueLine('jeff',
                       'Она очень любит ореховый шоколад. Это обычный шоколад, но в зелёной упаковке. '
                       'Я не знаю, где его можно взять, но если ты принесёшь мне такую плитку, я заплачу тебе.'),
          DialogueLine('artem', 'Хорошо, попробую где-нибудь найти.', 0, 0, False, 'lock Джефф 502',
                       'unlock Джефф 501', 'unlock quest 4')]],
        [[DialogueLine('artem', 'Я принёс ореховый шоколад.', 503, 0, True),
          DialogueLine('jeff', 'Ого! Спасибо большое! Вот твои деньги.'),
          DialogueLine('base', 'Вы получили 15 монет.', 0, 0, False, 'lock Джефф 503', 'unlock Джефф 501',
                       'add money 15', 'remove nut_chocolate 1', 'lock quest 4', 'unlock achieve 2')]],
        [[DialogueLine('jeff', 'Тебе что-то нужно?', 501, 0, True),
          DialogueLine('artem', 'Нет, просто мимо проходил.'),
          DialogueLine('jeff', 'Хорошо.')]]
    ],
    'бочки': [
        [[DialogueLine('artem-thinking', 'Что там внутри?')]]
    ],
    'товары': [
        [[DialogueLine('artem-thinking', 'Какие-то яблоки...'),
          DialogueLine('artem', 'И яблочный сидр.')]]
    ],
    'торговец': [
        [[DialogueLine('base', 'Немой торговец молча кивнул.')]]
    ],
    'вывеска': [
        [[DialogueLine('base', 'Бар "Дж".'),
          DialogueLine('artem-thinking', 'Почему "Дж"?')]]
    ],
}
denis_dialogues = {
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
    'тумба': [
        [[DialogueLine('denis', 'Внутри пусто.')]]
    ],
    'носок': [
        [[DialogueLine('denis', 'Надо бы как-нибудь прибраться.')]]
    ],
    'Денис': [
        [[DialogueLine('denis', 'Ксюша лохушка у неё забаговалась игра.')]]
    ],
    'Артём': [
        [[DialogueLine('artem', 'Привет, Денис!', 100),
          DialogueLine('denis', 'Привет. Как проходит день рождения?'),
          DialogueLine('artem', 'Пока неплохо.'),
          DialogueLine('denis', 'Окей.', 0, 0, False,
                       'unlock Артём 101', 'lock Артём 100'),
          ]],
        [[DialogueLine('artem', 'Чё, Денис? Тебе что-то нужно?', 101, 0, True),
          DialogueLine('denis', 'Да нет, я просто подошёл.'),
          DialogueLine('artem', 'Ок.')]]
    ],
    'Ксюша': [
        [[DialogueLine('ksusha', 'Привет!', 200),
          DialogueLine('denis', 'Чё как дела?'),
          DialogueLine('ksusha', '...'),
          DialogueLine('ksusha-left', 'Почему спрашиваешь?'),
          DialogueLine('denis', 'Не знаю, чем заняться.'),
          DialogueLine('ksusha', 'Тогда лучше переключись на Артёма.'),
          DialogueLine('ksusha-left', 'У него квестов побольше.'),
          DialogueLine('denis', 'Ок.', 0, 0, False, 'lock Ксюша 200', 'unlock Ксюша 201', ),
          ]],
        [[DialogueLine('ksusha', 'Да?', 201, 0, True),
          DialogueLine('denis', 'Чё нового здесь появилось?'),
          DialogueLine('ksusha',
                       'Достижения, например. За них ты можешь получить в награду несколько монет.'
                       ' Окно достижений можно открыть при помощи "k".'),
          DialogueLine('denis', 'Круто.'),
          DialogueLine('ksusha', 'Слева от дома кстати теперь находятся бар и торговец.'),
          DialogueLine('denis', 'А когда бар откроется?'),
          DialogueLine('ksusha-sad', 'Пока не знаю...', 0, 0, False, 'lock Ксюша 201', 'unlock Ксюша 202', ),
          ]],
        [[DialogueLine('ksusha', 'м? Что-то случилось?', 202, 0, True),
          DialogueLine('denis', 'Да нет, я просто подошёл.'),
          DialogueLine('ksusha', 'Хорошо.')]]
    ],
    'Джесс': [
        [[DialogueLine('jess', 'Рады вас видеть в местном баре "Дж"!... Только мы пока закрыты.', 400),
          DialogueLine('denis', 'Всё-таки решили закрыться?'),
          DialogueLine('jess', 'Пока не решили. Но думаю, что да.'),
          DialogueLine('denis', 'Ну, удачи вам.'),
          DialogueLine('jess', 'Спасибо.', 0, 0, False,
                       'unlock Джесс 401', 'lock Джесс 400'),
          ]],
        [[DialogueLine('jess', 'Тебе что-то нужно?', 401, 0, True),
          DialogueLine('denis', 'Нет, просто мимо проходил.'),
          DialogueLine('jess', 'Хорошо.')]]
    ],
    'Джефф': [
        [[DialogueLine('jeff', 'Привет. Мы закрыты.', 500),
          DialogueLine('denis', 'Жаль. Но ты главное не расстраивайся.'),
          DialogueLine('jeff', 'Да, спасибо.', 0, 0, False,
                       'unlock Джефф 501', 'lock Джефф 500'),
          ]],
        [[DialogueLine('jeff', 'Тебе что-то нужно?', 501, 0, True),
          DialogueLine('denis', 'Нет, просто мимо проходил.'),
          DialogueLine('jeff', 'Хорошо.')]]
    ],
    'бочки': [
        [[DialogueLine('denis-grudge', 'Что там внутри?')]]
    ],
    'товары': [
        [[DialogueLine('denis-grudge', 'Какие-то яблоки...'),
          DialogueLine('denis', 'И яблочный сидр.')]]
    ],
    'торговец': [
        [[DialogueLine('base', 'Немой торговец молча кивнул.')]]
    ],
    'вывеска': [
        [[DialogueLine('base', 'Бар "Дж".'),
          DialogueLine('denis', 'Первая буква имён владельцев.')]]
    ],
}

denis_dialogues = settings.saving_manager.load_data('denis_dialogues', denis_dialogues)
artem_dialogues = settings.saving_manager.load_data('artem_dialogues', artem_dialogues)

# going through the dialogue strings to find out if some parts are too long
for name, talks in denis_dialogues.items():
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
    denis_dialogues[name] = new_talks

for name, talks in artem_dialogues.items():
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
    artem_dialogues[name] = new_talks

# looking for id of particular line

# for i in dialogues['Ксюша']:
#     for j in i:
#         print(*[k.id for k in j])
