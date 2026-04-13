from constants import *
from ai.agent  import Q_AI_PLayer
from snake     import distance

class SnakeAI:
    LEFT  = (-1,0)
    RIGHT = ( 1,0)
    UP    = ( 0,-1)
    DOWN  = ( 0, 1)
    def __init__(self,game):
        self.game  = game
        self.snake = game.snake
        self.Q_AI  = None
        self.max_count_level = 10
        self.move_mode = 0

    def train(self):
        if self.Q_AI == None:
            self.Q_AI  = Q_AI_PLayer(self.game)
        self.Q_AI.init()
        self.Q_AI.train()

    def start(self):
        self.x = 1
        self.y = 0
        self.board_size = self.snake.rows * self.snake.cols
        if self.game.ai_with_learning:
            if self.Q_AI == None:
                self.Q_AI  = Q_AI_PLayer(self.game)
            self.Q_AI.init()
        self.game.start()

    def is_good_path(self,r0,c0,vel_r,vel_c):
        r = r0 + vel_r
        c = c0 + vel_c
        r1 = r - 1
        r = False
        while self.snake.is_has(r,c):
            if is_open(self.snake.fields[r][c]):
                if self.count_closed(r,c) > 2:
                    r = True
                    break       
                r += vel_r
                c += vel_c
            else:
                return False
        return r         

    def change_to(self):
        if self.game.is_grow_by_food_only:
            HR = 1
            HC = 1
        else:
            enemies = self.snake.get_items(EMPTY_VAL)
            if len(enemies) == 0:
                HR = 1
                HC = 1
            else:
                HC = 3 if self.game.is_enemies else 1
                HR = 3 if self.game.is_enemies else 2

        (r,c) = self.snake.get_head()
        c += self.snake.x_velocity 
        r += self.snake.y_velocity 
        if self.move_mode == 0:
            if self.y != 0:
                self.y = 0
                if c <= HC:
                    dx = 1
                else:
                    dx = -1 

                c1 = c + dx
                if c1 < 0 or c1 >= self.snake.cols:
                    dx = -dx
                else:     
                    v = self.snake.fields[r][c1]
                    if is_closed(v):
                        dx = -dx
                print(f"Hor: {r},{c} --> {r},{c1} {v} {dx} ")  
                self.x = dx
                                 
            elif c <= HC  and self.x < 0: 
                self.x = 0
                if r < HR:
                    self.y = 1
                    self.move_mode = 1
                else:    
                    self.y = -1
                print(f"vert: {r},{c} --> {self.x},{self.y}  mode: {self.move_mode} ")  
            elif c >= self.snake.cols-2 and self.x > 0:   
                self.x = 0
                if r < HR:
                    self.y = 1
                    self.move_mode = 1
                    print(f"vert down: {r},{c} --> {self.x},{self.y} new mode: {self.move_mode} ")  
                else:    
                    self.y = -1 
                    print(f"vert  up: {r},{c} --> {self.x},{self.y} mode {self.move_mode} ")  

            else:
                r1 = r + 1
                down = False
                if r1 < self.snake.rows - 2:
                    v1 = self.snake.fields[r1][c]
                    if is_open(v1):
                        r2 = r1 + 1
                        v2 = self.snake.fields[r2][c]
                        if is_closed(v2):
                            if self.is_good_path(r2,c,0,self.x):
                                down = True
                if down:                  
                    self.y = 1
                    self.x = 0   
                    print(f"vert: {r},{c} --> {self.x},{self.y} move down ") 
                else:
                    print(f"hor: {r},{c} --> {self.x},{self.y} ") 

        elif r > self.snake.rows - 1 - HR:
            self.move_mode = 0  
            print(f"new mode 0, was 1: {r},{c} --> {self.x},{self.y} ") 
        else:
            print(f"vert mode 1: {r},{c} --> {self.x},{self.y} ")  
       
    def move(self):
        if self.game.ai_with_learning:
            self.Q_AI.move()  
        else:
            self.s_move()

    def s_move(self):
        F_MOVES     = 0
        F_FOOD      = 400 if self.game.is_grow_by_food_only else 1
        F_CRITICAL  = 0 
        F_DIRECTION = 300

        #print(sys.getrecursionlimit())
        (rm,cm) = self.snake.get_head()
        r_best = 0
        c_best = 0
        f_best = 0
        foods  = None

        #print(f" ------- ai move {rm} {cm} ---------")
        velocities = self.get_directions(self.snake.x_velocity,self.snake.y_velocity)
        for (c_vel,r_vel) in velocities:
            r = rm + r_vel
            c = cm + c_vel
            if self.snake.is_has(r,c):
                v = self.snake.fields[r][c]
                is_food = False
                if v == FOOD_VAL:
                    is_food = True
                elif v != EMPTY_VAL:
                    #print(f"Not empty cell {r},{c}: value: {v} velocity: {r_vel} {c_vel}")
                    continue

                if F_MOVES == 0 and F_CRITICAL == 0:
                    moves = 0
                    critical = 0
                else:                          
                    moves = self.count_moves(r,c)
                    critical = 11 -  moves if  moves <= 10  else 0                    
 
                f_moves = moves * F_MOVES
                if is_food:
                    df = 1
                    f_food = F_FOOD
                elif self.game.is_grow_by_food_only:
                    if foods == None:
                        foods = self.snake.get_items(FOOD_VAL)
                    df = 1 + distance(r,c,foods) 
                    f_food = F_FOOD * 1 / df
                else:
                    f_food = 0
                    df = 99999
       
                f_direction = F_DIRECTION if c_vel == self.x and r_vel == self.y else 0
                f_critical =  critical * F_CRITICAL    
                f = f_food + f_moves + f_direction +  f_critical 

                if r_best == 0 and c_best == 0:
                    r_best = r_vel
                    c_best = c_vel
                    f_best = f
                elif f_best < f:
                    r_best = r_vel
                    c_best = c_vel
                    f_best = f    
                
                print(f"{self.game.step_no}  food = {f_food} {df},moves={f_moves},direction={f_direction},critical={f_critical},f={f}, best={f_best}")         
                     
            #else:
            #     print(f"Out of field: {r},{c} velocity: {r_vel} {c_vel}")
        
        if c_best != 0 or r_best != 0:
            self.snake.x_velocity = c_best
            self.snake.y_velocity = r_best
            #print(f"{self.snake.x_velocity} {self.snake.y_velocity} best={f_best}")     
            self.change_to()    
 
        else:
            print('No moves')  

    def get_directions(self,x,y):       
        if x > 0:
            return [SnakeAI.RIGHT,SnakeAI.UP,SnakeAI.DOWN]      
        if x < 0:
            return [SnakeAI.LEFT,SnakeAI.UP,SnakeAI.DOWN]
        if y > 0:
            return [SnakeAI.DOWN,SnakeAI.RIGHT,SnakeAI.LEFT] 
        if y < 0:
            return [SnakeAI.UP,SnakeAI.LEFT,SnakeAI.RIGHT]  
    
    def _count_moves(self,r0,c0,cells,x,y,level = 0):
        n = 1
        old_value = cells[r0][c0]
        cells[r0][c0] = ENEMY_VAL
        l = 13
        if self.board_size > 600:
            l = 10

        directions = self.get_directions(x,y)
        for (dc,dr) in directions:
            c = c0 + dc
            r = r0 + dr
            if r >= 0 and r < self.snake.rows  and c >= 0 and c < self.snake.cols: 
                if cells[r][c] ==  EMPTY_VAL or cells[r][c] == FOOD_VAL:
                    if level == self.max_count_level:
                        n += 1
                    else:
                        n += self._count_moves(r,c,cells,dc,dr,level+1)  
        if level < l:
            cells[r0][c0] = old_value
        return n

    def copy_field(self):
        cells =[[0 for x in range(self.snake.cols )] for y in range(self.snake.rows)]
        for r in range(self.snake.rows ):
            for c in range(self.snake.cols):
                cells[r][c] = self.snake.fields[r][c]
        return cells

    def count_moves(self,r0,c0):
        cells = self.copy_field()
        n = self._count_moves(r0,c0,cells,self.snake.x_velocity,self.snake.y_velocity)
        return n;

    def count_closed(self,r0,c0):
        n = 0
        for (vc,vr) in VELOCITIES:
            r = r0 + vr
            c = c0 + vc
            if r >= 0 and r < self.snake.rows and c >= 0 and c < self.snake.cols:
                if is_open(self.snake.fields[r][c]):
                    n += 1
        return n;

    def get_path_size(self,r0,c0,vel_r,vel_c):
        n = 0
        r = r0 + vel_r
        c = c0 + vel_c
        while r >= 0 and r < self.snake.rows and c >= 0 and c < self.snake.cols:
            if is_open(self.snake.fields[r][c]):
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