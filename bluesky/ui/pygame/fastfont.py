import pygame as pg

class Fastfont:
    """ 
    Faster font for printing graphically, renders only at creation

    Methods:
        CFastfont(screen,name,size,color,bold,italic) :  constructor, renders font
        
        printat(screen,x,y,text): print text at x,y, at screen window (blit)
        setpos(x,y)   : not used anymore?

    Members: see create

    Created by  : Jacco M. Hoekstra
    """

    def __init__(self,screen,name,size,color,bold,italic):
        self.swposx = -1  # Default x = left side
        self.swposy = -1  # Default y = top

        self.font = pg.font.SysFont(name,size,bold,italic)
        self.color = color
        self.screen = screen

        # Cache glyphs on demand so non-ASCII text such as Chinese can render too.
        self.chmaps = {}
        self.linedy = self.font.get_linesize()
        return      

    def printat(self,screen,x,y,text):
        text = str(text)
        glyphs = []
        width = 0

        for ch in text:
            if ch not in self.chmaps:
                glyph = self.font.render(ch, False, self.color).convert_alpha(self.screen)
                self.chmaps[ch] = glyph
            glyph = self.chmaps[ch]
            glyphs.append(glyph)
            width += glyph.get_width()

        txtimg = pg.Surface((max(width, 1), self.linedy)) # Standard height bitmap
        txtimg = txtimg.convert_alpha(screen)
        txtimg.fill((0, 0, 0, 0))
        
        ix = 0
        for glyph in glyphs:
            dest = glyph.get_rect()
            dest.top = 0
            dest.left = ix
            ix += glyph.get_width()
            txtimg.blit(glyph,dest)# Removed pg.BLEND_ADD which broke it on Windows machine

        dest = txtimg.get_rect()

        # Set position
        if self.swposx <0:
            dest.left = x
        elif self.swposx>0:
            dest.right = x
        else:
            dest.centerx = x

        if self.swposy <0:
            dest.top = y
        elif self.swposy>0:
            dest.bottom = y
        else:
            dest.centery = y

        # Paste it onto the screen
        screen.blit(txtimg,dest)# Removed pg.BLEND_ADD which broke it on Windows machine

        return

    def setpos(self,swposx,swposy):
        self.swposx = swposx
        self.swposy = swposy
        return
