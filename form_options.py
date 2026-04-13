import pygame
from  os.path import join
from importlib.resources import files

from controls.form       import Form
from controls.button     import Button
from controls.checkbox   import Checkbox
from controls.combobox   import Combobox 
from controls.checkGroup import CheckGroup,reset_all_groups
from controls.textBox    import InputBox 
from controls.label      import Label 
from controls.listbox    import ListBox
from controls.image      import Image
from controls.controls   import *
from controls.message    import Message

from constants import *

class Form_Options(Form):

   def __init__(self,parent,game,images):
      super().__init__()
      self.parent = parent
      self.game = game
      self.images = images
      self._create_images()
      self._create_help_forms()
      Control.form = self
      self._create_controls()
      Control.form = parent

      self.old_controls_settings = save_controls_settings()
      self.old_game_settings     = self.game.save_settings()
      
   def _create_help_forms(self):
      source = files(RESOURCES).joinpath('grow_by_food_ony.txt').read_text(encoding='utf-8')
      self.grow_by_food_only_msg = Message(source)

   def _create_images(self):
        root = self.game.resource_folder 
        self.imgUndo    = pygame.image.load(join(root,'undo.png')).convert_alpha()
        self.imgDefault = pygame.image.load(join(root,'default.png')).convert_alpha()
        self.imgInfo    = pygame.image.load(join(root,'info.png')).convert_alpha()
        Message.image_ok= pygame.image.load(join(root,'ok.png')).convert_alpha()

   def create_themes_box(self,x,y):
      i = 0
      cur_theme = get_theme()
      theme_index = 0
      for theme in Control.THEMES_BY_NAME.keys():
         if theme == cur_theme:
               theme_index = i
               break
         i += 1
      cboThemes = Combobox('cboThemes',position=(x,y),width=40,values=list(Control.THEMES_BY_NAME.keys()),index=theme_index,func=self.theme) 
      return cboThemes 
   
   def create_fonts_box(self,x,y):
      fonts = sorted(pygame.font.get_fonts())

      #fonts = [x for x in fonts if x is not None]

      try:
         font_index = fonts.index(Control.FONT)
      except:
         font_index = 0
     
      cboFonts = Combobox('cboFonts',position=(x,y),width=40,values=fonts,index=font_index,func=self.change_font,visible_size=7) 
      return cboFonts  
    
   def _create_help_button(self,c,msg_form,f):
      x = c.rect.right + 4
      y = c.rect.top + (c.rect.height - self.imgInfo.get_height()) //2  
      h = self.imgInfo.get_height()

      name = 'btn' + c.name[3:] + 'help'
      b= Image(name,position=(x,y),image=self.imgInfo,func=f)
      msg_form.generate(c.rect.left,c.rect.bottom)
      return b
       

   def _create_controls(self):
      big_font_size = Control.FONT_SIZE + 4
      x = W_BUTTON // 2 + 24
      y = self.parent.yButton 
      DY = 25

      imgBack = self.images['back']
      btnBack = Button('btnBackOptions',position=(x, y),  size=(W_BUTTON, H_BUTTON),  func=self.back, text='Back',image= imgBack)
      btnBack.hint  = "Back to main menu" 
      btnBack.key   = pygame.K_ESCAPE 

      (xLeft,y) = self.next_right(40)

      btnUndo = Button('btnUndo',position=(x ,btnBack.rect.bottom + H_BUTTON/2 + DY), font_name=Control.FONT_DEFAULT , size=(W_BUTTON, H_BUTTON),  
                       func=self.undo, text='Undo',image=self.imgUndo) 
      btnUndo.hint = "Restore old settings"
      
      btnDefault = Button('btnDefalt',position=(x ,btnUndo.rect.bottom + H_BUTTON/2 + DY), font_name=Control.FONT_DEFAULT , size=(W_BUTTON, H_BUTTON), 
                          func=self.set_default, text='Default',image=self.imgDefault ) 
      btnDefault.hint = "Set default settings"

      DX = 4
      DY = 12
     
      Label('lblSettings',position=(xLeft, y),text='Game settings',font_size=big_font_size)
      (x,y) = self.next_down(DY)
     
      lblUserName = Label('lblUser',position=(x, y),  text='Player name:')
      (xv,y) = self.next_right(DX)
      txtUserName = InputBox('txtUser',position=(xv,y),width=120,text=self.game.player_name,func = self.player_name)
      txtUserName.add_linked_controls(lblUserName)
      #
      (x,y) = self.next_down(DY,lblUserName)
      self.chkSound = Checkbox('chkSounds',position=(x,y),text='Sounds',checked= self.game.is_sound,func=self.sound)

      (x,y) = self.next_down(DY)
      self.chkGrid = Checkbox('chkGrid',position=(x,y),text='Grid',checked= self.game.is_grid,func=self.grid) 
      
      (x,y) = self.next_down(DY)
      lblLevel= Label('lblLevel',position=(x, y),text='Level:')
      (xv,y) = self.next_right(DX)
      xv += 16
      self.lstLevel = ListBox('lstLevel',position=(xv,y),values=list(LEVELS.keys()),index=self.game.level,func=self.set_level) 
      self.lstLevel.add_linked_controls(lblLevel)

      (x,y) = self.next_down(DY)
      lblSize = Label('lblSize',position=(xLeft, y),text='Size:')
      self.lstSize = ListBox('lstSize',position=(xv,y),values=SIZE_NAMES,index= self.game.board_size,func=self.sizes ) 
      self.lstSize.add_linked_controls(lblSize)
 
      (x,y) = self.next_down(DY)
      lblTheme =  Label('lblTheme',position=(xLeft ,y),text='Theme:') 
      self.cboThemes = self.create_themes_box(xv,y)
      self.cboThemes.add_linked_controls(lblTheme)
      #
      rect = self.get_control_rect()
      #
      (x,y) = self.next_down(DY)
      lblFonts = Label('lblFonts',position=(xLeft, y),text='Fonts:')
      self.cboFonts = self.create_fonts_box(xv,y)
      self.cboFonts.add_linked_controls(lblFonts)
      
      # =========== Rules ============

      y  =  rect.top
      x  =  rect.right + 70

      Label('lblRules',position=(x, y),text='Rules',font_size=big_font_size)
      (x,y) = self.next_down(DY)

      self.chkGrowByfoodOnly = Checkbox('chkGrowByfoodOnly',position=(x,y),text='Grow by food only',checked= self.game.is_grow_by_food_only,func=self.grow_by_food_only) 
      (x,y) = self.next_down(DY)
      self._create_help_button(self.chkGrowByfoodOnly ,self.grow_by_food_only_msg,self.help_growByfoodOnlyHelp)
  
      
      self.chkFoodAlways = Checkbox('chkFoodAlways',position=(x,y),text='Food always available',
                                    checked= self.game.is_food_always,func=self.food_always) 
      (x,y) = self.next_down(DY)

      self.chkEnemy= Checkbox('chkEnemy',position=(x,y),text='Is mongooses',checked= self.game.is_enemies,func=self.enemy) 
      
      (x,y) = self.next_down(DY+8)
      i = 0 if self.game.max_foods_on_fields == 1 else 0
      self.chgFoodOnField = CheckGroup(options=["One apple","Multiple apples"],cur_choice=i,x=x,y=y,caption="Food on field",name="fdOnFld",
                                  multi_sellect=False,func=self.food_on_field)
      (x,y) = self.next_down(DY+12)

      
      action_index =  self.get_action_index() 
      lblAction = Label('lblAction',position=(x, y),text='Play:')
      (xv,y) = self.next_right(DX)
      self.cboPlayer = Combobox('cboPlayer',position=(xv,y),width=40,values=list(ACTIONS.keys()),index= action_index,func=self.players ) 
      self.cboPlayer.add_linked_controls(lblAction)
      #print(len(self.controls))

      (x,y) = self.next_down(DY)
      self.chkAIMode = Checkbox('chkAIMode',position=(x,y),text='AI with learning',checked= self.game.ai_with_learning,func=self.AI_learningood) 
      self.chkAIMode.hide = (self.game.play_mode != AI)

      if self.game.is_grow_by_food_only:
         self.chkFoodAlways.enabled = False
         self.chkFoodAlways.checked = True 

   def get_action_index(self):
      i = 0
      action_index = 0
      for a in ACTIONS.values():
         if a == self.game.play_mode:
               return i
               break
         i += 1 
      return 0

   def back(self):
      #selflUser.parent.hide_show()
      self.game.snake.mode = MODE_WELCOME
      self.game.save_config()
      self.game.for_board_size()
      self.game.load_statistics()
  
   def player_name(self,value):
      self.game.player_name = value

   def sound(self,value):
      self.game.is_sound = value

   def grid(self,value):
      self.game.is_grid = value

   def set_level(self,value1,value2):
      self.game.level = int(value2)

   def grow_by_food_only(self,value):
      self.game.is_grow_by_food_only = value
      if value :        
         self.chkFoodAlways.checked = True
         self.chkFoodAlways.enabled = False
      else:
         self.chkFoodAlways.enabled = True 

   def help_growByfoodOnlyHelp(self):
      self.grow_by_food_only_msg.hide = False   

   def sizes(self,value,index):
      self.game.set_board_size(index)

   def food_always(self,value):
      self.game.is_food_always = value


   def enemy(self,value):
      self.game.is_enemies = value

   def food_on_field(self,i,checked):
      if i == 0 and checked:
         self.game.max_foods_on_fields == 1
      else:
         self.game.max_foods_on_fields == 0
      
   def AI_learningood(self,value):
      self.game.ai_with_learning = value

   def players(self,value,index):
      self.game.play_mode = ACTIONS[value]
      self.parent.set_start_hint()
      self.chkAIMode.hide = self.game.play_mode != AI

   def update_theme(self):
      theme = self.cboThemes.text
      mode = Control.THEMES_BY_NAME[theme]
      set_contols_mode(mode)
      set_shema_by_name()
      reset_all_controls()  
      reset_all_groups() 

   def theme(self,value,index):
      self.update_theme()

   def change_font(self,value,index):
      update_controls_font(value)
      reset_all_groups() 
      self.game.reset()

   def set_default(self):
      default_contols_setings()
      self.game.set_default()
      self._update_controls()

   def undo(self):
       restore_controls_settings( self.old_controls_settings)
       self.game.restore_settings(self.old_game_settings)
       self._update_controls()
   
   def _update_controls(self):

    
      self.cboFonts.setValue(Control.FONT)
      self.cboThemes.setValue(get_theme())
      self.chkSound.checked = self.game.is_sound
      self.chkGrid.checked  = self.game.is_grid
      self.lstLevel.index   = self.game.level
      self.lstSize.index    = self.game.board_size
      self.chkGrowByfoodOnly.checked = self.game.is_grow_by_food_only 
      self.chkFoodAlways.checked = self.game.is_food_always 
      self.chkEnemy.checked      = self.game.is_enemies
      self.chgFoodOnField.select (self.game.max_foods_on_fields)
      self.cboPlayer.setIndex(self.get_action_index()) 
      self.chkAIMode.checked     = self.game.ai_with_learning
   
      self.chkFoodAlways.enabled = not self.game.is_grow_by_food_only
      if self.game.is_grow_by_food_only :  
         self.chkFoodAlways.checked = True   

   def draw(self, surface: pygame.Surface):
      super().draw(surface)
      if not self.grow_by_food_only_msg.hide :
         self.grow_by_food_only_msg.draw(surface)

   def handle_controls_events(self,event):     
      if not self.grow_by_food_only_msg.hide :
         self.grow_by_food_only_msg.handle_controls_events(event)  
         return
      super().handle_controls_events(event)


       