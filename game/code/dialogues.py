from core import DialogueLine

dialogues = {
    'пугало': [
        [DialogueLine('denis', 'Это пугало как будто говорит воронам: "Страдай или вали".'),
         DialogueLine('denis', 'Зачем ставить пугало рядом с клумбой?')],
    ],
    'указатель': [
        [DialogueLine('base', '"Торговец".'),
         DialogueLine('denis', 'Надпись почти не разобрать.')],
    ],
    'корзинка для пикника': [
        [DialogueLine('denis', 'Блин, пустая.')],
    ],
    'клумба': [
        [DialogueLine('denis', 'Не могу узнать ни один цветок.'),
         DialogueLine('denis', 'Земля ещё сырая. Кто-то за ней ухаживает... Интересно, кто.')]
    ],
    'окно': [
        [DialogueLine('denis', 'Ничего не видно.')]
    ],
    'почтовый ящик': [
        [DialogueLine('denis', 'Хм... пусто.')]
    ],
    'коврик': [
        [DialogueLine('denis', 'Под ковриком лежат ключи... Один от двери, от чего другие?', False, 'unlock')]
    ],
}

# looking for id of particular line

# for i in dialogues['клумба']:
#    print(*[j.id for j in i])
