import pygame_menu as pm
from pygame_menu import themes

import constants

from  game import   *
from  snake import  Snake
from  button import Button

class MenuSettings:
    FONT_SIZE = 18
    THEME     = themes.THEME_BLUE
    THEMS     = []

    for t in constants.THEMES:
        THEMS.append((t,t))
    
    LEVELS=[
        ("Easy"  ,"0"),
        ("Medium","1"),
        ("Hard"  ,"2"),
        ("Crazy" ,"3")
    ]

    PLAYERS= [
        ("Human","H"),
        ("AI"   ,"A")
    ]

    SIZES = [
        ("Small"    ,"0"),
        ("Standard" ,"1"),
        ("Large"    ,"2")
    ]

    def __init__(self,game):
        self.game = game

    def get_player_name(self,value):
        self.game.player_name = value

    def get_sound(self,value):
        self.game.is_sound = value

    def get_grid(self,value):
        self.game.is_grid = value

    def get_theme(self,value1,value2):
        if constants.set_shema_by_name(value2):
            self.game.theme = value2
            
    def get_level(self,value1,value2):
        self.game.level = int(value2)

    def get_grow_by_food_only(self,value):
        self.game.is_grow_by_food_only = value


    def get_sizes(self,value1,value2):
        self.game.set_board_size(int(value2))

    def get_food_always(self,value):
        self.game.is_food_always = value

    def get_players(self,value1,value2):
        if value2 == "A":
            self.game.is_AI = True
        else:
            self.game.is_AI = False


    def create(self,close_menu_settings):
        menuSettings = pm.Menu('Settings', 600, 400, theme=self.THEME)
        # Adjusting the default values
        menuSettings._theme.widget_font_size  = self.FONT_SIZE
        menuSettings._theme.widget_font_color = constants.BLACK
        menuSettings._theme.widget_alignment  = pm.locals.ALIGN_LEFT

        theme_index =constants.THEMES.index(self.game.theme)
        player_index = 1 if self.game.is_AI else 0


        menuSettings.add.text_input('Player name: '    , default=self.game.player_name ,maxchar=20,onchange=self.get_player_name)
        menuSettings.add.toggle_switch(title="Sounds:" , default=self.game.is_sound    ,toggleswitch_id="sound",onchange=self.get_sound)
        menuSettings.add.toggle_switch(title="Grid:"   , default=self.game.is_grid     ,toggleswitch_id="grid" ,onchange=self.get_grid)

        menuSettings.add.dropselect(title="Theme:"     , default=theme_index           ,items = self.THEMS ,dropselect_id="Theme",onchange=self.get_theme)
        menuSettings.add.dropselect(title="Level:"     , default=self.game.level       ,items = self.LEVELS,dropselect_id="Level",onchange=self.get_level)
        menuSettings.add.dropselect(title="Size:"      , default=self.game.board_size  ,items = self.SIZES ,dropselect_id="Size" ,onchange=self.get_sizes)

        #menuSettings.add.button(title="Back"           , action=close_menu_settings,background_color = (127,127,127))
       
        menuRules = pm.Menu('Rules', 600, 400, theme=self.THEME)
        menuRules._theme.widget_font_size  = self.FONT_SIZE
        menuRules._theme.widget_font_color = constants.BLACK
        menuRules._theme.widget_alignment  = pm.locals.ALIGN_LEFT
        menuRules.add.toggle_switch(title="Grow by food only:"    , default=self.game.is_grow_by_food_only ,toggleswitch_id="grow_food_only",onchange=self.get_grow_by_food_only)
        menuRules.add.toggle_switch(title="Food always available" , default=self.game.is_food_always       ,toggleswitch_id="food_always",onchange=self.get_food_always)
        menuRules.add.dropselect(title="Player:"     , default=player_index           ,items = self.PLAYERS ,dropselect_id="players",onchange=self.get_players)
 
        # Creating the main menu
        mainMenu = pm.Menu(title="Options",width=300,height=300,theme=self.THEME)
        mainMenu._theme.widget_font_size  = self.FONT_SIZE
        mainMenu._theme.widget_font_color = constants.BLACK
        mainMenu._theme.widget_alignment  = pm.locals.ALIGN_CENTER


        b = mainMenu.add.button(title="Settings", action=menuSettings,
                        font_color=constants.WHITE,background_color=constants.GRAY)
        b.set_margin(10, 10)
        b = mainMenu.add.button(title="Rules", action=menuRules,
                        font_color=constants.WHITE, background_color=constants.GRAY)
        b.set_margin(10, 10)
        b = mainMenu.add.button(title="Back" , action=close_menu_settings,font_color=constants.WHITE,background_color = constants.GRAY)
        b.set_margin(10, 10)
       

       
        return mainMenu

