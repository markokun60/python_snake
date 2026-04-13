import pygame
import os
from   time import time

import constants

class AnimatedSprite():
    def __init__(self):
        self.images = []       
        self.current_frame = 0 
        self.image = None
        self.is_one_run_only = True
        self.x = None
        self.y = None

    def set_xy(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        if self.current_frame >= len(self.images):
            if self.is_one_run_only:
                self.current_frame = len(self.images)-1
                return False 
            else:
                self.current_frame = 0
                return True
        self.image = self.images[int(self.current_frame)]
        self.current_frame += 1
        return True

    def draw(self,window):
       if self.x != None and self.y != None:
            if self.image == None:
                self.image = self.images[self.current_frame]
            window.blit(self.image,(self.x,self.y))

    def get_width(self):
        return self.images[0].get_width()
                
    def get_height(self):
        return self.images[0].get_height()
    
                         
class Grave(AnimatedSprite):
    def __init__(self,resource_folder):
        super().__init__()
        for i in range(0,16):
            img_path = os.path.join(resource_folder,constants.GRAVE_FOLDER,f'grave{i}.png')
            image = pygame.image.load(img_path).convert_alpha()
            self.images.append(image)

class Enemy(AnimatedSprite):
    def __init__(self,images,row,col):
        super().__init__() 
        self.is_one_run_only = False
        self.images = images
        y = constants.row_to_y(row)
        x = constants.col_to_x(col)
        self.set_xy(x,y)

    def draw(self,window):
        self.update()
        super().draw(window)


class SnakeImage(AnimatedSprite):
    def __init__(self,resource_folder):
        super().__init__()
        self.is_one_run_only = False
        for z in constants.SnakeStatusGroup.keys():
            im = constants.SnakeStatusGroup[z]
            img = pygame.image.load(os.path.join(resource_folder,"snakes",im)).convert_alpha()
            img = pygame.transform.smoothscale(img,(256,256))
            self.images.append(img)
        self.update_time = None         

    def draw(self,window):
        if self.update_time == None:
            self.update_time = time()
        else:
            dt = time() - self.update_time
            if dt > 1.0:
                self.update_time = time() 
                self.update()
        super().draw(window)
