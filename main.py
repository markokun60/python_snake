import pygame
import random
import time
import pygame_menu as pm
from pygame_menu import themes

import constants
import menu_settings 
from  game import   *
from  snake import  Snake
from  button import Button

pygame.init()
pygame.font.init()
pygame.mixer.init()

field_rect = pygame.Rect(constants.FIELD_BORDER_LEFT,constants.FIELD_BORDER_TOP,constants.WIDTH,constants.HEIGHT)
window = pygame.display.set_mode((constants.WIDTH_WOINDOW,constants.HEIGHT_WINDOW))

big_text_font  = pygame.font.SysFont(constants.FONTS, 18,italic = True )
info_text_font = pygame.font.SysFont(constants.FONTS, 16,bold=True)

#welcome_font = pygame.font.SysFont("comicsans", 16)

show_settings_menu = False
def close_menu_settings():
    global show_settings_menu
    show_settings_menu = False
    mainSettings.disable()
    hide_show_buttins()
    game.save_config()

game  = Game(big_text_font,info_text_font)
pygame.display.set_icon(game.SNAKE_IMAGE)
pygame.display.set_caption("Snake")

ms =  menu_settings.MenuSettings(game)
mainSettings = ms.create(close_menu_settings)

def about():
    hide_show_buttins()
    game.snake.set_about_mode()

def help():
    hide_show_buttins()
    game.snake.mode = constants.MODE_HELP

def back():
    hide_show_buttins()
    game.snake.mode = constants.MODE_WELCOME

def menu_settings():
    hide_show_buttins()
    mainSettings.enable()
    global show_settings_menu
    show_settings_menu = True

def exit_game():
    game.snake.mode = constants.MODE_EXIT

imgSnake   = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'snake_small.png'))
imgStart   = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'start.png'))
imgHelp    = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'help.png'))
imgOptions = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'options.png'))
imgBack    = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'cancel.png'))
imgExit    = pygame.image.load(os.path.join(constants.ASSET_FOLDER,'exit.png'))

x_button = 80
y_button = 100
W_BUTTON = 110
H_BUTTON = 50

CLR_BTN = (220, 220, 220)
CLR_BTN_CHNG = (255, 0, 0)

btnStart = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), clr=CLR_BTN, cngclr=CLR_BTN_CHNG, func=game.start, text='Start')
btnStart.image = imgStart

btnBack = Button(position=(x_button, y_button),  size=(W_BUTTON, H_BUTTON), clr=CLR_BTN, cngclr=CLR_BTN_CHNG, func=back, text='Back')
btnBack.hide = True
btnBack.image = imgBack

x_button += W_BUTTON
x_button += 10
btnAbout = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), clr=CLR_BTN, cngclr=CLR_BTN_CHNG, func=about, text='About')
btnAbout.image = imgSnake

x_button += W_BUTTON
x_button += 10
btnHelp = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), clr=CLR_BTN, cngclr=CLR_BTN_CHNG, func=help, text='Help')
btnHelp.image = imgHelp

x_button += W_BUTTON
x_button += 10
btnOptions = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), clr=CLR_BTN, cngclr=CLR_BTN_CHNG, func=menu_settings, text='Options')
btnOptions.image = imgOptions

x_button += W_BUTTON
x_button += 10
btnExit = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), clr=CLR_BTN, cngclr=CLR_BTN_CHNG, func=exit_game, text='Exit')
btnExit.image = imgExit


buttons = [btnStart,btnAbout,btnHelp,btnBack,btnOptions,btnExit]
def hide_show_buttins():
    for b in buttons:
        b.hide = not b.hide
 
 
def draw_buttons():
    for b in buttons:
        if not b.hide:
            b.draw(window)


def draw_exit_message():
    source = f"""
        
        Buy {game.player_name}
    """
    fnt  = pygame.font.SysFont(constants.FONTS, 36,italic = True )
    text = fnt.render(source,1,constants.TEXT_COLOR)
    window.blit(text,(constants.WIDTH_WOINDOW/2 - text.get_width()/2,constants.HEIGHT_WINDOW/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def draw():
    window.fill(constants.BK)
    if game.snake.mode == constants.MODE_WELCOME:
        draw_welcome_text(window,big_text_font)
        draw_buttons()
     
    elif game.snake.mode == constants.MODE_ABOUT:
        game.draw_about_text(window)
        draw_buttons()

    elif game.snake.mode == constants.MODE_HELP:
        game.draw_help_text(window)
        draw_buttons() 
    elif game.snake.mode == constants.MODE_EXIT:
        draw_exit_message()
        return
    else:
        pygame.draw.rect(window,constants.FIELD_COLOR,field_rect)
        game.draw_play(window)
    pygame.display.update()


def main():
    global show_settings_menu
    FPS = 3
    clock = pygame.time.Clock()
    run = True
   
    while run:
        if show_settings_menu:          
            mainSettings.mainloop(window)
            show_settings_menu = False
            continue
       
        game.get_time()
    
        if game.snake.mode == constants.MODE_EXIT:
            run = False
            break
        elif game.snake.mode == constants.MODE_AGONY:
            clock.tick(60)
        else:      
            clock.tick(FPS * (game.level+1))  
            
        events = pygame.event.get()    

        for event in events:
            if event.type == pygame.QUIT:
                game.snake.mode = constants.MODE_EXIT
                run = False
                break 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for b in buttons:
                        if not b.hide:
                            if b.rect.collidepoint(pos):
                                b.call_back()
                                break

            elif event.type == pygame.KEYDOWN:
                if game.snake.mode != constants.MODE_PLAY:
                    if event.key == pygame.K_SPACE: 
                        if game.snake.mode == constants.MODE_GAME_OVER:
                            game.snake.mode = constants.MODE_WELCOME
                        else:
                            game.start()
                    elif event.key == pygame.K_F1:
                        help()
                    elif event.key == pygame.K_F2:
                        about()
                  
                elif event.key == pygame.K_SPACE:
                    game.pause_resume()
                   
                elif not game.snake.is_paused:
                    cmd = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        cmd = constants.CMD_LEFT
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                        cmd = constants.CMD_RIGHT   
                    elif event.key == pygame.K_UP or  event.key == pygame.K_w:
                        cmd = constants.CMD_UP
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        cmd = constants.CMD_DOWN
                    elif  event.key == pygame.K_z:
                        cmd = constants.CMD_T_LEFT
                    elif  event.key == pygame.K_x:
                        cmd = constants.CMD_T_RIGHT
                    
                    if cmd != 0:
                        game.commands.append(cmd)

        if game.snake.mode == constants.MODE_AGONY:
            if not game.grave.update():
                game.snake.mode = constants.MODE_GAME_OVER
        elif game.snake.is_moving():
            game.step()
        draw()

    pygame.quit()


if __name__ == "__main__":
    main()