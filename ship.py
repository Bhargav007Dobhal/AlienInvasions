import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    #A Class To Manange The Ship
    def __init__(self,ai_game):
        #initialize The Ship And Set It's Starting Position
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()
        #Load The Ship Image And Get It's Rect
        self.image=pygame.image.load('Images/ship.bmp')
        self.rect=self.image.get_rect()
        #Start Each New Ship At The Bottom Center Of The Screen
        self.rect.midbottom=self.screen_rect.midbottom
        #Store A  Float For The Ship's Exact Horizontal Position
        self.x=float(self.rect.x)
        #Movement Flag , Start With A Ship That's Not Moving
        self.moving_right=False
        self.moving_left=False
    def center_ship(self):
        #Center The Ship On Screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    def update(self):
        #Update The Ship's Position Based On The Movement Flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
        #Update rect object from self.x
        self.rect.x=self.x
    def blitme(self):
        #Draw The Ship At It's Current Location
        self.screen.blit(self.image , self.rect)