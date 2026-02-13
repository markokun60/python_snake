import pygame
import os

import constants

class AnimatedSprite():
    def __init__(self):
        self.images = []
        for i in range(0,16):
            img_path = os.path.join(constants.ASSET_FOLDER,f'grave{i}.png')
            image = pygame.image.load(img_path)
            self.images.append(image)

        self.current_frame = 0
        self.image = self.images[self.current_frame]

    def set_xy(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        if self.current_frame >= len(self.images):
            self.current_frame = len(self.images)-1
            return False
        self.image = self.images[int(self.current_frame)]
        self.current_frame += 1
        return True

    def draw(self,window):
       window.blit(self.image,(self.x,self.y))
             