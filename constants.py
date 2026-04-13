from typing import Final
from controls.controls import *

#Apps
VERSION :Final[str] = "1.1.0"
AUTHOR  :Final[str]= "Mark Okun"
APP_NAME:Final[str]= "Snake"

IS_DEV:Final[bool]     = False
IS_RELEASE:Final[bool] = False

#Colors

RED         :Final = (255, 0, 0)
RED_DARK    :Final = (127, 0, 0)
ORANGE      :Final = (255,127,0)
GREEN       :Final = (0, 255, 0)
GREEN_DARK  :Final = (0,127,0)
BLUE        :Final = (0, 0, 255)
BLUE_DARK   :Final = (0, 0, 127)
CYAN        :Final = (0, 100, 100)
BLACK       :Final = (0, 0, 0)
WHITE       :Final = (255, 255, 255)
GRAY        :Final = (127,127,127) 
GRAY_DARK   :Final = (64,64,64)
GRAY_LIGHT  :Final = (212,212,212)

#
# THEME
#
TEXT_COLOR       = WHITE
BK               = GRAY_DARK
FIELD_COLOR      = GRAY 
SNAKE_BODY_COLOR = GREEN
SNAKE_HEAD_COLOR = GREEN_DARK
SNAKE_TONG_COLOR = RED
SNAKE_EYE_COLOR  = RED
EYE_PUPIL_COLOR  = WHITE 
GRID_COLOR       = BK
FIELD_BORDER     = ORANGE    

VELOCITIES:Final[list] = [(-1,0),(1,0),(0,-1),(0,1)]
 
# cells values
EMPTY_VAL:Final[int] = 0
SNAKE_VAL:Final[int] = 1
FOOD_VAL :Final[int] = 2
ENEMY_VAL:Final[int] = 3

# return values

OK_RET_VAL    :Final[int] = 0
FOOD_RET_VAL  :Final[int] = 1
ERROR_RET_VAL :Final[int] = 10
BORDER_RET_VAL:Final[int] = ERROR_RET_VAL + 1
BODY_RET_VAL  :Final[int] = ERROR_RET_VAL + 2
EMENY_RET_VAL :Final[int] = ERROR_RET_VAL + 3

#geometric vaalues
CELL_SIZE   = 16
CELL_SIZE2  = CELL_SIZE/2

MAX_ROWS:Final[int] = 32
MAX_COLS:Final[int] = 48

MAX_FIELD_BORDER_TOP    :Final[int]= 32
MAX_FIELD_BORDER_BOTTOM :Final[int]= 24
MAX_FIELD_BORDER_LEFT   :Final[int]= 60
MAX_FIELD_BORDER_RIGHT  :Final[int]= 20

WIDTH_WINDOW  = CELL_SIZE * MAX_COLS + MAX_FIELD_BORDER_LEFT + MAX_FIELD_BORDER_RIGHT
HEIGHT_WINDOW = CELL_SIZE * MAX_ROWS + MAX_FIELD_BORDER_TOP  + MAX_FIELD_BORDER_BOTTOM

ROWS = MAX_ROWS
COLS = MAX_COLS

WIDTH  = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS

FIELD_BORDER_TOP    :Final[int]= MAX_FIELD_BORDER_TOP
FIELD_BORDER_BOTTOM :Final[int]= MAX_FIELD_BORDER_BOTTOM
FIELD_BORDER_LEFT   :Final[int]= MAX_FIELD_BORDER_LEFT
FIELD_BORDER_RIGHT  :Final[int]= MAX_FIELD_BORDER_RIGHT

#Folders

ASSET_FOLDER:str = 'assets'
SOUND_FOLDER:Final[str] = 'sounds'
DATA_FOLDER :Final[str] = 'data'
GRAVE_FOLDER:Final[str] = 'grave'
RESOURCES   :Final[str] = 'resources'  

#Files
SCORE_FILE   :Final[str] = "statistics.ini"
SETTINGS_FILE:Final[str] = "snake.ini"

#game properties

MAX_ENEMIES          :Final[int] = 10
STEPS_TO_CREATE_FOOD :Final[int] = 100
STEPS_TO_CREATE_ENEMY:Final[int] = 220

#modes
     
