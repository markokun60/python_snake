import pygame
import random

import constants

class SnakeCell:
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
        

    def draw(self,window):
        h  = int(constants.CELL_SIZE2) 
        h2 = int(h/2)
        xLeft = self.x
        yTop  = self.y
      
        x =  xLeft + constants.CELL_SIZE2
        y =  yTop  + constants.CELL_SIZE2
        if self.next == None:
            color = constants.SNAKE_HEAD_COLOR
          
            pygame.draw.circle(window,color,(x,y),constants.CELL_SIZE/2)
            #pygame.draw.circle(window,(255,255,255),(x,y),2)
            
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

    def set_about_mode(self):
        self.mode = constants.MODE_ABOUT
        print("About - mode")

    def start(self):
        self.body.clear()
        self.mode = constants.MODE_PLAY
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
        
    def get_status(self):
        field_size = constants.ROWS * constants.COLS
        field_size -= constants.MAX_ENEMIES
        y = field_size * 0.9
        x = len(self.body) / y
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
                print(f"Invslid data for head {r,c}")
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
