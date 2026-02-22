# Source - https://stackoverflow.com/a/63435568
# Posted by Girish Hegde
# Retrieved 2026-02-11, License - CC BY-SA 4.0

from tkinter import SE
import pygame

import constants

class Button:
    FONT = "Segoe Print"
    CLR_BTN_RADIUS   = 5

    CLR_BTN      = (220, 220, 220)
    CLR_BTN_CHNG = (255, 0, 0)
    CLR_BTN_HINT = (255, 255, 255)
    BTN_RADIUS   = 5

    def __init__(self, position, size, clr=None, cngclr=None, hint_clr=None, func=None, text='', font_name=FONT, font_size=16, font_clr=[0, 0, 0], image = None):
        if clr == None:
            self.clr = self.CLR_BTN
        else:
            self.clr = clr
        self.size   = size
        self.func   = func
        self.surf   = pygame.Surface(size)
        self.surf1  = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)
        self.image  = image
 
        if cngclr == None:
            self.cngclr = self.CLR_BTN_CHNG

        if self.cngclr == None:
            self.cngclr = self.clr

        if len(self.clr) == 4:
            self.surf.set_alpha(clr[3])

        # text         
        self.font_name= font_name
        self.font_size= font_size  
        self.font     = pygame.font.SysFont(self.font_name, self.font_size)   
        self.txt      = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])
        
        #hints
        
        self.hint     = ''
        self.hint_surf= None
        if hint_clr == None:
            self.hint_clr = self.CLR_BTN_HINT
        else:
            self.hint_clr = hint_clr
       
        self.hide     = False
        self.pressed  = False

        self.draw_surface(self.surf ,self.clr)
        self.draw_surface(self.surf1,self.cngclr)
    
    def reset(self):
        self.clr      = self.CLR_BTN
        self.cngclr   = self.CLR_BTN_CHNG
        self.hint_clr = self.CLR_BTN_HINT
        if self.cngclr == None:
            self.cngclr = self.clr

        self.hint_surf= None
        self.draw_surface(self.surf ,self.clr)
        self.draw_surface(self.surf1,self.cngclr)


    def check_click_not_used(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                print('Pressed: ' + self.txt)
            else:
                if self.pressed:
                    self.pressed = False
                    self.call_back()
                    return True
        return False

    def set_hint(self,hint):
        self.hnt = hint
        if  self.hint_surf == None:
            font_size =  self.font_size - 2
            font_hint = pygame.font.SysFont(self.font_name,font_size)
            self.hint_surf = font_hint.render(self.hint, 1,  self.hint_clr)
        else:
            self.hint_surf = font_hint.render(self.hint, 1, self.hint_clr)

    def draw_surface(self, surf, curclr):
        rect = pygame.Rect(0,0,self.rect.width,self.rect.height)
        if self.BTN_RADIUS == 0:
            surf.fill(curclr)
        else:
            surf.fill(constants.BK)
            pygame.draw.rect(surf, curclr, (0,0,rect.width,rect.height), border_radius=self.BTN_RADIUS)   
       
        surf.blit(self.txt_surf, self.txt_rect)

        if self.image != None:
            x = rect.x
            y = rect.y + rect.height/2 - self.image.get_height()/2
            surf.blit(self.image,(x,y))
    
    def draw(self, screen):  
        if self.mouseover():
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                r = self.rect.copy()
                r.x += 2;
                r.y += 2
                screen.blit(self.surf1, r)
            else:
                screen.blit(self.surf1, self.rect)
                self.draw_hint(screen)
        else:
            screen.blit(self.surf, self.rect)
           

    def draw_not_used(self, screen):      
        over = self.mouseover()

        if self.CLR_BTN_RADIUS == 0:
            self.surf.fill(self.curclr)
            #self.surf.blit(self.txt_surf, self.txt_rect)
        else:
            pygame.draw.rect(self.surf, self.curclr, (0,0,self.rect.width,self.rect.height), border_radius=self.CLR_BTN_RADIUS)  
        
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)
        if self.image != None:
            x = self.rect.x
            y = self.rect.y + self.rect.height/2 - self.image.get_height()/2
            screen.blit(self.image,(x,y))
        if over:
            self.draw_hint(screen)
      
    def draw_hint(self,screen):
        if len(self.hint) > 0 :
            if self.hint_surf == None:
                self.set_hint(self.hint)
            screen.blit(self.hint_surf, (self.rect.x + 5,self.rect.bottom))
    
    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr
            return True
        return False

    def call_back(self, *args):
        if self.func:
            return self.func(*args)

   
class Text:
    def __init__(self, msg, position, clr=[100, 100, 100], font="Segoe Print", font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)


    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)



