SIZE = WIDTH, HEIGHT = 1536, 864
CENTER = WIDTH // 2, HEIGHT // 2

INTERACTION_DISTANCE = 120

DIALOGUE_POS = (CENTER[0], 750)
MAX_DIALOGUE_LENGTH = 111
DIALOGUES = {
    'пугало': ['denis_Это пугало как будто говорит воронам: "Страдай или вали".',
               'denis_Зачем ставить пугало рядом с клумбой?'],
    'указатель': ['base_"Торговец".', 'denis_Надпись почти не разобрать.'],
    'корзинка для пикника': ['denis_Блин, пустая.'],
    'клумба': [
        'denis_Не могу узнать ни один цветок.', 'denis_Земля ещё сырая. Кто-то за ней ухаживает... Интересно, кто.'],
    'окно': ['denis_Ничего не видно.'],
    'почтовый ящик': ['denis_Хм... пусто.'],
    'коврик': ['denis_Под ковриком лежат ключи... Один от двери, от чего другие?'],
}

FONT = '../assets/fonts/main.ttf'
TEXT_COLOR = (97, 57, 34)

LAYERS = {
    'background': 0,
    'floor': 1,
    'main': 2,
    'ceiling': 3,
    'rain': 4,
    'dialogue': 5,
    'overlay': 6,
}

# variables that can be changed
current_cursor = None
dialogue_run = False
scene = 'first_street_scene'
