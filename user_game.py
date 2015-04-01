from engine import *
from kivy.properties import NumericProperty, BooleanProperty, ListProperty


class UserGame():
    def __init__(self, ):
        self.game_started = False

    score1 = NumericProperty(0)
    score2 = NumericProperty(0)
        
    def game_start(self, user_team, team2, league, tourn=False):
        self.user = user_team
        self.opp = team2
        self.league = league
        self.tourn = tourn
        
        
        self.user.games_played += 1
        self.opp.games_played += 1
        self.user.player_g_stat_reset(league)
        self.opp.player_g_stat_reset(league)
        
        self.turns_top = 12
        self.end_reg = False
        self.overall_turn = 1
        self.foul_out = 6
        if league.college == True:
            self.turns_top = 10
            self.foul_out = 5
        self.half = 1
        self.score1 = 0
        self.score2 = 0
        self.time_out1 = 5
        self.time_out2 = 5
        self.run1, self.run2 = 1.0, 1.0
        self.called_time = False
        self.user_lineup = []
        
        for i in range(10):
            self.user.roster[i].tiredness, self.opp.roster[i].tiredness = 0,0
            self.user.roster[i].set_exhaust()
            self.opp.roster[i].set_exhaust()
    
    
        for player in self.user.roster:
            player.rest(True)
        for player in self.opp.roster:
            player.rest(True)
    
        self.current_turn = 0
        #possessions
        self.team1_carry = [0]
        self.team2_carry = [0]
        self.game_started = True
        self.game_fin = False
        
    def halftime(self):
        for player in self.user.roster:
            player.rest(True)
        for player in self.opp.roster:
            player.rest(True)
    
        self.current_turn = 1
        #possessions
        self.team1_carry = [0]
        self.team2_carry = [0]
        
        self.half += 1
        if self.half >= 3:
            self.game_started = False
            self.game_fin = True
            
    
    def play_turn(self):
        self.current_turn += 1
        self.overall_turn += 1
        if self.called_time == True and self.time_out1 > 0:
            self.time_out1 -= 1
            self.run1, self.run2 = 1.0, 1.0
            for i in range(len(self.user.roster)):
                self.user.roster[i].rest()
                self.opp.roster[i].rest()
        elif self.league.coaches[self.opp.head_coach].call_time(self.run1, self.overall_turn, self.time_out2, self.opp.roster) == True and self.time_out2 > 0:
            self.time_out2 -= 1
            self.run1, self.run2 = 1.0, 1.0
            for i in range(len(self.user.roster)):
                self.user.roster[i].rest()
                self.opp.roster[i].rest()
        lineup2 = self.league.coaches[self.opp.head_coach].set_lineup(self.opp.roster, self.score2-self.score1, self.overall_turn, self.foul_out, self.turns_top*2)
        change = Game_turn(self.user_lineup, lineup2, self.team1_carry, self.team2_carry, self.foul_out, self.run1, self.run2)
        self.run1 += change
        if self.run1 > 1.9:
            self.run1 = 1.9
        elif self.run1 < 0.1:
            self.run1 = 0.1
        self.run2 = 2.0 - self.run1
        
        for player in self.user.roster:
            played = False
            for i in self.user_lineup:
                if player.player_id == i[0].player_id:
                    played = True
            if played == False:
                player.rest()
        for player in self.opp.roster:
            played = False
            for i in lineup2:
                if player.player_id == i[0].player_id:
                    played = True
            if played == False:
                player.rest()
        self.score1, self.score2 = update_points(self.user), update_points(self.opp)
        
        if self.current_turn >= self.turns_top:
            self.halftime()
            
            
    def debug_user(self):
        temp_lineup = self.league.coaches[self.user.head_coach].set_lineup(self.user.roster, self.score1-self.score2, self.overall_turn, self.foul_out, self.turns_top*2)
        '''final_lineup = []
        for i in temp_lineup:
            final_lineup.append(i[0])'''
        self.user_lineup = temp_lineup
            
        