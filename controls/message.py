import pygame
from controls.button import Button
from controls.label  import Label
from controls.controls import Control
from controls.form import Form

class Message(Form):
    image_ok = None
    def __init__(self,message):
        super().__init__()
        self.is_ok_button = True
        self.message = message
        self.hide = True
    
    def generate(self,x,y): 
        old_form = Control.form 
        Control.form = self
        w_button = 80

        label = Label('lblMessage',position=(x,y),text=self.message,font_size=Control.FONT_SIZE-4,font_italic=True)
        btn_height = 24
        y = label.rect.bottom + btn_height // 2 + 12
        if self.is_ok_button:
            btnOk = Button("btnOk", position=(x,y),size=(w_button,btn_height),text="OK",image=Message.image_ok,func=self.close)                        
            btnOk.rect.left = x + (label.get_width() - btnOk.rect.width)//2
            btnOk.key   = pygame.K_ESCAPE 
        self.rect = self.get_control_rect()
        h = 8
        self.rect.left -= h 
        self.rect.top  -= h
        self.rect.width += 2 * h
        self.rect.height += 2 * h
        Control.form = old_form
       
    def close(self):
        self.hide = True


    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface,Control.BK,self.rect)
        pygame.draw.rect(surface,Control.CLR_BORDER,self.rect,1)
        super().draw(surface)
      


        

