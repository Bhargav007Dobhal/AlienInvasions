import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
    #A Class To Manage Bullets Fired From The Ship
    def __init__(self,ai_game):
        #Create A Bullet Object At The Ship's Current Position
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color
        #Create A Bullet Rect At (0,0) and Then Set The Correct Position
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop
        #Store The BUllet's Position As  A Float
        self.y=float(self.rect.y)
    def update(self):
        #Move The Bullet Up The Screen
        #Update's The Exact Position Of The Bullet
        self.y-=self.settings.bullet_speed
        self.rect.y=self.y
    def draw_bullet(self):
        #Draw The Bullet To The Screen
        pygame.draw.rect(self.screen,self.color,self.rect)
        




