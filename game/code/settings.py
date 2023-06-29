SIZE = WIDTH, HEIGHT = 1536, 864
CENTER = WIDTH // 2, HEIGHT // 2

INTERACTION_DISTANCE = 120

DIALOGUE_POS = (CENTER[0], 750)
MAX_DIALOGUE_LENGTH = 111
DIALOGUES = {
    'пугало': [
        'denis_Это пугало как будто говорит воронам: "Страдай или вали".']
}

FONT = '../assets/fonts/main.ttf'
TEXT_COLOR = (97, 57, 34)

LAYERS = {
    'background': 0,
    'main': 1,
    'rain': 2,
    'dialogue': 3,
    'overlay': 4,
}

# variables that can be changed
current_cursor = None
dialogue_run = False
