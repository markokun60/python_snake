from typing import Tuple,Final
import pygame

from   controls.controls import Control

class Image(Control):

    def __init__(self, name: str,position: Tuple[float, float],image,func):
        "A basic image."
        super().__init__(name,Control.IMAGE,func=func)
        self.image = image              
        self.rect = pygame.Rect(position[0], position[1], self.image.get_width(), self.image.get_height())
        self.draw_box = False 
       
    def get_width(self):
        return self.rect.width

    def draw(self, surface: pygame.Surface):
        if self.draw_box:
            pygame.draw.rect(surface,Control.CLR_BORDER,self.rect,1)
        surface.blit(self.image,(self.rect.left,self.rect.top))


    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        if self.func != None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()   
                if self.rect.collidepoint(pos):
                    self.call_back()
                    return True
        return False            
    

        


