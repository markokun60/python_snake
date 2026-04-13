#import pygame
from typing import Final
from importlib.resources import files
from draw_html import DrawHTML
import constants

class WelcomeMessage:
    AI_WITH_LEARRNING :Final[str]= "AI_Y"
    AI_NO_LEARRNING   :Final[str]= "AI_N"
    TEXT_SOURCES : Final = {
            constants.HUMAN     : 'welcome',
            constants.TRAINING  : 'training',
            AI_WITH_LEARRNING   :'ai_learning',
            AI_NO_LEARRNING     :'ai'
        }   
     
    def __init__(self,game):
        self.game = game
        self.images = {
            constants.HUMAN   : game.snake_image,
            constants.AI      : game.AI_IMAGE,
            constants.TRAINING: game.AI_TRAINING_IMAGE
        }  
        self.sources = {}
        for key in WelcomeMessage.TEXT_SOURCES.keys():
            source = f"{WelcomeMessage.TEXT_SOURCES[key]}.txt"
            self.sources[key]  = files(constants.RESOURCES).joinpath(source).read_text(encoding='utf-8') 

        self.draw_sources = {}
        self.reset()

    def reset(self):  
        self.draw_sources.clear()
        for key in self.sources.keys():
            source = self.sources[key]
            #self.draw_sources[key] = self.game.big_text_font.render(source,1,constants.TEXT_COLOR)
            self.draw_sources[key] = DrawHTML(source,self.game.big_text_font,constants.TEXT_COLOR)

    def draw(self,window):
        mode = self.game.play_mode
        img = self.images[mode] 
        if mode == constants.AI:
            mode = WelcomeMessage.AI_WITH_LEARRNING if self.game.ai_with_learning else WelcomeMessage.AI_NO_LEARRNING           
        
        dh = self.draw_sources[mode]   

        x = (constants.WIDTH_WINDOW  - dh.get_width()) //2
        y = (constants.HEIGHT_WINDOW - dh.get_height())//2
        #window.blit(dh,(x,y))
        dh.draw(window,(x,y))

        x = (constants.WIDTH_WINDOW  - img.get_width()) - 24
        y = (constants.HEIGHT_WINDOW - img.get_height()) - 24
        if mode == constants.HUMAN:
            img.set_xy(x,y)
            img.draw(window)
        else:
            window.blit(img,(x,y))
        