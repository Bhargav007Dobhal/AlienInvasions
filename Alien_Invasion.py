import sys
from time import sleep
import pygame
from settings import Settings
from game_Stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
class AlienInvasion:
    #Overall Class To Manage Game Assets And Behaviour
    def __init__(self):
        #Initialize The Game And Create Game Resources
        pygame.init()
        self.clock=pygame.time.Clock()
        self.settings=Settings()
        #The Code Commented Out Below Sets The Screen In Full Screen Mode
        # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width=self.screen.get_rect().width
        # self.settings.screen_height=self.screen.get_rect().height
        #The Code Of Line Below Will Set The Specified Screen Size
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #Create An Instance To Store Game Statistics
        # And Create A Scoreboard
        self.stats=GameStats(self)
        self.sb=Scoreboard(self) 
        #Create An Instance To Store Game Statistics
        # self.stats=GameStats(self)
        self.ship=Ship(self)
        #An Instance Of pygame.sprite.Group clas/A Group that holds bulletss in __init__()
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        #Start Alien Invasion In An Active State
        self.game_active=False

        #Make The Play Button
        self.play_button = Button(self , "Play")

    def run_game(self):
        #Start The Main Loop For The Game
        while True:
            #Watch For Keyboard And Mouse Events
         self._check_events()
         if self.game_active:
          self.ship.update()
          self._update_bullets()
          self._update_aliens()
         self._update_screen()
         self.clock.tick(60)
    def _check_events(self):
        #Responds To Keypress And Mouse Events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self , mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
        
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True
            #Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            #Create A New Fleet And Center The Ship
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

            #Reset The Game Settings
            self.settings.initialize_dynamic_settings()

    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        if len(self.bullets)<self.settings.bullets_allowed:
         new_bullet=Bullet(self)
         self.bullets.add(new_bullet)
    def _create_fleet(self):
        #Create The Fleet Of Aliens
        #Make An Alien
        #Spacing Between Alien Is One Alien Width And One Alien Height
        alien=Alien(self)
        alien_width, alien_height=alien.rect.size
        current_x, current_y=alien_width, alien_height
        while current_y<(self.settings.screen_height-3*alien_height):
         while current_x < (self.settings.screen_width-2 * alien_width):
            self._create_alien(current_x, current_y)
            current_x += 2*alien_width
         current_x=alien_width
         current_y+=1*alien_height           
    def _update_bullets(self):
        #Update Position Of Bullets And Get Rid Of Old Bullets
        #Update Bullet Position
        self.bullets.update()
        #Get Rid Of The Bullets That Have Disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        #Respond To Bullet Action Collision 
        #Remove Any Bullets And Aliens That Have Collided
        #Check For Any Bullets That Have Hit Aliens
        #If So Get Rid Of The Bullet And The ALien
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        #But If I Want To Create A Super Bullet That Keeps Killing All The Aliens That Apppear In Front Of It , Until It(Bullet)Disappears from the screen then check out the commented code below
        #collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,False,True)

        if collisions:
            for aliens in collisions.values():
             self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase Level
            self.stats.level +=1
            self.sb.prep_level()
            self.sb.prep_ships()

    def _create_alien(self,x_position,y_position):
        #Create An Alien And Place It In The Row
        new_alien=Alien(self)
        new_alien.x=x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien) 

    def _check_fleet_edges(self):
        #Respond Apptly If Any Alien Has Reached The Edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        #Drop The Entire Fleet And Change The Fleet's Direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        #Check If The Fleet Is AT THe Edge And Then Update The Positions 
        self._check_fleet_edges()
        self.aliens.update()
        #Looking For Alien Ship Collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Look For Alien Hitting The Bottom Of THe Screen
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        #Respond To The Ship Being Hit By The Alien
        if self.stats.ships_left > 0:
         #Decrement ships_left
         self.stats.ships_left -=1
         self.sb.prep_ships()
         #Get Rid Of Any Remaining Bullet And Aliens
         self.bullets.empty()
         self.aliens.empty()
         #Create A New Fleet And Center The Ship
         self._create_fleet()
         self.ship.center_ship()
         #pause
         sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)
         

    def _check_aliens_bottom(self):
        #Check If Any Aliens Have Reached The Bottom Of The Screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=self.settings.screen_height:
                #Treat It The Same As If The Ship Got Hit By An ALien
                self._ship_hit()
                break
    
    def _update_screen(self):
        #Update Images On The Screen And Flip To The New Screen
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #Draw The Score Information
        self.sb.show_score()

        #Draw The Play Button If THe Game Is Inactive
        if not self.game_active:
            self.play_button.draw_button()
        #Make The Most Recently Drawn Screen Visible
        pygame.display.flip()   



if __name__=='__main__':
    #Make A game Instance and Run The Game
     ai=AlienInvasion()
     ai.run_game() 