MODE_PLAY      :Final[int] = 0
MODE_CMP_PLAY  :Final[int] = 1
MODE_WELCOME   :Final[int] = 2
MODE_ABOUT     :Final[int] = 3
MODE_HELP      :Final[int] = 4
MODE_AGONY     :Final[int] = 5
MODE_GAME_OVER :Final[int] = 6
MODE_EXIT      :Final[int] = 7
MODE_OPTIONS   :Final[int] = 8


MODES_MENU :Final[list] = [MODE_WELCOME,MODE_ABOUT,MODE_HELP]
MODES_PLAY :Final[list] = [MODE_PLAY,MODE_CMP_PLAY,MODE_AGONY]

#Commands

CMD_UP     :Final[int]= 1
CMD_DOWN   :Final[int]= 2
CMD_LEFT   :Final[int]= 3
CMD_RIGHT  :Final[int]= 4
CMD_T_LEFT :Final[int]= 5
CMD_T_RIGHT:Final[int]= 6

SnakeStatus :Final = [
        "Small Worm",
        "Worm",
        "Big Worm",
        "Small Grass Snake",
        "Grass Snake",
        "Big Grass Snake",
        "Small Adder",
        "Adder",
        "Big Adder",
        "Small Rattle Snake",
        "Rattle Snake",
        "Big Rattle Snake",
        "Small Cobra",
        "Cobra",
        "Big Cobra",
        "Small Python",
        "Python",
        "Big Python",
        "Small Boa",
        "Boa",
        "Big Boa",
        "Small Dragon",
        "Dragon",
        "Big Dragon"
] 
SnakeStatusGroup = {
    "Worm"  : "worm.png",
    "Grass" : "grass.png",
    "Adder" : "adder.png",
    "Rattle": "rattle.png",
    "Cobra" : "cobra.png" ,
    "Python": "python.png",
    "Boa"   : "boa.png",
    "Dragon": "dragon.png"
}


#thems

# for ini
SECTION_GENERAL:Final[str] = "General"
SECTION_RULES  :Final[str] = "Rules"
KEY_SOUND      :Final[str] = "sound"
KEY_PLAYER     :Final[str] = "player"
KEY_THEME      :Final[str] = "theme"
KEY_GRID       :Final[str] = "grid"
KEY_LEVEL      :Final[str] = "level"
KEY_GROW_BY_FOOD_ONLY :Final[str] = "grow_by_food_only"
KEY_FOOD_ALWAYS:Final[str] = "food_always"
KEY_PLAY_MODE  :Final[str] = "PLAY_MODE"
KEY_SIZE       :Final[str] = "size"
KEY_FONT       :Final[str] = "font"
KEY_PLAY_MODE  :Final[str] = "play_mode"
KEY_ENEMY      :Final[str] = "enemy"
KEY_MAX_FOODS  :Final[str] = "max_foods" 
KEY_AI_MODE    :Final[str] = "ai_mode" 
KEY_TOTAL_GAMES:Final[str] = "gamecount"
KEY_HIGH_SCORE :Final[str] = "highscore"
KEY_AVG_SCORE  :Final[str] = "avgscore"
KEY_HIGH_SIZE  :Final[str] = "highsize"

W_BUTTON :Final[int] = 120
H_BUTTON :Final[int] = 50
  
AI      :Final[str] = 'AI'
HUMAN   :Final[str] = 'HUMAN'
TRAINING:Final[str] = "AI_TRAINING"

def is_ok(ret):
    return ret < ERROR_RET_VAL

def row_to_y(row):
    return row * CELL_SIZE + FIELD_BORDER_TOP

def col_to_x(col):
    return col * CELL_SIZE + FIELD_BORDER_LEFT

def set_shema(bk,field_clr,txt_clr,snake_body_clr,snake_head_clr,snake_eye_clr = RED,
              snake_tong_clr = RED,eye_pupil=BLUE,field_border = ORANGE,grid_color = None):
    global BK,FIELD_COLOR,TEXT_COLOR,SNAKE_BODY_COLOR,SNAKE_HEAD_COLOR
    global SNAKE_TONG_COLOR,GRID_COLOR,SNAKE_EYE_COLOR,FIELD_BORDER,EYE_PUPIL_COLOR
    
    BK = bk
    FIELD_COLOR      = field_clr
    TEXT_COLOR       = txt_clr
    SNAKE_BODY_COLOR = snake_body_clr
    SNAKE_HEAD_COLOR = snake_head_clr
    SNAKE_TONG_COLOR = snake_tong_clr
    if grid_color == None:
        GRID_COLOR = BK
    else:
        GRID_COLOR = grid_color      
    SNAKE_EYE_COLOR  = snake_eye_clr
    FIELD_BORDER     = field_border
    EYE_PUPIL_COLOR  = eye_pupil
  
