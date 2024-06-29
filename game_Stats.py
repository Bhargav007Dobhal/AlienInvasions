class GameStats:
    #Track Statistics For Alien Invasion
    def __init__(self,ai_game):
        #Initialize Statistics
        self.settings=ai_game.settings
        self.reset_stats()
        #High Score
        self.high_score=0
    def reset_stats(self):
        #Initialize Statistics That Can Changfe During The Game
        self.ships_left=self.settings.ship_limit
        self.score=0
        self.level=1

        