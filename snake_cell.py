import pygame
import constants

class SnakeCell:
    snake = None
    SIZE_EYE = 6
    SIZE_EYE_PUPIL = 2
    
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
 
    def copy(self,source):
        self.row        = source.row
        self.col        = source.col
        self.velocity   = source.velocity
        self.x          = source.x
        self.y          = source.y
        self.next       = source.next    

    def draw_tong(self,window): 
        h = self.snake.tong_size    
        tong_size = 2
        x =  self.x + constants.CELL_SIZE2
        y =  self.y + constants.CELL_SIZE2
        color_tong = constants.SNAKE_TONG_COLOR
        if self.velocity == 'U': 
            y = self.y
            points0 = [(x,y),(x-h,y-h)]
            points1 = [(x,y),(x+h,y-h)]
            pygame.draw.lines(window,color_tong,False,points0,tong_size)
            pygame.draw.lines(window,color_tong,False,points1,tong_size)
        elif self.velocity == 'D':
            y = self.y + constants.CELL_SIZE
            points0 = [(x,y),(x-h,y+h)]
            points1 = [(x,y),(x+h,y+h)]
            pygame.draw.lines(window,color_tong,False,points0,tong_size)
            pygame.draw.lines(window,color_tong,False,points1,tong_size)
        elif self.velocity == 'R':
            x = self.x + constants.CELL_SIZE
            points0 = [(x,y),(x+h,y+h)]
            points1 = [(x,y),(x+h,y-h)]
            pygame.draw.lines(window,color_tong,False,points0,tong_size)
            pygame.draw.lines(window,color_tong,False,points1,tong_size)
        elif self.velocity == 'L':
            x = self.x 
            points0 = [(x,y),(x-h,y-h)]
            points1 = [(x,y),(x-h,y+h)]
            pygame.draw.lines(window,color_tong,False,points0,tong_size)
            pygame.draw.lines(window,color_tong,False,points1,tong_size)

    def draw_eye(self,window:pygame.Surface,x:int,y:int):
        pygame.draw.circle(window,constants.SNAKE_EYE_COLOR,(x,y),SnakeCell.SIZE_EYE)
        if self.velocity == 'U':
            y  -= SnakeCell.SIZE_EYE
        elif self.velocity == 'D':
            y  += SnakeCell.SIZE_EYE 
        elif self.velocity == 'L':
            x  -= SnakeCell.SIZE_EYE
        elif self.velocity == 'R':
            x  += SnakeCell.SIZE_EYE    
        pygame.draw.circle(window,constants.EYE_PUPIL_COLOR,(x,y),SnakeCell.SIZE_EYE_PUPIL)

    def draw_head(self,window):
        color     = constants.SNAKE_HEAD_COLOR
        x =  self.x + constants.CELL_SIZE2
        y =  self.y + constants.CELL_SIZE2   
        d_eye =  constants.CELL_SIZE2 - SnakeCell.SIZE_EYE-1
        h  = int(constants.CELL_SIZE2) 
        h2 = int(h/2) 
        pygame.draw.circle(window,color,(x,y),constants.CELL_SIZE2)   
        if self.velocity == 'U': 
            pygame.draw.rect(window,color,(x-h2,y,h,h))
            self.draw_eye(window,x-d_eye,y)
            self.draw_eye(window,x+d_eye,y)
        elif self.velocity == 'D': 
            pygame.draw.rect(window,color,(x-h2,y-h,h,h))
            self.draw_eye(window,x-d_eye,y)
            self.draw_eye(window,x+d_eye,y)
        elif self.velocity == 'R':
            pygame.draw.rect(window,color,(x-h,y-h2,constants.CELL_SIZE2  ,h))
            self.draw_eye(window,x,y - d_eye)
            self.draw_eye(window,x,y + d_eye)

        elif self.velocity == 'L':
            pygame.draw.rect(window,color,(x,y-h2,constants.CELL_SIZE  ,h))
            self.draw_eye(window,x,y - d_eye)
            self.draw_eye(window,x,y + d_eye)
            
    def draw(self,window,tail):
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
   
        c4 = constants.CELL_SIZE2 // 2
        if self.next.velocity == self.velocity and self.velocity == 'R' and tail:
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE,h),border_radius=h2)
            pygame.draw.rect(window,color,(x+c4 ,y-h2,constants.CELL_SIZE2-c4 ,h))
      
        elif self.next.velocity == self.velocity and self.velocity == 'L' and tail:
            pygame.draw.rect(window,color,(xLeft,y-h2,constants.CELL_SIZE,h),border_radius=h2)
            pygame.draw.rect(window,color,(xLeft,y-h2,c4 ,h))
      
        elif self.next.velocity == self.velocity and self.velocity == 'U' and tail:
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE),border_radius=h2)
            pygame.draw.rect(window,color,(x-h2,yTop,h,c4))

        elif self.next.velocity == self.velocity and self.velocity == 'D' and tail:
            pygame.draw.rect(window,color,(x-h2,yTop,h,constants.CELL_SIZE),border_radius=h2)
            pygame.draw.rect(window,color,(x-h2,yTop+constants.CELL_SIZE-c4,h,c4))

        elif self.next.velocity == self.velocity and (self.velocity == 'R' or self.velocity == 'L'):
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
