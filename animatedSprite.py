import pygame
import os

import constants

class AnimatedSprite():
    def __init__(self):
        self.images = []       
        self.current_frame = 0 
        self.image = None
        self.is_one_run_only = True

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
       if self.image == None:
            self.image = self.images[self.current_frame]
       window.blit(self.image,(self.x,self.y))
             

class Grave(AnimatedSprite):
    def __init__(self):
        super().__init__()
        for i in range(0,16):
            img_path = os.path.join(constants.ASSET_FOLDER,'grave',f'grave{i}.png')
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
