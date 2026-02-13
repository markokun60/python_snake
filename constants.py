from typing import Final

#Collors

RED         = (255, 0, 0)
RED_DARK    = (127, 0, 0)
ORANGE      = (255,127,0)
GREEN       = (0, 255, 0)
GREEN_DARK  = (0,127,0)
BLUE        = (0, 0, 255)
BLUE_DARK   = (0, 0, 127)
CYAN        = (0, 100, 100)
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
GRAY        = (127,127,127) 
GRAY_DARK   = (64,64,64)
GRAY_LIGHT  = (212,212,212)

#
# THEME
#
TEXT_COLOR  = WHITE
BK          = GRAY_DARK
FIELD_COLOR = GRAY 
SNAKE_BODY_COLOR = GREEN
SNAKE_HEAD_COLOR = GREEN_DARK
SNAKE_TONG_COLOR = RED
GRID_COLOR = BK

VELOCITIES = [(-1,0),(1,0),(0,-1),(1,0)]
FONTS      = 'Arial, Helvetica, sans-serif'
 
# cells values
EMPTY_VAL:Final[int] = 0
SNAKE_VAL:Final[int] = 1
FOOD_VAL :Final[int] = 2
ENEMY_VAL:Final[int] = 3

# return values

OK_RET_VAL    :Final[int]  = 0
FOOD_RET_VAL  :Final[int]  = 1
ERROR_RET_VAL :Final[int] = 10
BORDER_RET_VAL:Final[int] = ERROR_RET_VAL + 1
BODY_RET_VAL  :Final[int] = ERROR_RET_VAL + 2
EMENY_RET_VAL :Final[int] = ERROR_RET_VAL + 3

#geometric vaalues
CELL_SIZE  = 16
CELL_SIZE2 = CELL_SIZE/2
ROWS = 32
COLS = 48

WIDTH  = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS

FIELD_BORDER_TOP    :Final[int]= 32
FIELD_BORDER_BOTTOM :Final[int]= 20
FIELD_BORDER_LEFT   :Final[int]= 20
FIELD_BORDER_RIGHT  :Final[int]= 20

WIDTH_WOINDOW = WIDTH  + FIELD_BORDER_LEFT + FIELD_BORDER_RIGHT
HEIGHT_WINDOW = HEIGHT + FIELD_BORDER_TOP  + FIELD_BORDER_BOTTOM

#Folders

ASSET_FOLDER = 'assets'
SOUND_FOLDER = 'sounds'
DATA_FOLDER  = 'data'

#Files
SCORE_FILE   = "highscore.txt"
SETTINGS_FILE= "snake.ini"

#game properties

MAX_ENEMIES          :Final[int] = 10
STEPS_TO_CREATE_FOOD :Final[int] = 100
STEPS_TO_CREATE_ENEMY:Final[int] = 220

#modes

MODE_PLAY   = 0
MODE_WELCOME= 1
MODE_ABOUT  = 2
MODE_HELP   = 3
MODE_AGONY  = 4
MODE_GAME_OVER = 5
MODE_EXIT  = 6

#Commands

CMD_UP   = 1
CMD_DOWN = 2
CMD_LEFT = 3
CMD_RIGHT= 4
CMD_T_LEFT=5
CMD_T_RIGHT=6

SnakeStatus = [
        "Small Worm",
        "Worm",
        "Big Worm",
        "Small Grass Snake",
        "Grass Snake",
        "Big Grass Snake",
        "Small Adder",
        "Adder",
        "Big Adder",
        "Small Ruttle Snake",
        "Ruttle Snake",
        "Big Snake",
        "Small Cobra",
        "Cobra",
        "Big Cobra",
        "Small Python",
        "Python",
        "Big Python",
        "Small Dragon",
        "Dragon",
        "Big Dragon"] 
#thems

THEME_RED    = "Mars"
THEME_FOREST = "Forest"
THEME_GRAY   = "Gray"
THEME_BLACK  = "Night"
THEME_WHITE  = "Snow"

THEMES = [THEME_BLACK,THEME_FOREST,THEME_GRAY,THEME_RED,THEME_WHITE]

# for ini
SECTION_GENERAL = "General"
SECTION_RULES   = "Rules"
KEY_SOUND  = "sound"
KEY_PLAYER = "player"
KEY_THEME  = "theme"
KEY_GRID   = "grid"
KEY_LEVEL  = "level"
KEY_GROW_BY_FOOD_ONLY = "grow_by_food_only"
KEY_FOOD_ALWAYS       = "food_always"

# for statictics
KEY_TOTAL_GAMES = "gamecount"
KEY_HIGH_SCORE  = "highscore"
KEY_AVG_SCORE   = "avgscore"

def is_ok(ret):
    return ret < ERROR_RET_VAL

def row_to_y(row):
    return row * CELL_SIZE + FIELD_BORDER_TOP

def col_to_x(col):
    return col * CELL_SIZE + FIELD_BORDER_LEFT

def set_shema(bk,field_clr,txt_clr,snake_body_clr,snake_head_clr,snake_tong_clr = RED):
    global BK,FIELD_COLOR,TEXT_COLOR,SNAKE_BODY_COLOR,SNAKE_HEAD_COLOR,SNAKE_TONG_COLOR,GRID_COLOR
    BK = bk
    FIELD_COLOR      = field_clr
    TEXT_COLOR       = txt_clr
    SNAKE_BODY_COLOR = snake_body_clr
    SNAKE_HEAD_COLOR = snake_head_clr
    SNAKE_TONG_COLOR = snake_tong_clr
    GRID_COLOR       = BK

def red_shema():
    set_shema(RED,ORANGE,WHITE,BLUE,BLUE,BLUE_DARK)  

def green_shema():
    set_shema(GREEN_DARK,GREEN,WHITE,BLUE,BLUE)  

def gray_shema():
    set_shema(GRAY_DARK,GRAY,WHITE,GREEN,GREEN_DARK) 
    
def black_shema():
    global GRID_COLOR
    set_shema(BLACK,BLACK,WHITE,RED,RED_DARK) 
    GRID_COLOR = GRAY_DARK

def white_schema():
    set_shema(WHITE,GRAY_LIGHT,BLACK,BLACK,GRAY_DARK) 

def set_shema_by_name(theme):
    if theme == THEME_FOREST:
        green_shema()  
    elif theme == THEME_GRAY:
        gray_shema()   
    elif theme == THEME_RED:
        red_shema()   
    elif theme == THEME_BLACK:
        black_shema()
    elif theme == THEME_WHITE:
        white_schema()
    else:
        return False
    return True
