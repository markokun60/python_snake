from re import I
import pygame

class DrawHTML:
    def __init__(self,source:str,fnt:pygame.font.Font, color:tuple):
        self.source = source.strip().replace('\n','<hr>')
        self.text = []
        self.font = fnt
        self.color = color
        t = self._parse(self.source)
        while t is not None:
            t = self._parse(t)
        #print(self.text)
        self.width, self.height = self.draw(None,(0,0))

    def _parse(self,source):
        i0 = source.find('<')
        if i0 == -1:
            self.text.append(('',source))
            return None
        i1 = source.find('>',i0)
        if i1 == -1:
            print('Invalid HTML: missing ">"')
        s   = source[:i0]
        self.text.append(('',s))
        tag = source[i0+1:i1] 
        self.text.append((tag,''))
        return source[i1+1:]

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height


    def draw(self,surface:pygame.Surface,position:tuple):
        pos_start = position
        text_surf = None
        width = 0
        for t in self.text:
            tag = t[0]
            s   = t[1]
            if tag == 'b':
                self.font.set_bold(True)
            elif tag == '/b':
                self.font.set_bold(False)
            elif tag == 'i':
                self.font.set_italic(True)
            elif tag == '/i':
                self.font.set_italic(False)
            elif tag == 'u':
                self.font.set_underline(True)
            elif tag == '/u':
                self.font.set_underline(False)
            elif tag == 'hr':
                if text_surf is not None:
                    position = (pos_start[0],position[1]+ text_surf.get_height()) 
            else:
                text_surf = self.font.render(s,1,self.color)
                if surface != None:
                    surface.blit(text_surf,position)
                position = (position[0]+text_surf.get_width(),position[1])
                if width < position[0] - pos_start[0]:
                    width = position[0] - pos_start[0]
                   
        return width,position[1] - pos_start[1] + text_surf.get_height() if text_surf is not None else 0


        





