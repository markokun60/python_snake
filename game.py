import pygame
import random
import os
from   time import time
from   configparser import ConfigParser
from   importlib.resources import files

import constants
from   summary import SummaryValues
from   controls.controls  import Control,set_contols_mode,get_theme
from   form_options import WIDTH_WINDOW
from   snake import Snake
from   animatedSprite import Grave,Enemy,SnakeImage
from   item import Item
from   lib  import bool_to_str
from welcome_message import WelcomeMessage

def draw_text(window,source,fnt ,other_height = 0):
    text = fnt.render(source,1,constants.TEXT_COLOR ) 
    x = int((constants.WIDTH_WINDOW - text.get_width ())/2)
    y = int((constants.HEIGHT_WINDOW - text.get_height() - other_height)/2)
    if x < 0 :
        x = 0
    window.blit(text,(x,y))
    return y + text.get_height()


class Game:  
    def __init__(self,window,resource_folder):
        self.window   = window
        self.resource_folder = resource_folder
        self.is_sound = True
        self.is_grid  = False
        self.is_grow_by_food_only = False
        self.is_food_always = True
        self.is_enemies     = False
        self.max_foods_on_fields = 1
        self.play_mode     = constants.HUMAN
        self.ai_with_learning = False
        self.player_name   = 'user'
        self.level         = 0
        self.board_size    = 0
        self.rect          = None
        self.steps_to_grow = 10

        self.best_status   = 0
        self.total_games   = 0

        os.makedirs(constants.DATA_FOLDER, exist_ok=True)  
        try:
            self.read_config()
        except:
            self.save_config()

        constants.set_shema_by_name()

        self.big_text_font  = pygame.font.SysFont(Control.FONT, 18,italic = True )
        self.info_text_font = pygame.font.SysFont(Control.FONT, 16,bold=True)
        
        self.field = [[0 for x in range(constants.COLS)] for y in range(constants.ROWS)]
        self.items = {}

        self.snake = Snake(self.field)
        self.grave = Grave(self.resource_folder)

        self.SNAKE_IMAGE  = pygame.image.load( os.path.join(self.resource_folder,'snake.png')).convert_alpha()
        #self.WELCOME_IMAGE= pygame.image.load( os.path.join(self.resource_folder,'cobra.png')).convert_alpha()
        self.AI_TRAINING_IMAGE= pygame.image.load( os.path.join(self.resource_folder,'ai_training.png')).convert_alpha()
        self.AI_IMAGE= pygame.image.load( os.path.join(self.resource_folder,'ai.png')).convert_alpha() 

        self.WALL_SOUND   = pygame.mixer.Sound(os.path.join(self.resource_folder,constants.SOUND_FOLDER,'wall.mp3'))
        self.FOOD_SOUND   = pygame.mixer.Sound(os.path.join(self.resource_folder,constants.SOUND_FOLDER,'eat.mp3'))

        self.level_group_images = {}
        for z in constants.SnakeStatusGroup.keys():
            im = constants.SnakeStatusGroup[z]
            img = pygame.image.load(os.path.join(self.resource_folder,"levels",im)).convert_alpha()

            #img = pygame.transform.smoothscale(img,(38,21))
            self.level_group_images[z] = img

        self.snake_image = SnakeImage(self.resource_folder)

        self.steps_to_create_enemy = constants.STEPS_TO_CREATE_ENEMY
        self.steps_to_create_food  = constants.STEPS_TO_CREATE_FOOD 
        self.not_grow_moves_count = 0
        self.food_step     = 0
        self.total_enemies = 0
        self.total_foods   = 0
        self.prompt = ""
        self.prompt_time = time()

        self.elapsed_time = 0   
        self.paused_time  = 0
        self.start_time = time()
        self.commands = []
        self.status   = 0
        self.is_egg   = True
        # 
        self.load_statistics()
        self.for_board_size()
   
        self.font_small = pygame.font.SysFont(Control.FONT,12)           
        #print(f"high score {self.highscore}")

    def for_board_size(self):
        constants.set_boars_size(self.board_size)
        self.rect = pygame.Rect(constants.FIELD_BORDER_LEFT,constants.FIELD_BORDER_TOP,constants.WIDTH,constants.HEIGHT)
        self.load_images()

    def set_default(self):
        self.is_sound = True
        self.is_grid  = False
        self.is_grow_by_food_only = False
        self.is_food_always = True
        self.is_enemies     = True
        self.max_foods_on_fields = False
        self.play_mode = constants.HUMAN
        self.ai_with_learning = False

    def save_settings(self):
        values = {
            constants.KEY_PLAYER: self.player_name,
            constants.KEY_SOUND : bool_to_str(self.is_sound),
            constants.KEY_GRID  : bool_to_str(self.is_grid),
            constants.KEY_LEVEL : self.level,
            constants.KEY_SIZE  : self.board_size,
            constants.KEY_GROW_BY_FOOD_ONLY : bool_to_str(self.is_grow_by_food_only),
            constants.KEY_FOOD_ALWAYS       : bool_to_str(self.is_food_always),
            constants.KEY_ENEMY             : bool_to_str(self.is_enemies),
            constants.KEY_MAX_FOODS         : self.max_foods_on_fields,
            constants.KEY_PLAY_MODE         : self.play_mode    
        }
        return values

    def restore_settings(self,values):
        self.player_name = values[constants.KEY_PLAYER]
        self.is_sound  = True if values[constants.KEY_SOUND] == 'Y' else False
        self.is_grid   = True if values[constants.KEY_GRID]  == 'Y' else False
        self.level     = values[constants.KEY_LEVEL]
        self.board_size= values[constants.KEY_SIZE]
        self.is_grow_by_food_only = True if values[constants.KEY_GROW_BY_FOOD_ONLY]  == 'Y' else False
        self.is_food_always       = True if values[constants.KEY_FOOD_ALWAYS]        == 'Y' else False 
        self.is_enemies           = True if values[constants.KEY_ENEMY]              == 'Y' else False 
        self.max_foods_on_fields  = values[constants.KEY_MAX_FOODS]
        self.play_mode  = values[constants.KEY_PLAY_MODE]

    def reset(self):
        self.big_text_font  = pygame.font.SysFont(Control.FONT, 18,italic = True )
        self.info_text_font = pygame.font.SysFont(Control.FONT, 16,bold=True)

    def load_images(self):
        self.FOOD_IMAGE  = pygame.image.load(os.path.join(self.resource_folder,'food.png')).convert_alpha()
        self.ENEMY_IMAGE = pygame.image.load(os.path.join(self.resource_folder,'enemy.png')).convert_alpha()

        self.FOOD_IMAGE  = pygame.transform.scale(self.FOOD_IMAGE ,(constants.CELL_SIZE,constants.CELL_SIZE))
        self.ENEMY_IMAGE = pygame.transform.scale(self.ENEMY_IMAGE,(constants.CELL_SIZE,constants.CELL_SIZE))

        self.enemy_images = []
        for i in range(0,4):
            img_path = os.path.join(self.resource_folder,'enemy',f'{i}.png')
            image = pygame.image.load(img_path).convert_alpha()
            #image.set_colorkey((163, 73, 164))
            image = pygame.transform.scale(image,(constants.CELL_SIZE,constants.CELL_SIZE))
            self.enemy_images.append(image)

    def set_board_size(self,i:int):
        self.board_size = i
        self.summary = self.summaryValues[self.board_size]
       
    def start(self):
        self.snake.is_report = not self.play_mode == constants.TRAINING
        #self.snake.is_report = True
        self.elapsed_time = 0  
        self.paused_time  = 0
        self.total_foods  = 0
        self.start_time   = time()
        self.pause_started = None
        if self.play_mode != constants.TRAINING:
            self.summary.total_games[self.play_mode] += 1
            self.total_games += 1
            self.is_egg  = True
        self.step_no = 0
        self.status = 0
        self.items.clear()
        self.commands.clear()   

        self.snake.start(self.play_mode == constants.AI)
        if self.is_food_always or self.is_grow_by_food_only:
            self.create_food()

        if self.snake.is_report:
            self.set_prompt("Game started")
        #self.create_enemy()


    def end_of_game(self):
        if self.is_sound:
            self.WALL_SOUND.play()
        (r,c) = self.snake.get_head()
        if self.snake.is_report:
            print(f"Snake is dead {r,c}")
        grave_d = 1
        if r > 10:
            r -= grave_d
        else:
            r += grave_d

        if c > 10:
            c -= grave_d
        else:
            c += grave_d
        
        x = constants.col_to_x(c)
        y = constants.row_to_y(r)

        self.grave.set_xy(x,y)
        snake_size = self.snake.get_size()

        status = self.snake.get_status()
        if status > self.best_status:
            self.best_status = status


        score = snake_size * (self.level + 1)
           
        if self.summary.new_score(score,self.play_mode,snake_size):
            if self.play_mode == constants.AI:
                self.set_prompt(f"Game over: {self.snake.message}. AI finished with highest score. Click SPACE to continue")
            else:
                self.set_prompt(f"Game over: {self.snake.message}. You finished with highest score. Click SPACE to continue")
        else:
            self.set_prompt(f"Game over: {self.snake.message}. Click SPACE to continue")     
        self.save_statistics()

    def input_enabled(self):
        if self.snake.is_paused: return False
        if self.snake.mode != constants.MODE_PLAY: return False
        if self.is_egg: return False
        return True

    def get_snake_image_for_status(self,status):
        i = int(status / 3)
        return self.snake_image.images[i]

    def pause_resume(self):
        self.snake.is_paused = not self.snake.is_paused
        if self.snake.is_paused:
            self.pause_started = time()
            self.set_prompt("Game paused")
            #print(self.snake.get_state())
        else: 
            self.set_prompt("Game resumed")

    def get_time(self):
       if self.snake.mode == constants.MODE_PLAY:
            if self.snake.is_paused:
                self.paused_time   = time() - self.pause_started
            self.elapsed_time = time() - self.start_time  -  self.paused_time

    def step(self): 
        if self.is_egg:
            if time() - self.start_time <= 1.0:
                return 
            self.is_egg = False
        
        self.step_no += 1
        is_grow = False
        if self.food_step > 0:
            is_grow = True
            self.food_step -= 1
        elif self.not_grow_moves_count == self.steps_to_grow and not self.is_grow_by_food_only:
            is_grow = True
            #self.set_prompt("Small grow")
            self.not_grow_moves_count = 0
        cmd = 0
        if len(self.commands) > 0:
            cmd = self.commands.pop()
            x = 0
            y = 0
            if   cmd == constants.CMD_LEFT: x -= 1
            elif cmd == constants.CMD_RIGHT:x += 1
            elif cmd == constants.CMD_UP:   y -= 1
            elif cmd == constants.CMD_DOWN: y += 1
            elif cmd == constants.CMD_T_LEFT:
                x,y = self.snake.turn_left()
            elif cmd == constants.CMD_T_RIGHT:
                x,y = self.snake.turn_right()

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
                if self.snake.is_report:
                    self.set_prompt(f"You are {constants.SnakeStatus[self.status]}")
            
            if res == constants.FOOD_RET_VAL:
                (r,c) = self.snake.get_head()
                i = r * constants.COLS + c
                del(self.items[i])
                self.food_step = self.snake.grow_by_food_size
                self.total_foods -= 1
                if self.is_sound:
                    self.FOOD_SOUND.play()
                if self.total_foods == 0 and (self.is_food_always or self.is_grow_by_food_only):
                    self.create_food()
                elif self.snake.is_report:
                    self.set_prompt("Food eaten")

        elif self.play_mode != constants.TRAINING :             
            self.end_of_game()    
           
        if self.steps_to_create_food == 0:       
            self.steps_to_create_food =  constants.STEPS_TO_CREATE_FOOD 
            self.create_food()
        else:
            self.steps_to_create_food -= 1

        if self.is_enemies:
            if self.steps_to_create_enemy == 0:       
                self.steps_to_create_enemy = constants.STEPS_TO_CREATE_ENEMY 
                self.create_enemy()
            else:
                self.steps_to_create_enemy -= 1

        if self.snake.is_report:
            if len(self.prompt) > 0:
                now = time()
                if now - self.prompt_time > 3:
                    self.prompt = ""
        return res

    def set_prompt(self,txt):
        self.prompt = txt
        self.prompt_time = time()

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

        i = r *constants.COLS + c
        if val == constants.FOOD_VAL:
            self.items[i] = Item(self.FOOD_IMAGE, r,c)
        elif val == constants.ENEMY_VAL:
            self.items[i] = Enemy(self.enemy_images, r,c)
        return True
                    
    def create_food(self):
        if self.total_foods >= self.max_foods_on_fields and self.max_foods_on_fields > 0:
            return False
        
        if self.create_item(constants.FOOD_VAL):   
            if self.snake.is_report:   
                self.set_prompt("New food")
            self.total_foods += 1
            return True
        return False
  
    def create_enemy(self):
        if self.total_enemies < constants.MAX_ENEMIES: 
            if self.create_item(constants.ENEMY_VAL):  
                self.total_enemies += 1
                if self.snake.is_report:
                    if self.total_enemies < constants.MAX_ENEMIES:
                        self.set_prompt("New mongoose")
                    else:
                        self.set_prompt("New mongoose. This is the last one")

    def get_high_status_name(self,code):
        size = self.summary.highsize[code]
        if size == 0:
            return 'Egg'
        status=  self.snake.get_status(size)
        return constants.SnakeStatus[status]

    def draw_progress(self,window):
        x      = 4
        xImg   = 20
        y      = constants.FIELD_BORDER_TOP
        #width  = constants.FIELD_BORDER_LEFT - x * 2
        #if width > constants.CELL_SIZE:
        #    width = constants.CELL_SIZE
        #    x = (constants.FIELD_BORDER_LEFT - width)/2
        width = xImg - x
        height = constants.HEIGHT
        done = self.snake.get_progress()
        wDone = int(height * done)  
        pygame.draw.rect(window,constants.SNAKE_BODY_COLOR,(x,y,width,wDone))
        
        n = len(constants.SnakeStatusGroup)
        h = height / n

        for z in constants.SnakeStatusGroup:
            #pygame.draw.rect(window,(0,0,255),(x,y,width,3))  
            window.blit(self.level_group_images[z],(xImg,y))
            y += h

        #y += wDone
        #height -= wDone
        #pygame.draw.rect(window,constants.BK,(x,y,width,height))

    def draw_grid(self,window):
        is_cord = constants.IS_DEV
        for r in range(0,constants.ROWS): 
            y = constants.row_to_y(r)
            for c in range(0,constants.COLS): 
                x = constants.col_to_x(c)
                pygame.draw.rect(window,constants.GRID_COLOR,(x,y,constants.CELL_SIZE,constants.CELL_SIZE),1)
                if is_cord:
                    if c == 0:
                        t = self.font_small.render(str(r),1,Control.CLR_TEXT)
                        window.blit(t,(x ,y+4))
                    elif r == 0:
                        t = self.font_small.render(str(c),1,Control.CLR_TEXT)
                        window.blit(t,(x+4,y+2))
                        

    def draw_field(self,window):
        self.draw_progress(window)
        if self.is_grid :
            self.draw_grid(window)

        for r in range(self.snake.rows): 
            y = constants.row_to_y(r)
            for c in range(self.snake.cols):
                val = self.field[r][c]
                if val == constants.EMPTY_VAL:
                    continue
                elif val in (constants.FOOD_VAL,constants.ENEMY_VAL):  
                    x = constants.col_to_x(c)
                    i = r *constants.COLS + c
                    self.items[i].draw(window)
                #if val == constants.FOOD_VAL:
                #    #window.blit(self.FOOD_IMAGE,(x,y))
                #   
                #    self.item[i].draw(window)
                #elif val == constants.ENEMY_VAL:
                #    window.blit(self.ENEMY_IMAGE,(x,y))
        
        if self.is_egg:
            self.draw_egg(window)
        else:
            self.snake.draw(window)
        pygame.draw.rect(window,constants.FIELD_BORDER,(constants.FIELD_BORDER_LEFT-1,constants.FIELD_BORDER_TOP-1,constants.WIDTH+2,constants.HEIGHT+2),2) 
       
        #window.blit(text,(x,y))

    def draw_egg(self,window):
        (r,c) = self.snake.get_head()
        x = constants.col_to_x(c) + constants.CELL_SIZE // 4
        y = constants.row_to_y(r)
        rect = pygame.Rect(x,y,constants.CELL_SIZE2,constants.CELL_SIZE)
        pygame.draw.ellipse(window,constants.WHITE,rect)


    def draw_time(self,window):
        source = f"Time: {round(self.elapsed_time)} s"
        text = self.info_text_font.render(source,1,constants.TEXT_COLOR ) 
        x = constants.FIELD_BORDER_LEFT
        y = 0
        window.blit(text,(x,y))

    def draw_score(self,window):
        score = self.snake.get_size()
        score *= (self.level + 1)
        source = f"Score: {score}"
        text   = self.info_text_font.render(source,1,constants.TEXT_COLOR ) 
        x = constants.WIDTH_WINDOW-10
        y = 0
        window.blit(text,(x-text.get_width(),y))

    def draw_status(self,window):
        if self.snake.is_paused:
            source = "Paused. Click SPACE to continue"
        else:
            source = constants.SnakeStatus[self.status]

        text   = self.info_text_font.render(source,1,constants.TEXT_COLOR ) 
        x = constants.WIDTH_WINDOW/2
        y = 0
        window.blit(text,(x-text.get_width()/2,y))

    def draw_snake_img(self,window,y = None,x_loc = 'R'):
        if x_loc == 'C':
            x = int(constants.WIDTH_WINDOW - self.snake_image.get_width())/2
        else:
            x = constants.WIDTH_WINDOW - self.snake_image.get_width()
        if y == None:
            y = 10
        
        self.snake_image.set_xy(x,y)
        self.snake_image.draw(window)

    def draw_prompt(self,window):
        if len(self.prompt) > 0:
            text = self.info_text_font.render(self.prompt,1,constants.TEXT_COLOR ) 
            y = constants.HEIGHT_WINDOW - text.get_height()
            window.blit(text,(constants.FIELD_BORDER_LEFT,y))


    def draw_about_text(self,window):
        status_human = self.get_high_status_name(constants.HUMAN) 
        status_AI    = self.get_high_status_name(constants.AI) 

        board_size_name = constants.SIZE_NAMES[self.board_size]      
        s_max_food = "Multiple apples" if self.max_foods_on_fields == 0 else "One apple on field"
        source_about = f"""
{constants.APP_NAME}
Version {constants.VERSION}
Made by {constants.AUTHOR}

Rules:
    Grow by food only: {self.is_grow_by_food_only}
    Play with mongooses: {self.is_enemies}
    Food always avaailable {self.is_food_always or self.is_grow_by_food_only}
    {s_max_food}
"""
        source = f"""
{source_about}

User summary for 
    board {board_size_name} 
    mongooses {self.is_enemies}
    grow by fodd only {self.is_grow_by_food_only}


Total games: {self.summary.total_games[constants.HUMAN]}
High score/size/status:  {self.summary.highscore[constants.HUMAN]} / {self.summary.highsize[constants.HUMAN]} / {status_human}
Avg score:   {round(self.summary.avg_score[constants.HUMAN],2)}
        """
        source_ai = f"""
{source_about}

User summary for {board_size_name} board
------------
Total games: {self.summary.total_games[constants.HUMAN]}
High score/size/status:  {self.summary.highscore[constants.HUMAN]} / {self.summary.highsize[constants.HUMAN]} / {status_human}
Avg score:   {round(self.summary.avg_score[constants.HUMAN],2)}

AI summary for {board_size_name} board
------------
Total games: {self.summary.total_games[constants.AI]}
High score/size/status:  {self.summary.highscore[constants.AI]} / {self.summary.highsize[constants.AI]} / {status_AI}
Avg score:   {round(self.summary.avg_score[constants.AI],2)}
        """

        s =  source_ai if self.summary.total_games[constants.AI] > 0 else source

        draw_text(window,s,self.big_text_font,self.SNAKE_IMAGE.get_height())
        self.draw_snake_img(window)

    def draw_help_text(self,window):
        source = files(constants.RESOURCES).joinpath('help.txt').read_text(encoding='utf-8')
        y = draw_text(window,source,self.big_text_font)
        self.draw_snake_img(window) 

    def draw_welcome_text(self,window):
        w = WelcomeMessage(self)
        w.draw(window)

    def draw_play(self,window):
        pygame.draw.rect(self.window,constants.FIELD_COLOR,self.rect)
        self.draw_time(window)
        self.draw_status(window)
        self.draw_score(window)
        self.draw_field(window)
        if self.snake.mode >= constants.MODE_AGONY:
            self.grave.draw(window)
        self.draw_prompt(window)

    def save_statistics(self):
        config = ConfigParser()
        for s in self.summaryValues:
            s.save(config)
      
        file_path = os.path.join(constants.DATA_FOLDER,self.player_name + "_"+ self.get_variation_code() +"_"+ constants.SCORE_FILE)
        with open(file_path, "w") as file:
            config.write(file)
       
    def load_statistics(self):
        self.summaryValues = []
        for sz in constants.SIZE_NAMES:
            self.summaryValues.append(SummaryValues(sz))

        file_path = os.path.join(constants.DATA_FOLDER,self.player_name + "_"+ self.get_variation_code() + "_"+ constants.SCORE_FILE)
        if os.path.isfile(file_path):
            config =  ConfigParser()
            config.read(file_path)
            for s in self.summaryValues:
                s.read(config)
        
        self.summary  = self.summaryValues[self.board_size]        

    def get_variation_code(self):
        ret = ''
        if self.is_grow_by_food_only:
            ret += 'T'
        else:
            ret += 'F'
        
        if self.is_food_always:
            ret += 'T'
        else:
            ret += 'F'

        if self.max_foods_on_fields == 0:
            ret += '0'
        else:
            ret += '1'

        if self.is_enemies == 0:
            ret += 'T'
        else:
            ret += 'F'

        ret += str(self.board_size)     
        return ret  


    def save_config(self):
        file_path = os.path.join(constants.DATA_FOLDER,constants.SETTINGS_FILE)
        config =  ConfigParser()
        config[constants.SECTION_GENERAL] = {
            constants.KEY_SOUND : self.is_sound,
            constants.KEY_PLAYER: self.player_name,
            constants.KEY_THEME : get_theme(),
            constants.KEY_GRID  : self.is_grid,
            constants.KEY_LEVEL : self.level,
            constants.KEY_SIZE  : self.board_size,
            constants.KEY_FONT  : Control.FONT

        }
        config[constants.SECTION_RULES] = {
            constants.KEY_GROW_BY_FOOD_ONLY : self.is_grow_by_food_only,
            constants.KEY_FOOD_ALWAYS       : self.is_food_always,
            constants.KEY_ENEMY             : self.is_enemies, 
            constants.KEY_MAX_FOODS         : self.max_foods_on_fields,
            constants.KEY_PLAY_MODE         : self.play_mode
        }
   
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    def read_config(self):
        file_path = os.path.join(constants.DATA_FOLDER,constants.SETTINGS_FILE)
        if not os.path.isfile(file_path):
            self.save_config()
            return
        config = ConfigParser()
        config.read(file_path)

        section = constants.SECTION_GENERAL
        self.is_sound    = config.getboolean(section, constants.KEY_SOUND , fallback=self.is_sound )
        self.is_grid     = config.getboolean(section, constants.KEY_GRID  , fallback=self.is_grid )
        self.player_name = config.get       (section, constants.KEY_PLAYER, fallback=self.player_name)
        
        theme = config.get(section, constants.KEY_THEME , fallback=get_theme())
        if theme in Control.THEMES_BY_NAME.keys():
            set_contols_mode(Control.THEMES_BY_NAME[theme])

        self.level      = config.getint    (section, constants.KEY_LEVEL , fallback=self.level)
        self.board_size = config.getint    (section, constants.KEY_SIZE  , fallback=self.board_size)
        if config.has_option(section,constants.KEY_FONT):
            Control.FONT = config.get(section, constants.KEY_FONT, fallback=Control.FONT)

        section = constants.SECTION_RULES
        self.is_grow_by_food_only = config.getboolean(section, constants.KEY_GROW_BY_FOOD_ONLY , fallback=self.is_grow_by_food_only )
        self.is_food_always       = config.getboolean(section, constants.KEY_FOOD_ALWAYS       , fallback=self.is_food_always )
        if config.has_option(section,constants.KEY_ENEMY):
            self.is_enemies = config.getboolean(section, constants.KEY_ENEMY, fallback= self.is_enemies) 

        if config.has_option(section,constants.KEY_MAX_FOODS):
            self.max_foods_on_fields  = config.getint(section, constants.KEY_MAX_FOODS, fallback= self.max_foods_on_fields )

        if config.has_option(section,constants.KEY_PLAY_MODE):
            self.play_mode  = config.get(section, constants.KEY_PLAY_MODE, fallback= self.play_mode )

      
   
