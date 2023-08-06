from tools import ImgEditor

NAME = 'AbobaGame'
ICON = ImgEditor.load_image('icon.png', colorkey=-1)

SIZE = WIDTH, HEIGHT = 1536, 864
CENTER = WIDTH // 2, HEIGHT // 2

INTERACTION_DISTANCE = 120
DOOR_DISTANCE = 70  # for invisible doors (passages)

DIALOGUE_POS = (CENTER[0], 750)
MAX_DIALOGUE_LENGTH = 111

FONT = '../assets/fonts/main.ttf'
TEXT_COLOR = (97, 57, 34)

TIME_COORDS = (1362, 5)
TIME_BOARD_COORDS = (1350, 20)

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
scene = 'menu'
time = {
    'hours': 12,
    'minutes': 0,
}
time_color = [255, 255, 255]
# for placing player when switching the scenes
player_pos = CENTER
player_status = 'down_idle'
window_opened = False
