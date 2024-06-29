import sys
import pygame
class AlienInvasion:
    #Overall Class To Mange Gmae Assets And Behaviour
    def __init__(self):
        #Initialize The Game And Create Game Resources
        pygame.init()
        self.screen=pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Alien Invasion")
    def run_game(self):
        #Start The Main Loop For The Game
        while True:
            #Watch For Keyboard And Mouse Events
            for i in pygame.event.get():
                if i.type==pygame.QUIT:
                    sys.exit()
            #Make The Most Recently Drawn Screen Visible
            pygame.display.flip()
if __name__=='__main__':
    #Make A game Instance and Run The Game
     ai=AlienInvasion()
     ai.run_game() 