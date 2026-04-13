import pygame
import random
import os

import constants
from   snake_cell import SnakeCell

class Snake:
    body = []

    x_velocity = 0
    y_velocity = 0
    message    = ""
    is_paused  = False
    is_report  = True
    is_draw    = True

    mode = constants.MODE_WELCOME

    def __init__(self,f):
        self.fields = f
        #self.images = self.import_images()
        SnakeCell.snake = self
        self.tong_size = constants.CELL_SIZE2 ;
        self.tong_velociity = 1
        self.rows = constants.ROWS
        self.cols = constants.COLS 

    def import_images_not_use(self):
        surf_dict = {}
        for folder_path, _, image_names in os.walk(os.path.join(constants.ASSET_FOLDER,  'snake')):
            for image_name in image_names:
                full_path = os.path.join(folder_path, image_name)
                surface = pygame.image.load(full_path).convert_alpha()

                surf_dict[image_name.split('.')[0]] = surface
        return surf_dict 

    def _update_tong_size(self):
        self.tong_size += self.tong_velociity
        if  self.tong_size >= constants.CELL_SIZE2 :
            self.tong_velociity = -1
        elif  self.tong_size < 2:
            self.tong_velociity = 1

    def set_about_mode(self):
        self.mode = constants.MODE_ABOUT
        if self.is_report:
            print("About - mode")

    def start(self,is_AI):
        self.rows = constants.ROWS
        self.cols = constants.COLS

        self.body.clear()
        if is_AI:
            self.mode = constants.MODE_CMP_PLAY
            self.is_draw = False
        else:
            self.mode    = constants.MODE_PLAY
            self.is_draw = True

        self.grow_by_food_size = round(self.rows * self.cols * 0.03)    
        if self.is_report:
            print(f'food give you grow by {self.grow_by_food_size} cells')
 
        for r in range(0,self.rows):
            for c in range(0,self.cols):
                self.fields[r][c] = constants.EMPTY_VAL

        d = 6
        c = random.randint(d,self.cols - d)
        r = random.randint(d,self.rows - d)
        

        #c = self.cols // 2
        #r = self.rows // 2
       
        self.fields[r][c] = constants.SNAKE_VAL

        (self.x_velocity,self.y_velocity) = random.choice(constants.VELOCITIES)
        self.x_velocity = 1
        self.y_velocity = 0
        cell = SnakeCell(r,c,self.x_velocity,self.y_velocity)
        self.body.append(cell)
        if self.is_report:
            print(f"Started: {r,c} {self.x_velocity,self.y_velocity}")

        self.x_velocity = 0
        self.y_velocity = -1
        self.grow()
     
    def get_progress(self):
        field_size = self.rows  * self.cols
        field_size -= constants.MAX_ENEMIES
        x = len(self.body) / field_size
        return x
        
    def get_status(self,body_size = 0):
        field_size = self.rows * self.cols
        field_size -= constants.MAX_ENEMIES
        y = field_size * 0.9
        size = len(self.body) if body_size == 0 else body_size
        x = size  / y
        if x > 1:
            x = 1
        x *= len(constants.SnakeStatus)
        n = int(x)
        return n

    def get_head(self):
        if len(self.body) == 0:
            return (-1,-1)

        head = self.body[-1]
        return (head.row,head.col)

    def is_moving(self):
        if not self.mode in (constants.MODE_PLAY,constants.MODE_CMP_PLAY) :
            return False
        elif self.is_paused:
            return False
        elif len(self.body) == 0:
            return False
        elif self.x_velocity == 0 and self.y_velocity == 0:
            return False
        return True
    
    def get_size(self):
        return len(self.body)

    def get_items(self,value:int):
        items = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.fields[r][c] == value:
                    items.append((r,c))
        return items

        
    def grow(self):
        if self.x_velocity == 0 and self.y_velocity == 0:
            print('No velocity')
            ret =  constants.ERROR_RET_VAL

        elif not (self.x_velocity == 0 or self.y_velocity == 0):
            print(f'Invalid vlocity  {self.x_velocity,self.y_velocity}')
            mode = constants.MODE_GAME_OVER
            ret = constants.ERROR_RET_VAL
    
        else:
            (r,c) = self.get_head()
            if self.fields[r][c] != constants.SNAKE_VAL:
                print(f"Invalid data for head {r,c}")
                ret =  constants.ERROR_RET_VAL
            else: 

                c += self.x_velocity
                r += self.y_velocity

                if r < 0 or r >= constants.ROWS or c < 0 or c >= constants.COLS:
                    if self.is_report:
                        print(f"Border: {r,c}: direction {self.x_velocity,self.y_velocity}")
                        self.message = "Meet border"
                    ret =  constants.BORDER_RET_VAL

                elif self.fields[r][c] == constants.SNAKE_VAL:
                    if self.is_report:
                        print(f"Meet body: {r,c}")
                        self.message = "Meet body"
                    ret = constants.BODY_RET_VAL

                elif self.fields[r][c] == constants.ENEMY_VAL:
                    if self.is_report:
                        print(f"Meet enemy: {r,c}")
                        self.message = "Meet mongoose"
                    ret =  constants.EMENY_RET_VAL
        
                else:
                    ret = constants.OK_RET_VAL
                    if self.fields[r][c] == constants.FOOD_VAL:
                        ret = constants.FOOD_RET_VAL

                    cell = SnakeCell(r,c,self.x_velocity,self.y_velocity,self.body[-1])
                    self.body.append(cell)
                    self.fields[r][c] = constants.SNAKE_VAL
                    self.sub_step = 0
       
        if not constants.is_ok(ret):
            self.mode = constants.MODE_AGONY
            if ret ==  constants.ERROR_RET_VAL:
                self.message = "Fatal application error"
        elif self.is_draw:
            self._update_tong_size()
        return ret

    def move(self):
        #n = len(self.body)
        #for i in range(n-1):
        #    self.body[i+1].copy(self.body[i])

        ret = self.grow()
        if ret < constants.ERROR_RET_VAL:
           
            tail = self.body[0]
            self.body.pop(0)
            self.fields[tail.row][tail.col] = constants.EMPTY_VAL 
        return ret
    
    def turn_left(self):
        x = self.x_velocity
        y = self.y_velocity

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
        x = self.x_velocity
        y = self.y_velocity

        if x < 0 and y == 0: #left
            return (0,-1) #up

        if x == 0 and y < 0: #up
            return (1,0) #right

        if x > 0 and y == 0: #right
            return (0,1) #down

        if x == 0 and y > 0: #down
            return (-1,0) #left

        return (0,0)

    def draw(self,window:pygame.Surface):
        tail = True
        for cell in self.body:
            cell.draw(window,tail)
            tail = False

    def is_has(self,r:int,c:int):
         return r >= 0 and r < self.rows and c >= 0 and c < self.cols

    def get_state(self):
        (rh,ch) = self.get_head()    
        foods = self.get_items(constants.FOOD_VAL)
        dir_l = self.x_velocity < 0
        dir_r = self.x_velocity > 0
        dir_u = self.y_velocity < 0
        dir_d = self.y_velocity > 0
        
        #meet_border = []
        #meet_body   = []
        #meet_enemy  = []
        dangers      = []
        meet_food    = []

        LEFT  = (-1 ,0)
        RIGHT = (1  ,0)
        UP    = (0 ,-1)
        DOWN  = (0 , 1)

        directions = [] # straight, right, left
        if self.x_velocity > 0: # right
            directions = [RIGHT,DOWN,UP]
        elif self.x_velocity < 0: # left
            directions = [LEFT,UP,DOWN]
        elif self.y_velocity < 0: # up
            directions = [UP,RIGHT,LEFT]
        elif self.y_velocity > 0: # down
            directions = [DOWN,LEFT,RIGHT]
        else:
            print("No directions")    

        for (cm,rm) in  directions:    
            r = rm + rh
            c = cm + ch
            is_border = False
            is_body   = False
            is_food   = False
            is_enemy  = False
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                is_border = True
            elif self.fields[r][c] == constants.SNAKE_VAL:
                is_body = True  
            elif self.fields[r][c] == constants.ENEMY_VAL:
                is_enemy = True          
            #elif self.fields[r][c] == constants.FOOD_VAL:
            #    is_food= True

            is_danger = is_border or is_enemy or is_body
            dangers.append(is_danger)
            #meet_border.append(is_border)
            #meet_body.append(is_body)
            #meet_enemy.append(is_enemy)
            #meet_food.append(is_food)

        food_l  = False
        food_r  = False
        food_d  = False
        food_u  = False

        for (rf,cf) in foods:
            if cf < ch:  
                food_l = True
            if cf > ch: 
                food_r = True

            if rf < rh: 
                food_u = True

            if rf > rh: 
                food_d = True

        
        state = [
            dangers[0],dangers[1],dangers[2],
            dir_l,dir_r,dir_u,dir_d,
            food_l,food_r,food_u,food_d
        ]
    
        return state


 
def distance(r,c,cells):
    x = 1000000
    for cell in cells:
        cell_r = cell[0]
        cell_c = cell[1]
        dr = abs(r - cell_r)
        dc = abs(c - cell_c)
        d = dr + dc
        if x > d:
            x = d
    return x