
from tkinter import W
import pygame
import random
import os

 
import constants

class SnakeCell:
    snake = None
    def __init__(self,row,col,x_velocity,y_velocity,prev = None):
        self.row = row
        self.col = col
        if x_velocity < 0:
            self.velocity = 'L'
        elif x_velocity > 0:
            self.velocity = 'R'
        elif y_velocity < 0:
            self.velocity = 'U'
        elif y_velocity > 0:
            self.velocity = 'D'
    
        self.next = None
        if prev != None:
            prev.next = self
    
        self.x = constants.col_to_x(self.col )
        self.y = constants.row_to_y(self.row )

     
    def draw_tong(self,window):
     
        h = self.snake.tong_size    

        x =  self.x + constants.CELL_SIZE2
        y =  self.y + constants.CELL_SIZE2
        color_tong = constants.SNAKE_TONG_COLOR
        if self.velocity == 'U': 
            y = self.y
            points0 = [(x,y),(x-h,y-h)]
            points1 = [(x,y),(x+h,y-h)]
            pygame.draw.lines(window,color_tong,False,points0,1)
            pygame.draw.lines(window,color_tong,False,points1,1)
        elif self.velocity == 'D':
            y = self.y + constants.CELL_SIZE
            points0 = [(x,y),(x-h,y+h)]
            points1 = [(x,y),(x+h,y+h)]
            pygame.draw.lines(window,color_tong,False,points0,1)
            pygame.draw.lines(window,color_tong,False,points1,1)
        elif self.velocity == 'R':
            x = self.x + constants.CELL_SIZE
            points0 = [(x,y),(x+h,y+h)]
            points1 = [(x,y),(x+h,y-h)]
            pygame.draw.lines(window,color_tong,False,points0,1)
            pygame.draw.lines(window,color_tong,False,points1,1)
        elif self.velocity == 'L':
            x = self.x 
            points0 = [(x,y),(x-h,y-h)]
            points1 = [(x,y),(x-h,y+h)]
            pygame.draw.lines(window,color_tong,False,points0,1)
            pygame.draw.lines(window,color_tong,False,points1,1)

    def draw_head(self,window):
        color = constants.SNAKE_HEAD_COLOR
        x =  self.x + constants.CELL_SIZE2
        y =  self.y + constants.CELL_SIZE2     
        h  = int(constants.CELL_SIZE2) 
        h2 = int(h/2) 
        pygame.draw.circle(window,color,(x,y),constants.CELL_SIZE/2)
        if self.velocity == 'U': 
           pygame.draw.rect(window,color,(x-h2,y,h,h))
        elif self.velocity == 'D': 
           pygame.draw.rect(window,color,(x-h2,y-h,h,h))
        elif self.velocity == 'R':
            pygame.draw.rect(window,color,(x-h,y-h2,constants.CELL_SIZE2  ,h))
        elif self.velocity == 'L':
            pygame.draw.rect(window,color,(x,y-h2,constants.CELL_SIZE  ,h))

    def draw(self,window):
        h  = int(constants.CELL_SIZE2) 
        h2 = int(h/2) 
        xLeft = self.x
        yTop  = self.y
      
        x =  xLeft + constants.CELL_SIZE2
        y =  yTop  + constants.CELL_SIZE2
        if self.next == None: 
            self.draw_head(window) 
            self.draw_tong(window)
            return
        color = constants.SNAKE_BODY_COLOR
   
        if self.next.velocity == self.velocity and (self.velocity == 'R' or self.velocity == 'L'):
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE,h))

        elif self.next.velocity == self.velocity and (self.velocity == 'U' or self.velocity == 'D'): 
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE))

        elif self.velocity == 'R' and self.next.velocity == 'U':
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE2+h2))

        elif self.velocity == 'R' and self.next.velocity == 'D':
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))
            pygame.draw.rect(window,color,(x-h2,y,h,constants.CELL_SIZE2))

        elif self.velocity == 'L' and self.next.velocity == 'U':
            pygame.draw.rect(window,color,(x,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE2+h2))

        elif self.velocity == 'L' and self.next.velocity == 'D':
            pygame.draw.rect(window,color,(x-h2,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))
            pygame.draw.rect(window,color,(x-h2,y,h,constants.CELL_SIZE2))

        elif self.velocity == 'D' and self.next.velocity == 'L':
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE2))
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))

        elif self.velocity == 'D' and self.next.velocity == 'R':
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE2))
            pygame.draw.rect(window,color,(x-h2,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))

        elif self.velocity == 'U' and self.next.velocity == 'L':
            pygame.draw.rect(window,color,(x-h2,y-h2,constants.CELL_SIZE2,constants.CELL_SIZE2 + h2))
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE2,constants.CELL_SIZE2))

        elif self.velocity == 'U' and self.next.velocity == 'R':
            pygame.draw.rect(window,color,(x-h2,y-h2,constants.CELL_SIZE2,constants.CELL_SIZE2+h2))
            pygame.draw.rect(window,color,(x-h2,y-h2,constants.CELL_SIZE2+h2,constants.CELL_SIZE2))

        #else:
        #    pygame.draw.rect(window,color,(self.x,self.y,constants.CELL_SIZE,constants.CELL_SIZE))