def red_shema():
    set_shema(bk=RED,field_clr=RED_DARK,txt_clr=WHITE,snake_body_clr=BLUE,snake_head_clr=BLUE,
              snake_tong_clr=BLUE_DARK,snake_eye_clr=WHITE,eye_pupil=BLACK,field_border=BLUE)  

def green_shema():
    set_shema(bk=GREEN_DARK,field_clr=GREEN,txt_clr=WHITE,snake_body_clr=BLUE,snake_head_clr=BLUE)  

def gray_shema():
    set_shema(bk=GRAY_DARK,field_clr=GRAY,txt_clr=WHITE,snake_body_clr=GREEN,snake_head_clr=(16,255,16))   
    
def black_shema():
    set_shema(bk=BLACK,field_clr=BLACK,txt_clr=WHITE,snake_body_clr=RED,snake_head_clr=(255,64,64),
              snake_eye_clr=BLUE,eye_pupil=WHITE,grid_color= GRAY_DARK)   

def white_schema():
    set_shema(bk=WHITE,field_clr=GRAY_LIGHT,txt_clr=BLACK,snake_body_clr=BLACK,snake_head_clr=GRAY_DARK)    

def desert_schema():
    set_shema(bk=Control.BK,field_clr=GRAY_LIGHT,txt_clr=Control.CLR_TEXT,
              snake_body_clr=BLACK,snake_head_clr=GRAY_DARK,snake_eye_clr=RED,field_border=BLUE)  
    

def set_shema_by_name():
    theme = get_theme()
    if theme == Control.THEME_FOREST:
        green_shema()  
    elif theme == Control.THEME_GRAY:
        gray_shema()   
    elif theme == Control.THEME_RED:
        red_shema()   
    elif theme == Control.THEME_BLACK:
        black_shema()
    elif theme == Control.THEME_WHITE:
        white_schema()
    elif theme == Control.THEME_DESERT:
        desert_schema()
    else:
        set_shema(bk=Control.BK,field_clr=GRAY_LIGHT,txt_clr=Control.CLR_TEXT,snake_body_clr=BLACK,snake_head_clr=GRAY_DARK,snake_eye_clr=RED)     
        return False
    return True

SIZES = [
    (16,24),
    (24,34),
    (32,48),
]

SIZE_NAMES = [
    "Small",
    "Standard",
    "Large" 
]

LEVELS={
        "Easy"  :"0",
        "Medium":"1",
        "Hard"  :"2",
        "Crazy" :"3"
   }

ACTIONS = {
    "Your play"   :HUMAN,
    "AI play"     :AI,
    "AI training" :TRAINING
}

def set_boars_size(size_level):
    global ROWS,COLS,WIDTH,HEIGHT
    global FIELD_BORDER_TOP,FIELD_BORDER_BOTTOM,FIELD_BORDER_LEFT,FIELD_BORDER_RIGHT
    global HEIGHT_WINDOW,WIDTH_WOINDOW
    global CELL_SIZE,CELL_SIZE2

    r,c = SIZES[size_level] 
     
    if r == 16:
        CELL_SIZE = 32
    elif r == 24:
            CELL_SIZE = 22
    else:
        CELL_SIZE = 16

    CELL_SIZE2  = CELL_SIZE/2

    ROWS = r
    COLS = c

    WIDTH  = CELL_SIZE * COLS 
    HEIGHT = CELL_SIZE * ROWS

    #print(WIDTH,HEIGHT, WIDTH_WINDOW,HEIGHT_WINDOW)

    FIELD_BORDER_TOP    = (HEIGHT_WINDOW - HEIGHT)//2
    FIELD_BORDER_BOTTOM = (HEIGHT_WINDOW - HEIGHT)//2 
    #FIELD_BORDER_LEFT   = (WIDTH_WINDOW  - WIDTH)//2
    #FIELD_BORDER_RIGHT  = (WIDTH_WINDOW  - WIDTH)//2
    

def is_open(v):
    return v == FOOD_VAL or v == EMPTY_VAL

def is_closed(v):
    return v != FOOD_VAL and v != EMPTY_VAL 