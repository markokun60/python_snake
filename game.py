from asyncio.sslproto import add_flowcontrol_defaults
from pickle import FALSE
import pygame
import random
import os
import time
import configparser

import constants
import lib
from  snake import Snake
from  animatedSprite import AnimatedSprite

def draw_text(window,source,fnt ,other_height = 0):
    text = fnt.render(source,1,constants.TEXT_COLOR ) 
    x = int((constants.WIDTH_WOINDOW - text.get_width ())/2)
    y = int((constants.HEIGHT_WINDOW - text.get_height() - other_height)/2)
    if x < 0 :
        x = 0
    window.blit(text,(x,y))
    return y + text.get_height()

def draw_grid(window):
    for r in range(0,constants.ROWS): 
        y = constants.row_to_y(r)
        for c in range(0,constants.COLS): 
            x = constants.col_to_x(c)
            pygame.draw.rect(window,constants.GRID_COLOR,(x,y,constants.CELL_SIZE,constants.CELL_SIZE),1)

def draw_welcome_text(window,fnt):
    source = """
You are a snake. The goal of the game is grow, grow and grow.
To grow you need a food. 
This won\'t the problems for you: a lot of tasty rabbits will be around.

But be caution! 
The mongooses are need food too and you are their favorite food.

Others very dangerous spots for you are the edges of the field. 
You can\'t live without moving.
The edge stops and kills you.

Press SPACE or button "Start" to play
"""
    return draw_text(window,source,fnt)


