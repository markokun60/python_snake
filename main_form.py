import pygame
from  os.path import join
from   typing import Final

from controls.form       import Form
from controls.button     import Button
from controls.controls   import Control,init_controls
from constants import *
from form_options        import Form_Options

class MainForm(Form):
    DX:Final[int] = 10
    
    def __init__(self,game,snake_ai):
        super().__init__()
        init_controls()
        self.game = game
        self.snake_ai = snake_ai
        Control.form = self
        self.mode = MODE_WELCOME
        self.yButton  = H_BUTTON 
        self.xButtton = (WIDTH_WINDOW - 5 * W_BUTTON - 4 * MainForm.DX)//2+ W_BUTTON/ 2
        
        self._create_images()
        self._create_buttons()
        self.form_options = Form_Options(self,self.game, self.images)

    def _create_images(self):
        root = self.game.resource_folder
        self.imgSnake   = pygame.image.load(join(root,'snake_small.png')).convert_alpha()
        self.imgStart   = pygame.image.load(join(root,'start.png')).convert_alpha()
        self.imgHelp    = pygame.image.load(join(root,'help.png')).convert_alpha()
        self.imgOptions = pygame.image.load(join(root,'options.png')).convert_alpha()
        self.imgBack    = pygame.image.load(join(root,'cancel.png')).convert_alpha()
        self.imgExit    = pygame.image.load(join(root,'exit.png')).convert_alpha()
        self.images = {
            'back': self.imgBack
        }

    def set_start_hint(self):
        if self.game.play_mode == HUMAN: 
            self.btnStart.set_hint("Start play the game")
        elif self.game.play_mode == AI: 
            self.btnStart.set_hint("Start AI play") 
        else:
            self.btnStart.set_hint( "Start AI Training")

    def _create_buttons(self):
        x = self.xButtton
        y = self.yButton 
     
        btnBack = Button('btnBack',position=(W_BUTTON // 2+12, y),  size=(W_BUTTON, H_BUTTON),  func=self.back, text='Back',image=self.imgBack)
        btnBack.hide  = True
        btnBack.hint  = "Back to main menu" 
        btnBack.key   = pygame.K_ESCAPE

        self.btnStart = Button('btnStart',position=(x, y), size=(W_BUTTON, H_BUTTON), func= self.start, text='Start',image = self.imgStart)
        self.set_start_hint()
        self.btnStart.key = pygame.K_SPACE

        x += W_BUTTON
        x += MainForm.DX
        btnAbout = Button('btnAbout',position=(x, y), size=(W_BUTTON, H_BUTTON),  func=self.about, text='About',image=self.imgSnake)
        btnAbout.hint  = "Show about information"

        x += W_BUTTON
        x += MainForm.DX
        btnHelp = Button('btnHelp',position=(x, y), size=(W_BUTTON, H_BUTTON),  func=self.help, text='Help',image=self.imgHelp)
        btnHelp.hint  = "Show how to play"

        x += W_BUTTON
        x += MainForm.DX
        btnOptions = Button('btnOptions',position=(x, y), size=(W_BUTTON, H_BUTTON),  func=self.menu_settings, text='Options',image=self.imgOptions)
        btnOptions.hint  = "Change settings"

        x += W_BUTTON
        x += MainForm.DX
        btnExit = Button('btnExit',position=(x, y), size=(W_BUTTON, H_BUTTON), func=self.exit_game, text='Exit',image=self.imgExit)
        btnExit.hint  = "Exit the game"      

    def back(self):
        self.hide_show()
        self.game.snake.mode = MODE_WELCOME

    def start(self):    
        if self.game.play_mode == TRAINING:
            self.snake_ai.train()
        elif self.game.play_mode == AI:
            self.snake_ai.start() 
        else:
            self.game.start()

    def about(self):
        self.hide_show()
        self.game.snake.set_about_mode()    

    def help(self):
        self.hide_show()
        self.game.snake.mode = MODE_HELP 

    def exit_game(self):
        self.game.snake.mode = MODE_EXIT

    def menu_settings(self):
        self.game.snake.mode = MODE_OPTIONS

    def draw(self,surface:pygame.Surface):
        super().draw(surface)       
    