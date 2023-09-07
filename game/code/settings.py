from tools import ImgEditor
from saving_manager import SavingManager

SCALE_K = 4
BIGGER_SCALE = SCALE_K * 1.5 - 0.5 * bool(SCALE_K % 2)

NAME = 'AbobaGame'
ICON = ImgEditor.load_image('icon.png', 6, colorkey=-1)

SIZE = WIDTH, HEIGHT = 384 * SCALE_K, 216 * SCALE_K
CENTER = WIDTH // 2, HEIGHT // 2

INTERACTION_DISTANCE = 37 * SCALE_K
DOOR_DISTANCE = 16 * SCALE_K  # for invisible doors (passages)

DIALOGUE_POS = (CENTER[0], 188 * SCALE_K)
MAX_DIALOGUE_LENGTH = 96

FONT = '../assets/fonts/main.ttf'
TEXT_COLOR = (97, 57, 34)

TIME_COORDS = (342 * SCALE_K, 1 * SCALE_K)
TIME_BOARD_COORDS = (338 * SCALE_K, 5 * SCALE_K)

ITEM_COORDS = (133 * SCALE_K, 65 * SCALE_K)
ITEM_OFFSET = 19 * SCALE_K

QUEST_COORDS = (129 * SCALE_K, 65 * SCALE_K)
QUEST_OFFSET = 19 * SCALE_K
QUEST_IMAGE = ImgEditor.load_image('overlay/exclamation mark.png', SCALE_K, colorkey=-1)

LAYERS = {
    'background': 0,
    'floor': 1,
    'main': 2,
    'ceiling': 3,
    'rain': 4,
    'dialogue': 5,
    'overlay': 6,
}

saving_manager = SavingManager()

# will be set in main.py
journal = None
inventory = None

# variables that can be changed
player = 'denis'
current_cursor = None
scene = 'menu'
previous_scene = 'menu'

time = {
    'hours': 12,
    'minutes': 0,
}
time = saving_manager.load_data('time', time)

# for placing player when switching the scenes
player_pos = CENTER
player_status = 'down_idle'

window_opened = False
dialogue_run = False

new_quest = False
