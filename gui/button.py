import pygame
pygame.init()

class Button:
    def __init__(self, x, y, width, height, bg_color=(120,120,120), hover_color=(150,150,150), text="Text", 
                 text_color=(0,0,0), font_size=18, center_text = True, border=0, border_color=(0,0,0), font=None):
        self.x = x - width / 2
        self.y = y - height / 2
        self.width = width
        self.height = height
        self.pos = (self.x, self.y)
        self.size = (width,height)
        self.image = pygame.Surface(self.size)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.hovering = False

        self.font = pygame.font.Font(None, font_size) if font is None else font
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.center_text = center_text
        self.border = border
        self.border_color = border_color


    def draw(self, screen):
        if self.hovering:
            if self.border == 0:
                self.image.fill(self.hover_color)
            else:
                self.image.fill(self.border_color)
                pygame.draw.rect(self.image, self.hover_color, (self.border, self.border, self.width-self.border*2, self.height-self.border*2))

        elif self.border == 0:
            self.image.fill(self.bg_color)
        else:
            self.image.fill(self.border_color)
            pygame.draw.rect(self.image, self.bg_color, (self.border, self.border, self.width-self.border*2, self.height-self.border*2))

        #text        
        text = self.font.render(self.text, True, self.text_color)
        text_width = text.get_width()
        text_height = text.get_height()

        if self.center_text:
            self.image.blit(text, (self.width//2-text_width//2,self.height//2-text_height//2))
        else: self.image.blit(text, (self.border+5,self.height//2-text_height//2))
        screen.blit(self.image, self.pos)


    def check_hover(self, mouse_pos):
        self.hovering = (
            mouse_pos[0] >= self.x
            and mouse_pos[0] <= self.x + self.width
            and mouse_pos[1] >= self.y
            and mouse_pos[1] <= self.y + self.height)


    def check_click(self):
        return bool(self.hovering)