class Game:  
    def __init__(self,big_text_font,info_text_font):
        self.is_sound = True
        self.is_grid  = False
        self.is_grow_by_food_only = False
        self.is_food_always = True
        self.player_name = 'user'
        self.theme    = constants.THEME_GRAY
        self.level    = 0
        self.read_config()
        constants.set_shema_by_name(self.theme)

        self.big_text_font = big_text_font
        self.info_text_font= info_text_font
        self.field = [[0 for x in range(constants.COLS)] for y in range(constants.ROWS)]
        self.snake = Snake(self.field)
        self.grave = AnimatedSprite()

        self.FOOD_IMAGE  = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'food.png'))
        self.ENEMY_IMAGE = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'enemy.png'))
        self.SNAKE_IMAGE = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'snake.png'))

        self.FOOD_IMAGE  = pygame.transform.scale(self.FOOD_IMAGE,(constants.CELL_SIZE,constants.CELL_SIZE))
        self.ENEMY_IMAGE = pygame.transform.scale(self.ENEMY_IMAGE,(constants.CELL_SIZE,constants.CELL_SIZE))

        self.WALL_SOUND  = pygame.mixer.Sound(os.path.join(constants.SOUND_FOLDER,'wall.mp3'))
        self.FOOD_SOUND  = pygame.mixer.Sound(os.path.join(constants.SOUND_FOLDER,'eat.mp3'))

        self.steps_to_create_enemy = constants.STEPS_TO_CREATE_ENEMY
        self.steps_to_create_food  = constants.STEPS_TO_CREATE_FOOD 
        self.not_grow_moves_count = 0
        self.food_step = 0
        self.total_enemies = 0
        self.total_foods   = 0
        self.prompt = ""
        self.prompt_time = time.time()

        self.elapsed_time = 0   
        self.paused_time  = 0
        self.start_time = time.time()
        self.commands = []
        self.status = 0
        self.highscore   = 0
        self.total_games = 0 
        self.avg_score   = 0.0
        self.load_statistics()
       
            
        #print(f"high score {self.highscore}")

    def start(self):
        self.elapsed_time = 0  
        self.paused_time  = 0
        self.start_time = time.time()
        self.pause_started = None
        self.total_games += 1
        self.status = 0
        self.commands.clear()
        self.snake.start()
        if self.is_food_always:
            self.create_food()

        self.set_prompt("Game started")

    def pause_resume(self):
        self.snake.is_paused = not self.snake.is_paused
        if self.snake.is_paused:
             self.pause_started = time.time()
             self.set_prompt("Game paused")
        else: 
            self.set_prompt("Game resumed")

    def get_time(self):
       if self.snake.mode == constants.MODE_PLAY:
            if self.snake.is_paused:
                self.paused_time   = time.time() - self.pause_started
            self.elapsed_time = time.time() - self.start_time  -  self.paused_time

    def step(self): 
        is_grow = False
        if self.food_step > 0:
            is_grow = True
            self.food_step -= 1
        elif self.not_grow_moves_count == 10 and not self.is_grow_by_food_only:
            is_grow = True
            self.not_grow_moves_count = 0
        cmd = 0
        if len(self.commands) > 0:
            cmd = self.commands.pop()
            x = 0
            y = 0
            if cmd == constants.CMD_LEFT: x -= 1
            elif cmd == constants.CMD_RIGHT:x += 1
            elif cmd == constants.CMD_UP: y -= 1
            elif cmd == constants.CMD_DOWN: y += 1
            elif cmd == constants.CMD_T_LEFT:
                x,y = self.turn_left()
            elif cmd == constants.CMD_T_RIGHT:
                x,y = self.turn_right()

            if x != 0 or y != 0:
                self.snake.x_velocity = x
                self.snake.y_velocity = y

        if is_grow:
            res = self.snake.grow()                
        else:
            res = self.snake.move()
            if self.food_step == 0:
                if constants.is_ok(res):
                    self.not_grow_moves_count += 1
                    #self.set_prompt(f"You become bigger: {self.snake.get_size()}")

        if constants.is_ok(res):
            gs = self.snake.get_status()
            if gs != self.status:
                self.status = gs
                self.set_prompt(f"You are {constants.SnakeStatus[self.status]}")
            

        if res == constants.FOOD_RET_VAL:
            self.food_step = 10
            self.total_foods -= 1
            if self.is_sound:
                self.FOOD_SOUND.play()
            if self.total_foods == 0 and self.is_food_always:
                self.create_food()
            else:
                self.set_prompt("Food eaten")

        elif not constants.is_ok(res): 
            if self.is_sound:
                self.WALL_SOUND.play()
            (r,c) = self.snake.get_head()
            print(f"Snake is dead {r,c}")
            if r > 10:
                r -= 2
            else:
                r += 2

            if c > 10:
                c -= 2
            else:
                c += 2
        
            x = constants.col_to_x(c)
            y = constants.row_to_y(r)

            self.grave.set_xy(x,y)
            score = self.snake.get_size()
            sum_score = self.avg_score * (self.total_games-1)
            sum_score += score

            self.avg_score = sum_score / self.total_games
            if score > self.highscore:
                self.highscore = score
                self.set_prompt(f"Game over: {self.snake.message}. You finished with highest score. Click SPACE to continue")
            else:
                self.set_prompt(f"Game over: {self.snake.message}. Click SPACE to continue")
            self.save_statistics()    
           
        if self.steps_to_create_food == 0:       
            self.steps_to_create_food =  constants.STEPS_TO_CREATE_FOOD 
            self.create_food()
        else:
            self.steps_to_create_food -= 1

        if self.steps_to_create_enemy == 0:       
            self.steps_to_create_enemy = constants.STEPS_TO_CREATE_ENEMY 
            self.create_enemy()
        else:
            self.steps_to_create_enemy -= 1

        if len(self.prompt) > 0:
            now = time.time()
            if now - self.prompt_time > 3:
                self.prompt = ""
        return res

    def set_prompt(self,txt):
        self.prompt = txt
        self.prompt_time = time.time()

    def get_free_cells(self):
        cells = []
        for r in range(0,constants.ROWS):
            for c in range(0,constants.COLS):
                if self.field[r][c] == constants.EMPTY_VAL:
                    cells.append((r,c))
        return cells

    def create_item(self,val):
        cells = self.get_free_cells()
        n = len(cells)
        if n == 0:
            return False
        n = random.randint(0,n-1)
        (r,c) = cells[n]
        self.field[r][c] = val
        return True
                    

    def create_food(self):
        if self.create_item(constants.FOOD_VAL):      
            self.set_prompt("New food")
            self.total_foods += 1
            return True
        return False
  
    def create_enemy(self):
        if self.total_enemies < constants.MAX_ENEMIES: 
            if self.create_item(constants.ENEMY_VAL):  
                self.total_enemies += 1
                if self.total_enemies < constants.MAX_ENEMIES:
                    self.set_prompt("New mongoose")
                else:
                    self.set_prompt("New mongoose. This is the last one")


    def turn_left(self):
        x = self.snake.x_velocity
        y = self.snake.y_velocity

        if x < 0 and y == 0: #left
            return (0,1) #down

        if x == 0 and y > 0: #down
            return (1,0) #right

        if x > 0 and y == 0: #right
            return (0,-1) #up

        if x == 0 and y < 0: #up
            return (-1,0) #right

        return (0,0)

    def turn_right(self):
        x = self.snake.x_velocity
        y = self.snake.y_velocity

        if x < 0 and y == 0: #left
            return (0,-1) #up

        if x == 0 and y < 0: #up
            return (1,0) #right

        if x > 0 and y == 0: #right
            return (0,1) #down

        if x == 0 and y > 0: #down
            return (-1,0) #left

        return (0,0)

    def draw_progress(self,window):
        x      = 4
        y      = constants.FIELD_BORDER_TOP
        width  = constants.FIELD_BORDER_LEFT - x * 2
        height = constants.HEIGHT
        done = self.snake.get_progress()
        wDone = int(height * done) 
        pygame.draw.rect(window,constants.SNAKE_BODY_COLOR,(x,y,width,wDone))
        #y += wDone
        #height -= wDone
        #pygame.draw.rect(window,constants.BK,(x,y,width,height))
     
    def draw_field(self,window):
        self.draw_progress(window)
        if self.is_grid :
            draw_grid(window)
        for r in range(0,constants.ROWS): 
            y = y = constants.row_to_y(r)
            for c in range(0,constants.COLS):
                val = self.field[r][c]
                if val == constants.EMPTY_VAL:
                    continue
                x = constants.col_to_x(c)
                if val == constants.FOOD_VAL:
                    window.blit(self.FOOD_IMAGE,(x,y))
                elif val == constants.ENEMY_VAL:
                    window.blit(self.ENEMY_IMAGE,(x,y))
        self.snake.draw(window)
        
       
        #window.blit(text,(x,y))


    def draw_time(self,window):
        source = f"Time: {round(self.elapsed_time)} s"
        text = self.info_text_font.render(source,1,constants.TEXT_COLOR ) 
        x = 0
        y = 0
        window.blit(text,(x,y))

    def draw_score(self,window):
        score = self.snake.get_size()
        score *= (self.level + 1)
        source = f"Score: {score}"
        text   = self.info_text_font.render(source,1,constants.TEXT_COLOR ) 
        x = constants.WIDTH_WOINDOW-10
        y = 0
        window.blit(text,(x-text.get_width(),y))

    def draw_status(self,window):
        if self.snake.is_paused:
            source = "Paused. Click SPACE to continue"
        else:
            source = constants.SnakeStatus[self.status]

        text   = self.info_text_font.render(source,1,constants.TEXT_COLOR ) 
        x = constants.WIDTH_WOINDOW/2
        y = 0
        window.blit(text,(x-text.get_width()/2,y))

    def draw_smake_img(self,window,y):
        x = int(constants.WIDTH_WOINDOW - self.SNAKE_IMAGE.get_width())/2
        window.blit(self.SNAKE_IMAGE,(x,y))

    def draw_prompt(self,window):
        if len(self.prompt) > 0:
            text = self.info_text_font.render(self.prompt,1,constants.TEXT_COLOR ) 
            y = constants.HEIGHT_WINDOW - text.get_height()
            window.blit(text,(0,y))

    def draw_about_text(self,window):
        source = f"""
Snake.
Version 1.0.0
Made by Mark Okun

Total games: {self.total_games}
High score:  {self.highscore}
Avg score:   {round(self.avg_score,2)}
        """
        y = draw_text(window,source,self.big_text_font,self.SNAKE_IMAGE.get_height())
        y += 10
        self.draw_smake_img(window,y)

    def draw_help_text(self,window):
        source = """
To move the snake you can use

To turn
  z - anticlockwise
  x - clockwise
To move  - use arrow keys
To pause/resume - space

To start new game press - space
    """

        y = draw_text(window,source,self.big_text_font)
        self.draw_smake_img(window,y)

    def draw_play(self,window):
        self.draw_time(window)
        self.draw_status(window)
        self.draw_score(window)
        self.draw_field(window)
        if self.snake.mode >= constants.MODE_AGONY:
            self.grave.draw(window)
        self.draw_prompt(window)

    def save_statistics(self):
        file_path = os.path.join(constants.DATA_FOLDER,self.player_name + "_"+ constants.SCORE_FILE)
        with open(file_path, "w") as file:
            file.write(f'{constants.KEY_HIGH_SCORE} = {self.highscore}\n')
            file.write(f'{constants.KEY_TOTAL_GAMES} = {self.total_games}\n')
            file.write(f'{constants.KEY_AVG_SCORE} = {self.avg_score}\n')

    def load_statistics(self):

        file_path = os.path.join(constants.DATA_FOLDER,self.player_name + "_"+ constants.SCORE_FILE)
        if os.path.isfile(file_path):
            values = lib.read_variables_from_file(file_path)
            for key in values.keys():
                if key==constants.KEY_TOTAL_GAMES:
                    self.total_games = int(values[key])
                elif key == constants.KEY_HIGH_SCORE:
                    self.highscore = int(values[key])
                elif key == constants.KEY_AVG_SCORE:
                    self.avg_score = float(values[key])
                    

    def save_config(self):
        file_path = os.path.join(constants.DATA_FOLDER,constants.SETTINGS_FILE)
        config = configparser.ConfigParser()
        config[constants.SECTION_GENERAL] = {
            constants.KEY_SOUND : self.is_sound,
            constants.KEY_PLAYER: self.player_name,
            constants.KEY_THEME : self.theme,
            constants.KEY_GRID  : self.is_grid,
            constants.KEY_LEVEL : self.level
        }
        config[constants.SECTION_RULES] = {
            constants.KEY_GROW_BY_FOOD_ONLY : self.is_grow_by_food_only,
            constants.KEY_FOOD_ALWAYS       : self.is_food_always
        }
   
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    def read_config(self):
        file_path = os.path.join(constants.DATA_FOLDER,constants.SETTINGS_FILE)
        if not os.path.isfile(file_path):
            self.save_config()
            return
        config = configparser.ConfigParser()
        config.read(file_path)
        section = constants.SECTION_GENERAL
        self.is_sound    = config.getboolean(section, constants.KEY_SOUND , fallback=self.is_sound )
        self.is_grid     = config.getboolean(section, constants.KEY_GRID  , fallback=self.is_grid )
        self.player_name = config.get       (section, constants.KEY_PLAYER, fallback=self.player_name)
        
        theme = config.get       (section, constants.KEY_THEME , fallback=self.theme)
        if theme in constants.THEMES:
            self.theme = theme

        self.level = config.getint    (section, constants.KEY_LEVEL , fallback=self.level)
        section = constants.SECTION_RULES
        self.is_grow_by_food_only = config.getboolean(section, constants.KEY_GROW_BY_FOOD_ONLY , fallback=self.is_grow_by_food_only )
        self.is_food_always       = config.getboolean(section, constants.KEY_FOOD_ALWAYS       , fallback=self.is_food_always )
