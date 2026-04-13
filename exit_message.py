import pygame
from draw_html import DrawHTML
from constants import *

class ExitMessage:
    def __init__(self,game,color):
        self.game = game
        if self.game.total_games == 0:
            source = f"Goodbye  <b> {self.game.player_name}</b>"
        else:
            source = f"""<i>
    It was fun to play with you.

    # of games {self.game.total_games}
    Your best result {SnakeStatus[self.game.best_status]}

    But now it's time to say
    Goodbye  <b> {self.game.player_name}</b>

        """
        fnt  = pygame.font.SysFont(Control.FONT, 36)
        self.draw_html = DrawHTML(source,fnt,color)

    def draw(self,window):
        x = (WIDTH_WINDOW  - self.draw_html.width)  //2
        y = (HEIGHT_WINDOW - self.draw_html.height - self.game.SNAKE_IMAGE.get_height()) //2 - 12
        w,h = self.draw_html.draw(window,(x,y))
        i = self.game.best_status
        img = self.game.get_snake_image_for_status(i)   
        y += h
        x = (WIDTH_WINDOW  - img.get_width())  //2
        window.blit(img,(x,y))
        pygame.display.update()