class Snake:
    body = []

    x_velocity = 0
    y_velocity = 0
    message    = ""
    is_paused  = False


    mode = constants.MODE_WELCOME

     
    def __init__(self,f):
        self.fields = f
        #self.images = self.import_images()
        SnakeCell.snake = self
        self.tong_size = constants.CELL_SIZE2 ;
        self.tong_velociity = 1

    def import_images_not_use(self):
        surf_dict = {}
        for folder_path, _, image_names in os.walk(os.path.join(constants.ASSET_FOLDER,  'snake')):
            for image_name in image_names:
                full_path = os.path.join(folder_path, image_name)
                surface = pygame.image.load(full_path).convert_alpha()

                surf_dict[image_name.split('.')[0]] = surface
        return surf_dict 

    def update_tong_size(self):
        self.tong_size += self.tong_velociity
        if  self.tong_size >= constants.CELL_SIZE2 :
            self.tong_velociity = -1
        elif  self.tong_size < 2:
            self.tong_velociity = 1

    def set_about_mode(self):
        self.mode = constants.MODE_ABOUT
        print("About - mode")

    def start(self,is_AI = False):
        self.body.clear()
        if is_AI:
            self.mode = constants.MODE_CMP_PLAY
        else:
            self.mode    = constants.MODE_PLAY
        d = 6
        for r in range(0,constants.ROWS):
            for c in range(0,constants.COLS):
                self.fields[r][c] = constants.EMPTY_VAL

        c = random.randint(d,constants.COLS-d)
        r = random.randint(d,constants.ROWS-d)
       
        self.fields[r][c] = constants.SNAKE_VAL

        (self.x_velocity,self.y_velocity) = random.choice(constants.VELOCITIES)
        self.x_velocity = 1
        self.y_velocity = 0
        cell = SnakeCell(r,c,self.x_velocity,self.y_velocity)
        self.body.append(cell)
        print(f"Started: {r,c} {self.x_velocity,self.y_velocity}")

        self.x_velocity = 0
        self.y_velocity = -1
        self.grow()
     
    def get_progress(self):
        field_size = constants.ROWS * constants.COLS
        field_size -= constants.MAX_ENEMIES
        x = len(self.body) / field_size
        return x
        
    def get_status(self,body_size = 0):
        field_size = constants.ROWS * constants.COLS
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
        if self.mode != constants.MODE_PLAY:
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
 
    def distance(self,r,c,cells):
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


    def _count_moves(self,r0,c0,cells,level = 0):
        n = 1
        old_value = cells[r0][c0]
        cells[r0][c0] = constants.ENEMY_VAL
        board_size = constants.ROWS * constants.COLS   
        l = 12
        if board_size > 600:
            l = 10

        for (dr,dc) in constants.VELOCITIES:
            c = c0 + dc
            r = r0 + dr
            if r >= 0 and r < constants.ROWS and c >= 0 and c < constants.COLS:
                if cells[r][c] == constants.EMPTY_VAL or cells[r][c] == constants.FOOD_VAL:
                    if level == 700:
                        n += 1
                    else:
                        n += self._count_moves(r,c,cells,level+1)  
        if level < l:
            cells[r0][c0] = old_value
        return n

    def copy_field(self):
        cells =[[0 for x in range(constants.COLS)] for y in range(constants.ROWS)]
        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                cells[r][c] = self.fields[r][c]
        return cells

    def count_moves(self,r0,c0):
        cells = self.copy_field()
        n = self._count_moves(r0,c0,cells)
        return n;

    def count_closed(self,r0,c0):
        n = 0
        for (vr,vc) in constants.VELOCITIES:
            r = r0 + vr
            c = c0 + vc
            if r >= 0 and r < constants.ROWS and c >= 0 and c < constants.COLS:
                if self.fields[r][c] == constants.EMPTY_VAL or self.fields[r][c] == constants.FOOD_VAL:
                    n += 1
        return n;

    def get_path_size(self,r0,c0,vel_r,vel_c):
        n = 0
        r = r0 + vel_r
        c = c0 + vel_c
        while r >= 0 and r < constants.ROWS and c >= 0 and c < constants.COLS:
            if self.fields[r][c] == constants.EMPTY_VAL or self.fields[r][c] == constants.FOOD_VAL:
                if self.count_closed(r,c) <= 2:
                    break
                n += 1
                #f n == max_path: 
                #    break
                r += vel_r
                c += vel_c
            else:
                break
        return n

    def get_items(self,value):
        items = []
        for r in range(constants.ROWS):
            for c in range(constants.COLS):
                if self.fields[r][c] == value:
                    items.append((r,c))
        return items

    def ai_move(self):
        #print(sys.getrecursionlimit())
        (rm,cm) = self.get_head()
        r_best = 0
        c_best = 0
        f_best = 0
        foods  = self.get_items(constants.FOOD_VAL)

        n_to_folow_food = 2

        for (r_vel,c_vel) in constants.VELOCITIES:
            r = rm + r_vel
            c = cm + c_vel
            if r >= 0 and r < constants.ROWS and c >= 0 and c < constants.COLS:
                is_food = False
                if self.fields[r][c] == constants.FOOD_VAL:
                    is_food = True
                elif self.fields[r][c] != constants.EMPTY_VAL:
                    continue
                
                if is_food:
                    f_food = 0
                else:
                    f_food  = 0 #self.distance(r,c,foods)
                           
                f_bad_cells = 0
                if r == 0 or r == constants.ROWS-1 or c == 0 or c == constants.COLS-1:
                    f_bad_cells = 3500
                elif r == 1 or r == constants.ROWS-2 or c == 1 or c == constants.COLS-2:
                    f_bad_cells = 2000
                elif r == 2 or r == constants.ROWS-3 or c == 2 or c == constants.COLS-3:
                    f_bad_cells = 500

                p_size = self.get_size()
                if p_size > n_to_folow_food:
                    f_moves = 0#self.count_moves(r,c)
                    f_path  = self.get_path_size(r,c,r_vel,c_vel)
                    p_size /= 50
                else:
                    f_moves = 0
                    f_path  = 0
                    p_size  = 0
                    
                #f = -60 * f_food + (4 + p_size) * f_path + f_moves * 16 - 3 * f_bad_cells
                f  = -f_food + (1 + p_size) * f_path + f_moves  -  f_bad_cells
                
                print(f"food = {f_food},p_size={p_size}, f_path={f_path}, moves={f_moves},f_bad_cells={f_bad_cells}, best={f_best}")
                if r_best == 0 and c_best == 0:
                    r_best = r_vel
                    c_best = c_vel
                    f_best = f
                elif f_best < f:
                    r_best = r_vel
                    c_best = c_vel
                    f_best = f
        
        if c_best != 0 or r_best != 0:
            self.x_velocity = c_best
            self.y_velocity = r_best
        

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
                    print(f"Border: {r,c}: direction {self.x_velocity,self.y_velocity}")
                    self.message = "Meet border"
                    ret =  constants.BORDER_RET_VAL

                elif self.fields[r][c] == constants.SNAKE_VAL:
                    print(f"Neet body: {r,c}")
                    self.message = "Meet body"
                    ret = constants.BODY_RET_VAL

                elif self.fields[r][c] == constants.ENEMY_VAL:
                    print(f"Neet enemy: {r,c}")
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
        else:
            self.update_tong_size()
        return ret

    def move(self):
        ret = self.grow()
        if ret < constants.ERROR_RET_VAL:
            tail = self.body[0]
            self.body.pop(0)
            self.fields[tail.row][tail.col] = constants.EMPTY_VAL 
        return ret

    def draw(self,window):
        for cell in self.body:
            cell.draw(window)
