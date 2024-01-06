from tools import ImgEditor
from saving_manager import SavingManager

SCALE_K = 4
BIGGER_SCALE = SCALE_K * 1.5 - 0.5 * bool(SCALE_K % 2)

NAME = 'AbobaGame'
ICON = ImgEditor.load_image('icon.png', 6, colorkey=-1)

SIZE = WIDTH, HEIGHT = 384 * SCALE_K, 216 * SCALE_K
CENTER = WIDTH // 2, HEIGHT // 2

ADD_SOUND = None  # will be set in main.py

INTERACTION_DISTANCE = 37 * SCALE_K
DOOR_DISTANCE = 16 * SCALE_K  # for invisible doors (passages)

DIALOGUE_POS = (CENTER[0], 188 * SCALE_K)
MAX_DIALOGUE_LENGTH = 96

FONT = '../assets/fonts/main.ttf'
TEXT_COLOR = (97, 57, 34)

TIME_COORDS = (1366, 3)
TIME_BOARD_COORDS = (1352, 18)

ITEM_COORDS = (133 * SCALE_K, 65 * SCALE_K)
ITEM_OFFSET = 19 * SCALE_K

QUEST_COORDS = (132 * SCALE_K, 68 * SCALE_K)
QUEST_OFFSET = 19 * SCALE_K
QUEST_IMAGE = ImgEditor.load_image('overlay/exclamation mark.png', SCALE_K, colorkey=-1)

ACHIEVE_COORDS = (132 * SCALE_K, 68 * SCALE_K)
ACHIEVE_OFFSET = 21 * SCALE_K
ACHIEVE_IMAGE = ImgEditor.load_image('overlay/achievement.png', SCALE_K, colorkey=-1)
LOCKED_ACHIEVE_IMAGE = ImgEditor.load_image('overlay/locked_achievement.png', SCALE_K, colorkey=-1)

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
achieves = None
menu_window = None
music_player = None
socks = None

# variables that can be changed
player = 'denis'
current_cursor = None

scene = 'menu'
previous_scene = 'first_street_scene'
scene = saving_manager.load_data('scene', scene)
previous_scene = saving_manager.load_data('previous_scene', previous_scene)

next_music = saving_manager.load_data('next_music', 'street_day.mp3')

time = {
    'hours': 12,
    'minutes': 0,
}
time = saving_manager.load_data('time', time)
time_color = None
next_time = 1

# for placing player when switching the scenes
player_pos = saving_manager.load_data('player_pos', CENTER)
player_status = 'down_idle'

window_opened = False
dialogue_run = False

new_achieve = False
denis_new_quest = saving_manager.load_data('denis_new_quest', False)
artem_new_quest = saving_manager.load_data('artem_new_quest', False)
new_achieve = saving_manager.load_data('new_achieve', new_achieve)

talked_characters = 0
visited_scenes = 0
seen_objects = 0
cleaned_socks = 0
finished_quests = 0
