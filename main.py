import pygame
import sys 
from  os.path import abspath

import constants      
from main_form          import MainForm
from game               import *
from exit_message       import ExitMessage
from snake_ai           import SnakeAI

pygame.init()
pygame.font.init()
pygame.mixer.init()

def get_resource_path():
   base_path = getattr(sys, '_MEIPASS', abspath("."))
   return os.path.join(base_path,constants.ASSET_FOLDER)

window = pygame.display.set_mode((constants.WIDTH_WINDOW,constants.HEIGHT_WINDOW))

resource_folder = get_resource_path()
game = Game(window,resource_folder)

pygame.display.set_icon(game.SNAKE_IMAGE)
pygame.display.set_caption(constants.APP_NAME)
constants.set_boars_size(game.board_size)

game.load_images()
snake_ai = SnakeAI(game)
main_form = MainForm(game,snake_ai)

def draw_exit_message():
    em = ExitMessage(game,constants.TEXT_COLOR )
    em.draw(window)
    pygame.time.delay(3000)

def draw():
    window.fill(constants.BK)
    if game.snake.mode == constants.MODE_WELCOME:
        game.draw_welcome_text(window)
        main_form.draw(window)
     
    elif game.snake.mode == constants.MODE_ABOUT:
        main_form.draw(window)
        game.draw_about_text(window)
     
    elif game.snake.mode == constants.MODE_HELP:
        main_form.draw(window)
        game.draw_help_text(window)
     
    elif game.snake.mode == constants.MODE_EXIT:
        draw_exit_message()
        return
    elif game.snake.mode == constants.MODE_OPTIONS:
        main_form.form_options.draw(window)
    else:
        game.draw_play(window)
    pygame.display.update()

def main():
    FPS = 3
    clock = pygame.time.Clock()
    run = True

    while run:       
        game.get_time()
        if game.snake.mode == constants.MODE_EXIT:
            run = False
            break
        elif game.snake.mode == constants.MODE_AGONY:
            clock.tick(60)
        else:   
            fps  = FPS * (game.level + 1)
            clock.tick(fps)  
         
        cmd = 0    
        events = pygame.event.get()    

        for event in events:
            if event.type == pygame.QUIT:
                game.snake.mode = constants.MODE_EXIT
                run = False
                break 
            elif game.snake.mode == constants.MODE_OPTIONS:
                main_form.form_options.handle_controls_events(event)     
            elif game.snake.mode in constants.MODES_MENU:
                main_form.handle_controls_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:            
                if event.button == 1:
                    pos = pygame.mouse.get_pos()                 
                    if game.snake.mode == constants.MODE_PLAY:
                        x, y = pos
                        if x <  constants.FIELD_BORDER_LEFT and y > constants.FIELD_BORDER_TOP and y < constants.HEIGHT - constants.FIELD_BORDER_RIGHT:
                            cmd = constants.CMD_LEFT
                        elif x > constants.WIDTH - constants.FIELD_BORDER_RIGHT and y > constants.FIELD_BORDER_TOP and y < constants.HEIGHT - constants.FIELD_BORDER_RIGHT:
                            cmd = constants.CMD_RIGHT
                        elif y < constants.FIELD_BORDER_TOP:
                            cmd = constants.CMD_UP
                        elif y >=  constants.HEIGHT - constants.FIELD_BORDER_RIGHT:
                            cmd = constants.CMD_DOWN

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.snake.mode == constants.MODE_GAME_OVER:
                        game.snake.mode = constants.MODE_WELCOME
                    elif game.snake.mode == constants.MODE_PLAY :
                        game.pause_resume()
                    elif game.snake.mode == constants.MODE_CMP_PLAY :
                        game.pause_resume()    
                    else:
                        game.start()   
                            
                elif game.input_enabled():
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
                    cmd = 0

        if game.snake.mode == constants.MODE_AGONY:
            if not game.grave.update():
                game.snake.mode = constants.MODE_GAME_OVER
        elif game.snake.is_moving():
            if game.play_mode == constants.AI:
                snake_ai.move()
            game.step()
            #game.pause_resume()
        draw()

    pygame.quit()
    sys.exit()



#def hide_console():
   #subprocess.Popen(["python", "snake.py"], creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == "__main__":
    #hide_console()
    main()

