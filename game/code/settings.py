from tools import ImgEditor

NAME = 'AbobaGame'
ICON = ImgEditor.load_image('icon.png', colorkey=-1)

SIZE = WIDTH, HEIGHT = 1536, 864
CENTER = WIDTH // 2, HEIGHT // 2

INTERACTION_DISTANCE = 148
DOOR_DISTANCE = 70  # for invisible doors (passages)

DIALOGUE_POS = (CENTER[0], 750)
MAX_DIALOGUE_LENGTH = 96

FONT = '../assets/fonts/main.ttf'
TEXT_COLOR = (97, 57, 34)

TIME_COORDS = (1362, 5)
TIME_BOARD_COORDS = (1350, 20)

ITEM_COORDS = (530, 260)
ITEM_OFFSET = 75

QUEST_COORDS = (515, 260)
QUEST_OFFSET = 75
QUEST_IMAGE = ImgEditor.enhance_image(ImgEditor.load_image('overlay/exclamation mark.png', colorkey=-1), 4)

LAYERS = {
    'background': 0,
    'floor': 1,
    'main': 2,
    'ceiling': 3,
    'rain': 4,
    'dialogue': 5,
    'overlay': 6,
}

# will be set in main.py
journal = None
inventory = None

# variables that can be changed
current_cursor = None
scene = 'menu'

time = {
    'hours': 12,
    'minutes': 0,
}

# for placing player when switching the scenes
player_pos = CENTER
player_status = 'down_idle'

window_opened = False
dialogue_run = False

new_quest = False
