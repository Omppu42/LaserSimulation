import pygame
pygame.init()

class ImageButton:
    def __init__(self, pos: tuple, size: tuple, image_path, bg_color=(120,120,120), hover_color=(150,150,150), border=0, border_color=(0,0,0)):
        self.x, self.y = pos
        self.w, self.h = size
        self.pos = pos
        self.size = size

        self.surf = pygame.Surface(self.size)
        self.image = pygame.transform.smoothscale(pygame.image.load(image_path), (self.w, self.h))

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.hovering = False

        self.border = border
        self.border_color = border_color


    def draw(self, screen):
        if self.hovering:
            if self.border == 0:
                self.surf.fill(self.hover_color)
            else:
                self.surf.fill(self.border_color)
                pygame.draw.rect(self.surf, self.hover_color, (self.border, self.border, 
                                                                self.w-self.border*2, self.h - self.border*2))

        elif self.border == 0:
            self.surf.fill(self.bg_color)
        else:
            self.surf.fill(self.border_color)
            pygame.draw.rect(self.surf, self.bg_color, (self.border, self.border, self.w - self.border*2, self.h - self.border*2))

        # image        
        self.surf.blit(self.image, (0,0))

        # if self.center_text:
        #     self.surf.blit(text, (self.w//2-text_width//2,self.h//2-text_height//2))
        # else: self.surf.blit(text, (self.border+5,self.h//2-text_height//2))
        screen.blit(self.surf, self.pos)


    def check_hover(self, mouse_pos):
        self.hovering = (
            mouse_pos[0] >= self.x
            and mouse_pos[0] <= self.x + self.w
            and mouse_pos[1] >= self.y
            and mouse_pos[1] <= self.y + self.h)


    def check_click(self):
        return bool(self.hovering)