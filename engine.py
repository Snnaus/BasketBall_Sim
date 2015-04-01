import random, math, operator


class Player():
    
    def __init__(self, world_id):
    
        self.player_id = world_id
        self.age = random.randint(17,19)
        self.location = random.randint(1,50)
        self.recruited = False
        
        self.attr = {}
        self.attr['pos_create'] = random.randint(3,10)
        self.attr['inside_rate'] = random.randint(3,10)
        self.attr['outside_rate'] = random.randint(3,10)
        self.attr['three_rate'] = random.randint(3,10)
        self.attr['inside_conversion'] = random.randint(3,10)
        self.attr['outside_conversion'] = random.randint(3,10)
        self.attr['three_conversion'] = random.randint(3,10)
        self.attr['assist_rate'] = random.randint(3,10)
        self.attr['poss_taken'] = random.randint(3,10)
        self.attr['inside_conv_mod'] = random.randint(3,10)
        self.attr['outside_conv_mod'] = random.randint(3,10)
        self.attr['block_rate'] = random.randint(3,10)
        self.attr['steal_rate'] = random.randint(3,10)
        self.attr['rebound'] = random.randint(3,10)
        self.attr['chemistry'] = random.randint(3,10)
        self.attr['fouling'] = random.randint(3,10)
        self.attr['free_throw'] = random.randint(3,10)
        self.attr['draw_foul'] = random.randint(3,10)
        self.attr['ball_security'] = random.randint(3,10)
        self.attr['stamina'] = random.randint(3,10)
        self.attr['work_rate'] = random.randint(3,10)
        self.attr['regen_rate'] = random.randint(3,10)
        self.attr['toughness'] = random.randint(3,10)
        
        self.g_stats = {
            'PTS': 0,
            'FGM': 0,
            'FGA': 0,
            '3PM': 0,
            '3PA': 0,
            'FTM': 0,
            'FTA': 0,
            'ORB': 0,
            'DRB': 0,
            'TRB': 0,
            'AST': 0,
            'STL': 0,
            'BLK': 0,
            'TOV': 0,
            'PF': 0,
            'GT': 0,
            'FG%': 0,
            '3P%': 0,
            'FT%': 0
        }
        
        self.season_totals = {}
        for key, value in self.g_stats.iteritems():
            self.season_totals[key] = 0
    
        #position scores
        self.posi = {
            'PG': 0,
            'SG': 0,
            'SF': 0,
            'PF': 0,
            'C': 0,
            'DE': 0,
            'OF': 0
            }
            
        self.pos_update()
        
        self.preferences = {
                'close_to_home': bool(random.getrandbits(1)),
                'school_prestige': bool(random.getrandbits(1)),
                'coach_prestige': bool(random.getrandbits(1)),
                'pro_prospects': bool(random.getrandbits(1)),
                'anti_charisma': random.triangular(0.1, 0.5)}
         
        #this is the attribute that affects the magnitude of the preference for the pros; lower the number the higher the dreams
        self.pro_dreams = random.randint(1,100)
        
        self.short_list = []
        
        #these attributes are for the progression of the player
        self.total_skill = 0
        for key,value in self.attr.iteritems():
            self.total_skill += value
        self.total_potential = random.randint(1,(660-self.total_skill))
        self.skill_change = random.randint(1,50)
        
        #Player Stats
        self.season_game_log = {}
        self.career_season_log = {}
        
                    
    
        self.tiredness = 0
        self.personality = 0
        self.exhaustion = 0
    
    
    #this method is used to update the players position scores
    def pos_update(self):
        for key, value in self.attr.iteritems():
            if key == 'pos_create' or key == 'assist_rate' or key == 'steal_rate' or key == 'outside_conv_mod' or key == 'ball_security':
                self.posi['PG'] += value
            if key == 'pos_create' or key == 'outside_conversion' or key == 'steal_rate' or key == 'outside_conv_mod' or key == 'three_conversion':
                self.posi['SG'] += value
            if key == 'inside_conversion' or key == 'draw_foul' or key == 'rebound' or key == 'outside_conv_mod' or key == 'inside_conv_mod':
                self.posi['SF'] += value
            if key == 'rebound' or key == 'inside_conversion' or key == 'block_rate' or key == 'outside_conversion' or key == 'inside_conv_mod':
                self.posi['PF'] += value
            if key == 'poss_taken' or key == 'inside_conversion' or key == 'block_rate' or key == 'rebound' or key == 'inside_conv_mod':
                self.posi['C'] += value
            if key == 'poss_taken' or key == 'outside_conv_mod' or key == 'block_rate' or key == 'steal_rate' or key == 'inside_conv_mod' or key == 'rebound' or key == 'toughness':
                self.posi['DE'] += value
            if key == 'pos_create' or key == 'outside_conversion' or key == 'inside_conversion' or key == 'outside_rate' or key == 'three_conversion' or key == 'assist_rate' or key == 'draw_foul':
                self.posi['OF'] += value
    
    def tired_set(self, grit=None):
        #grit is the value of the opponents toughness that affects the stamina of the teams players
        new_tired =  random.randint(1,30-self.attr['work_rate'])
        self.tiredness += new_tired #* (1 - (grit/100))
        self.set_exhaust()
    
    def rest(self, half_time=False):
        rest = 10 #+ random.randint(1,self.attr['regen_rate'])
        if half_time == True:
            rest = 30
        self.tiredness -= rest
        if self.tiredness < 0:
            self.tiredness = 0
        self.set_exhaust()
        
    def set_exhaust(self):
        #print self.tiredness
        if self.tiredness > self.attr['stamina']*10:
            self.exhaustion = 0.75
        elif self.tiredness > float(self.attr['stamina']*10)*0.75:
            self.exhaustion = 0.9
        else:    
            self.exhaustion = 1.0 #- (self.tiredness / self.attr['stamina'])
        
    def post_game_update(self, game_id):
        _temp_dict = {}
        bans = ['FT%','FG%','3P%']
        for key, value in self.g_stats.iteritems():
            _temp_dict[key] = value
            if key not in bans:    
                self.season_totals[key] += value
            self.g_stats[key] = 0
        self.update_percents(self.season_totals)
        self.season_game_log[game_id] = _temp_dict
        
    def post_season_update(self, year):
        _temp_dict = {}
        for key, value in self.season_totals.iteritems():
            _temp_dict[key] = value
            self.season_totals[key] = 0
        self.career_season_log[year] = _temp_dict    
            
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Decision Making

    def choose_school(self, league):
        shortlist_values = []
        for team in self.short_list:
            value = 0
            if self.preferences['close_to_home'] == True:
                distance = abs(team.location-self.location)
                value += float((50-distance)/50)
            if self.preferences['school_prestige'] == True:
                value += team.total_win_per
            if self.preferences['coach_prestige'] == True:
                value += league.coaches[team.head_coach].total_win_per
            if self.preferences['pro_prospects'] == True:
                value += float(league.coaches[team.head_coach].draft_value/self.pro_dreams)
            
            char_coef = league.coaches[team.head_coach].coaching_skills['CHA'] - self.preferences['anti_charisma']
            value = value * char_coef
            shortlist_values.append(value)
            
        choice = [0,-50]
        for x in range(len(self.short_list)):
            if shortlist_values[x] > choice[1]:
                choice[0], choice[1] = self.short_list[x], shortlist_values[x]
        
        return choice[0]
    
    def skill_progression(self):
        decay = 0
        if self.age > 41:
            decay = 50
        elif self.age > 35:
            decay = 20
        elif self.age > 28:
            decay = 10
        
        change_in_skill = self.skill_change
        if self.total_potential < self.skill_change:
            change_in_skill = self.total_potential
        
        for x in range(abs(change_in_skill - decay)):
            change = 1
            if decay > self.skill_change:
                change = -1
            while True:
                key = random.choice(self.attr.keys())
                if self.attr[key] < 20:
                    self.attr[key] += change
                    break
        
        self.total_potential -= self.skill_change
        if selt.total_potential < 0:
            self.total_potential = 0
    
    def g_stat_reset(self):
        for x in self.g_stats:
            self.g_stats[x] = 0
    
    def update_percents(self, stats):
        if stats['FGA'] > 0:
            stats['FG%'] = round(float(stats['FGM'])/float(stats['FGA']), 3)
        else:
            stats['FG%'] = 0.00
            
        if stats['3PA'] > 0:
            stats['3P%'] = round(float(stats['3PM'])/float(stats['3PA']), 3)
        else:
            stats['3P%'] = 0.00
            
        if stats['FTA'] > 0:
            stats['FT%'] = round(float(stats['FTM'])/float(stats['FTA']), 3)
        else:
            stats['FT%'] = 0.00
            
class Coach():
    '''#this is the dictionary for the preferences of the coach when it comes to the players play style
    preferences = {}
    total_pref = 0
    
    hired = False
    employer = 0
    
    #           [salary, years]
    contract = [0,0]'''
    
    
    def __init__(self, world_c_id):
        
        #this is the dictionary for the preferences of the coach when it comes to the players play style
        self.preferences = {}
        self.total_pref = 0
    
        self.hired = False
        self.employer = 0
    
        #           [salary, years]
        self.contract = [0,0]
        
        #this is the identification number for the coaches
        self.coach_id = world_c_id
    
        #this holds the stat modifier that the coach has; they range from 1 to 20;
        #the skill divided by 4, then divided again by 10 is added to 0.7 to create
        #the coefficient that this coach applies to the teams skills in game.
        #it has an effective range of 0.7-1.3
        self.coaching_skills = {
                'OFF': 0,
                'DEF': 0,
                'PHY': 0,
                'CHA': 0
                }
    
        for x in range(5):
            #                   PG, SG, SF, PF, C
            self.preferences[x] = [0,0,0,0,0]
            #this is setting the initial preferences of the coaches; assigning 1,2,3 randomly between the 5 play style signals
            intial_pref = [random.randint(0,4), random.randint(0,4), random.randint(0,4)]
            count = 0
            for i in intial_pref:
                count += 1
                self.preferences[x][i] += count
            self.total_pref += 6
        self.salary_dist = random.triangular(1.0, 2.1)
        for key,value in self.coaching_skills.iteritems():
            value = random.randint(1,20)
        #this is preference for game situations
        self.lower_limit = random.randint(4,20)
        self.focal_point = random.randint(1,5)
        
                            #[wins, games played]
        self.career_games = [0,0]
        self.previous_season = [0,0]
        self.recent_history = [-1,-1,-1] #this takes the wins from the past three seasons for the coaches recent history
        self.current_job_win_per = [] #this is for the log of season wins with the coaches current team
        
        #this is the metric for how many players and where they went in the pro draft: 1st overall = 7, 2-5 = 5, Lottery = 3, 1st round = 2, 2nd round = 1
        self.draft_value = 0
        
        #this is for the coaching trees; to see which coaches have influenced each other
        self.coach_mentors = []
        self.coach_children = []
        
        #this is to store the clubs that have offered the coach a job; much like the schools recruiting players
        #the items will be lists that have [team_id, money offered]
        self.job_offers = []
        
        #this is for the extension logic
        self.ext_threshold = random.randint(1,10)
        
        #these are for the board members to evaluate the coach for a contract
        self.total_win_per = 0.00
        self.recent_win_per = 0.00
        self.current_w_per = 0.00
        self.old_w_per = 0.00
        #this is a discount rate based on how many players the coach had a hand in signing/recruiting; for pros it is previously used money/cap; in college it is previously used scholarships/total scholarships
        self.eval_discount_rate = 0.00
        #this is how long the coach has been at the same club; this should affect his decision to chose an extension over FA
        self.inertia = 0
           
    def off_def_coef(self, point_diff, time, full_time):
        low = (self.lower_limit/2)*-1
        focal = self.focal_point - 3
        poss_diff = math.floor(point_diff/2.2)
        time_co = float(time)/(float(full_time)*.75)
        
        off_co = (((poss_diff-focal)/low)*2.0)*time_co
        if off_co < 0:
            off_co = 0 #+ off_co
        elif off_co > 2:
            off_co = 2
            
        def_co = 2 - off_co
        
        return [off_co, def_co]
        
    def set_lineup(self, team, point_diff, time, foul_out, full_time):
        coefs = self.off_def_coef(point_diff, time, full_time)
        lineup = [0,0,0,0,0]
        for player in team:
            foul = self.foul_coef(player.g_stats['PF'], time, foul_out)
            #print foul
            value = ((player.posi['OF']*player.exhaustion)*foul)*coefs[0]
            value += ((player.posi['DE']*player.exhaustion)*foul)*coefs[1]
            #print value
            new = False
            for x in range(len(lineup)):
                if new == False and lineup[x] == 0:
                    lineup[x] = [player, value]
                    break
                elif new == False and lineup[x] != 0 and lineup[x][1] < value:
                    new = lineup[x]
                    lineup[x] = [player, value]
                if new != False:
                    if lineup[x] == 0 or lineup[x][1] < new[1]:
                        __temp = lineup[x]
                        lineup[x] = new
                        if __temp == 0:
                            break
                        else:
                            new = __temp
        return lineup
    
    def foul_coef(self, fouls, current_time, foul_out):
        #print foul_out
        ought_fouls = float(current_time) / 4.0
        coef = float(fouls) / ought_fouls
        if current_time == 1 or fouls == 0 or fouls < foul_out:
            coef = 1
        elif fouls >= foul_out:
            #print 'dude'
            coef = 0
        #print coef
        return coef
    
    '''#these are for the board members to evaluate the coach for a contract
    total_win_per = 0.00
    recent_win_per = 0.00
    current_w_per = 0.00
    old_w_per = 0.00
    #this is a discount rate based on how many players the coach had a hand in signing/recruiting; for pros it is previously used money/cap; in college it is previously used scholarships/total scholarships
    eval_discount_rate = 0.00
    #this is how long the coach has been at the same club. this should affect his decision to chose an extension over FA
    inertia = 0'''
    
    def call_time(self, opp_run, time, time_outs, team):
        #This is the parent function of a coach calling a timeout; the logic here will decide if a timeout will be called because of an opponents 'run'
        call = False
        ought_time = 5.0 - (float(time)/4.0)
        #print 'ought', ought_time
        time_should = (float(time_outs)/ought_time)
        check = opp_run * time_should
        #print check
        if check > 1 or check == 0:
            call = True
        if call == False:
            call = self.rest_time_out(time_should, team)
        return call
    
    def rest_time_out(self, time_should, team):
        rest_coef = 0.00
        for player in team:
            rest_coef += player.exhaustion
        rest_coef = rest_coef/float(len(team))
        if rest_coef * time_should > 0.85:
            return True
        else:
            return False
        
    
    def update_per(self):
        total_win_per = float(self.career_games[0]/career_games[1])
        recent_history, years = 0, 0
        for year in self.recent_history:
            if year >= 0:
                years += 1
                recent_history += year
                
        self.recent_win_per = float(recent_history/(year*33))
        self.current_w_per = float(self.previous_season[0]/self.previous_season[1])
    
    def recruit_eval(self, player, current_pref):
        value = 0
        count = 0
        pos = ['PG', 'SG', 'SF', 'PF', 'C']
        for i in current_pref:
            value += player.posi[pos[count]] * i
            count += 1
        return value
    
    def pos_fit(self, player, taken_array):
        count = 0
        compare = -50
        spot = -1
        for i in self.preferences:
            if taken_array[count] == False:
                x = self.recruit_eval(player, self.preferences[i])
                if x > compare:
                    compare = x
                    spot = count
            count += 1
        taken_array[spot] == True
    
    def update_current_pref(self, taken_array):
        current_pref = [0,0,0,0,0]
        count = 0
        for i in self.preferences:
            if taken_array[count] == False:
                count2 = 0
                for x in self.preferences[i]:
                    current_pref[count2] += x
                    count2 += 1
            count += 1
        return current_pref
        
    def find_best(self, players, pref, temp_roster, looked_at):
        change = False
        if type(players) is list:
            for player in players:
                if player != 0 and player.recruited == False:
                    pl_value = self.recruit_eval(player, pref)
                    if pl_value > looked_at[1] and player.player_id not in temp_roster:
                        looked_at[0], looked_at[1] = player, pl_value
                        change = True
        else:
            for id,player in players.iteritems():
                if player != 0 and player.recruited == False:
                    pl_value = self.recruit_eval(player, pref)
                    if pl_value > looked_at[1] and player.player_id not in temp_roster:
                        looked_at[0], looked_at[1] = player, pl_value
                        change = True
        return change
    
    #this method can also be used in free agency for pros
    def recruiting(self, club, recruits):
        open_spots = club.open_spots()
        targets = None
        if open_spots > 0:
            targets = []
            taken_array = [False, False, False, False, False]
            _temp_roster = []
            count = 0
            while True:
                count += 1
                looked_at_player = [0,-50]
                curr_preff = self.update_current_pref(taken_array)
                foo = self.find_best(club.roster, curr_preff, _temp_roster, looked_at_player)
                change = self.find_best(recruits, curr_preff, _temp_roster, looked_at_player)
                if change == True:
                    open_spots -= 1
                    targets.append(looked_at_player[0])
                _temp_roster.append(looked_at_player[0])
                if open_spots < 1:
                    break
                if count < 5:
                    self.pos_fit(looked_at_player[0], taken_array)
                elif count == 5:
                    taken_array = [False, False, False, False, False]
            for player in targets:
                player.short_list.append(club)
                       
    def coaching_progression(self, head_coach):
        for x in range(len(self.preferences)):
            for y in range(len(self.preferences[x])):
                new_pref = (self.preferences[x][y] + head_coach.preferences[x][y])/2
                self.preferences[x][y] = new_pref
                
        for key in self.coaching_skills:
            if self.coaching_skills[key] < head_coach.coaching_skills[key]:
                new_skill = (self.coaching_skills[key]+head_coach.coaching_skills[key])/2
                self.coaching_skills[key] = new_skill
                
        self.coach_mentors.append(head_coach.coach_id)
        head_coach.coach_children.append(self.coach_id)
    
    def coach_job_choice(self, average_salary, league, asst=False):
        choice = [0, None , 0]
        for x in self.job_offers:
            value = 0.0
            value += float(league.teams[x[0]].wins/league.teams[x[0]].games_played)
            value += float(x[1]/average_salary)
            if value > choice[1] or choice[1] == None:
                choice[0], choice[1], choice[2] = x[0], value, x[1]
                
        if asst == False:
            #print choice[0]
            league.teams[choice[0]].head_coach = self.coach_id
            #print 'dude', self.coach_id
            league.teams[choice[0]].coach_salary = choice[2]
            league.teams[choice[0]].fire_extend_check(league, True)
            self.contract[0], self.contract[1] = choice[2], league.teams[choice[0]].contract_length
            league.teams[choice[0]].ast_salary = (choice[2]/4)
            self.employer = choice[0]
            self.hired = True
        else:
            league.teams[choice[0]].ast_coach = self.coach_id
            self.employer = choice[0]
            self.hired = True
                  
    def choose_ast(self, league):
        choice = [0, -100.0]
        for id, coach in league.coaches.iteritems():
            value = 0.0
            if coach.hired == False:
                diff = {}
                for x, skill in self.coaching_skills.iteritems():
                    if x != "CHA":
                        diff[x] = skill
                    
                for x, skill in coach.coaching_skills.iteritems():
                    if x != "CHA":
                        diff[x] -= skill
                
                low = [0,50.0]
                for x, num in diff.iteritems():
                    if num < low[1]:
                        low[0], low[1] = x, num
                
                value += low[1]
                for x, num in diff.iteritems():
                    if x != low[0] and num < 0:
                        value += num
                        
                value = value * -1.0
                if value > choice[1]:
                    choice[0], choice[1] = id, value
                    
        league.coaches[choice[0]].job_offers.append([self.employer, league.teams[self.employer].ast_salary])

    def ext_choice(self, average_salary, money):
        '''this function should decide if the coach is going to stay; if he does than it will change the necessary things within the club object'''
        if money/average_salary + self.inertia > self.ext_threshold:
            return True
        else:
            return False
    
class Board():
    #this class is for the board members of the team; they are the ones who makes decisions around the coach
    #and the financials of the club
    def __init__(self):
        #here the board member will have a money value attached to the skill level of a coach
        self.coach_value = {
            'OFF': 0,
            'DEF': 0,
            'PHY': 0,
            'CHA': 0,
            'Recent_history': 0,
            'Total_history': 0
            }
        total_money = 0
        for x in self.coach_value:
            if x == 'OFF' or x == 'DEF' or x == 'PHY' or x == 'CHA':
                new_money = random.triangular(0.0001,0.1666)
                total_money += new_money
                self.coach_value[x] = new_money
        hist_money = 1.0 - total_money
        self.coach_value['Recent_history'] = random.triangular(0.0001, hist_money)
        self.coach_value['Total_history'] = hist_money - self.coach_value['Recent_history']
        
        self.con_length = random.triangular(0.15,0.5)
        self.fire_limit = random.triangular(0.2,0.4)
        
        self.aversion = random.randint(0,50)

    def B_coach_value(self, coach, money):
        money_bid = 0
        for key,value in coach.coaching_skills.iteritems():
            money_bid += ((value - 0.7)/0.6) * (self.coach_value[key]*money)
        money_bid += coach.recent_win_per * (self.coach_value['Recent_history']*money)
        money_bid += coach.total_win_per * (self.coach_value['Total_history']*money)
        return money_bid
        
    def fire_ext(self, coach, ext=True):
        if coach != 0:
            standard = coach.old_w_per
        else:
            standard = 0.0
        if standard > 0.4:
            standard = 0.4
        eval = (coach.current_w_per - standard) * (1.0-coach.eval_discount_rate)
        if ext == False:
            eval = coach.total_win_per/2.0
        if eval < self.fire_limit * -1 and ext == True:
            return "Fire"
        else:
            x = int(eval/self.con_length)
            if x <= 0:
                x = 0
            return x

class Club():

    def __init__(self, club_id):
        #this class is for the object that is the team; all the other objects are stored in this object
        self.head_coach = 0
        self.roster = []
        self.ast_coach = 0
        #there are 3 board members
        self.board = []
        self.money = 100000
        self.coach_salary = 0
        self.contract_length = 0
        self.ast_salary = 0
    
        #this is an identification # for the club.
        self.club_id = club_id
        self.conf_id = None
        self.last_conference = None
        
        #The location attribute is tells where the club is located; it is 0-49 each vaguely describing a 
        #state in the united states that it is in; 0 is representative of international (This would be for player only)
        self.location = 0
        
        #these attributes are for the previous season, for rank ordering purposes
        self.wins = 50
        self.games_played = 100
        self.seas_point_diff = 0
        self.seas_point_scored = 0
        self.seas_point_allowed = 0
        self.current_season_game_log = []
        self.pse_elo = 0.00
        self.pse_elo2 = 0.00
        self.opp_win_per = 0.00
        
        self.total_wins = 50
        self.total_win_per = 0.00
        self.total_games_played = 100
        
        self.conf_offers = []
        
        #this is temporary for testing; board members will be created and stored outside in the league class 2/23/2015
        for x in range(3):
            self.board.append(Board())
            
        for x in range(12):
             self.roster.append(0)
        
    def pick_conference(self, league):
        choice = [0, -50]
        for i in self.conf_offers:
            if league.conferences[i].prestige > choice[1]:
                choice[0], choice[1] = i, league.conferences[i].prestige
                if i == self.last_conference:
                    break
        #print choice
        self.last_conference, self.conf_id = choice[0], choice[0]
        league.conferences[choice[0]].teams.append(self)
        
    def update_win_per(self):
        self.total_win_per = float(self.total_wins/self.total_games_played)
    
    def set_coach_old_per(self):
        self.head_coach.old_w_per = float(self.wins/self.games_played)
    
    def player_g_stat_reset(self, league):
        for x in self.roster:
            x.g_stat_reset()
    
    def open_spots(self):
        spots = 0
        for player in self.roster:
            if player == 0:
                spots += 1
        return spots
    
    def coach_value(self, coach):
        value = 0
        for BM in self.board:
            #print BM, self.money, coach
            value += BM.B_coach_value(coach, self.money)
        return value
    
    def offer_coach(self, league):
        choice = [0, None]
        for key, coach in league.coaches.iteritems():
            if coach.hired == False:
                value = self.coach_value(coach)
                if value > choice[1] or choice[1] == None:
                    choice[0], choice[1] = key, value
        #print choice
        league.coaches[choice[0]].job_offers.append([self.club_id, choice[1]])
    
    def fire_extend_check(self, league, new=False, fire_only=False):
        fire_votes = 0
        length = 0.0
        for member in self.board:
            years = member.fire_ext(league.coaches[self.head_coach])
            if years == 'fire':
                fire_votes += 1
            else:
                length += years
        if fire_votes > 1 and new == False:
            team.head_coach.hired = False
            team.head_coach = 0
        elif fire_only == False:
            self.contract_length = round(length)
            if self.contract_length < 1:
                self.contract_length = 1
            #print self.contract_length
            
    def update_elo(self, pd, opp_elo, second=False):
        '''if self.pse_elo == 0:
            self.pse_elo = 1000'''
        delta = self.pse_elo - opp_elo
        if delta == 0:
            delta = 1.00
        '''elif delta < 0 and delta > -1:
            delta = -1.00'''
        denom = abs(pd)+5.0*abs(delta)
        if denom == 0:
            add = 0.00
        else:
            add = pd/denom
        '''if pd < 0 and delta > 0:
            add = pd/denom'''
        '''if denom > pd and pd < 0:
            add = pd/(denom*-1)'''
        '''if pd < 0:
            add = pd/denom
            #add = 0
        else:
            add = pd/denom'''
        '''elif denom > pd:
            add = pd/(denom*-1)'''
        
        if second == False:    
            self.pse_elo += add
        else:
            self.pse_elo2 += add
            
        return (add, delta)
    
    def update_opp_win_per(self, league):
        #This is for the possible addition of an RPI system.
        count = 0.00
        total = 0.00
        for game in self.current_season_game_log:
            count += 1.00
            percent = float(league.teams[game[2]].wins)/float(league.teams[game[2]].games_played)
            total += percent
        
        self.opp_win_per = total/count
        
    def find_rpi(self, league):
        oowp = 0.00
        count = 0
        for game in self.current_season_game_log:
            count += 1
            oowp += league.teams[game[2]].opp_win_per
        oowp = oowp/count
        
        rpi = (0.25*(float(self.wins)/float(self.games_played)))+(0.5*self.opp_win_per)+(0.25*oowp)
        
        self.rpi = rpi
        
    def find_final_pse(self, league):
        for game in self.current_season_game_log:
            self.update_elo(game[0]-game[1], league.teams[game[2]].pse_elo, True)
            
class Conference():
    #this is the id number to identify the conference
    '''This needs to store the teams as objects, not ids. There will be a hell of a lot of refactoring if the ids are stored. 2/25/2015'''
    '''conf_id = 0
    season_wins = 0
    season_coef = 0.0
    teams = []
    rank_order = []
    team_id = 0
    prestige = 0 #this is a measure of the total value of all the teams in the conference. a make-shift way of measuring a conference's prestige.
    for x in range(12):
        rank_order.append(None)
        
    #this is the location of the "conference office"; this plays into the decision of which teams will be in the conference;
    #the effective location is the average between the office and the ten team locations
    office = 0
    effective_location = 0'''

    def __init__(self, id):
        self.office = random.randint(1,50)
        self.conf_id = id
        
        
        self.season_wins = 0
        self.season_coef = 0.0
        self.teams = []
        self.rank_order = []
        self.team_id = 0
        self.prestige = 0 #this is a measure of the total value of all the teams in the conference. a make-shift way of measuring a conference's prestige.
        for x in range(12):
            self.rank_order.append(None)
        
        #this is the location of the "conference office"; this plays into the decision of which teams will be in the conference;
        #the effective location is the average between the office and the ten team locations
        self.effective_location = 0
    
    def offer_schools(self, league):
        choice = [0, -50]
        for id, team in league.teams.iteritems():
            #print team.conf_id, len(self.teams)
            if team.conf_id == None:
                value = team.money * abs(team.location-self.office)
                #print 'dude'
                if choice[0] == 0 or value > choice[1]:
                    choice[0], choice[1] = team, value
        
        #print choice
        if choice[0] != 0:
            choice[0].conf_offers.append(self.conf_id)
    
    def update_wins(self):
        total = 0
        for team in self.teams:
            total += team.wins
        self.season_wins = total
    
    def update_seas_coef(self, games_played):
        self.update_wins()
        
        self.season_coef = float(self.season_wins/games_played)
    
    def rank_teams(self):
        for team in self.teams:
            current_team = team
            pos = 0
            for rank in self.rank_order:
                place = False
                if rank == None or current_team.wins > rank.wins:
                    place = True
                elif current_team.wins == rank.wins and current_team.seas_point_diff > rank.seas_point_diff:
                    place = True
                elif current_team.wins == rank.wins and current_team.seas_point_diff == rank.seas_point_diff and current_team.seas_point_scored > rank.seas_point_scored:
                    place = True
                
                if place == True:
                    _temp = rank
                    self.rank_order[pos] = current_team
                    current_team = _temp
                pos += 1
                
    def conf_game_sched(self):
        '''team_ids need to in the format so that they are greater that 11; otherwise this scheduling hack will not work'''
        schedule = [[[0,1],[2,3],[4,5],[6,7],[8,9],[10,11]],
                    [[0,2],[1,5],[3,4],[6,8],[7,11],[9,10]],
                    [[0,3],[1,4],[2,5],[6,9],[7,10],[8,11]],
                    [[0,4],[1,2],[3,5],[6,10],[7,8],[9,11]],
                    [[0,5],[1,3],[2,4],[6,11],[7,9],[8,10]]]
            
        teams = []
        teams2 = []
        
        for x in range(6):
            teams.append(self.rank_order[x].club_id)
            teams2.append(self.rank_order[x+6].club_id)
            
        for i in range(6):
            for day in schedule:
                for game in day:
                    team_count = 0
                    while True:
                        if game[team_count] == i:
                            game[team_count] = teams[i]
                        elif game[team_count] == i+6:
                            game[team_count] = teams2[i]
                        team_count += 1
                        if team_count > 1:
                            break
                            
        for i in range(6):
            week = []
            for y in range(6):
                week.append([teams[y], teams2[y]])
            schedule.append(week)
            
            if i < 6:
                new_teams2 = []
                for z in range(6):
                    if z == 0:
                        new_teams2.append(teams2[5])
                    else:
                        new_teams2.append(teams2[z-1])
                teams2 = new_teams2
        
        repeat = len(schedule)      
        for x in range(repeat):
            schedule.append(schedule[x])
            
        return schedule
        
    def update_location(self):
        total = self.office
        points = 1
        for x in self.teams:
            if x != None:
                total += x
                points += 1
        self.effective_location = total/points

class League():
    #this class is the class that holds all of the conferences teams, coaches, and players;
    #for now this also serves as the game logic portion of the game loop (this is probably going to change because there will be multiple leagues--namely, Pro and International play)
    '''teams = {}
    conferences = {}
    coaches = {}
    players = {}
    college = True
    recruits = {}
    
    average_salary = 500
    
    world_coach_id = 1
    world_id = 1
    club_id = 101
    conf_id = 1101
    
    schedule_of_games = []
    games_played = 1
    conference_rank = []'''
    game_count = 1
    
    def __init__(self, debug=False):
        self.teams = {}
        self.conferences = {}
        self.coaches = {}
        self.players = {}
        self.college = True
        self.recruits = {}
    
        self.average_salary = 500
        self.season_num = 2000
    
        self.world_coach_id = 1
        self.world_id = 1
        self.club_id = 101
        self.conf_id = 1101
    
        self.schedule_of_games = []
        self.games_played = 1
        self.conference_rank = []
    
        for x in range(144):
            self.teams[self.club_id] = Club(self.club_id)
            self.club_id += 1
            
        self.coach_creation()
        self.hiring_loop(self.average_salary)
        self.recruit_loop()
        
        self.confere_creation()
        self.conference_team()
        
        self.set_schedule()
        
        if debug == True:
            self.play_season()
    
    def play_season(self):
        self.season_num += 1
        for id, team in self.teams.iteritems():
            team.wins, team.total_wins, team.games_played = 0, 0, 0
            team.rank_pts, team.rank = 0, 0
            team.pse_elo, team.pse_elo2 = 1000, 1000
        for week in self.schedule_of_games:
                self.player_week(week)
                for id, team in self.teams.iteritems():
                    team.update_opp_win_per(self)
        for i,player in self.players.iteritems():
            player.post_season_update(self.season_num)
        
        for i,team in self.teams.iteritems():
            team.find_rpi(self)
            team.find_final_pse(self)
            
        self.rank_teams()
        self.tournament()
    
    def update_rank(self):
    
        for id,conf in self.conferences.iteritems():
            conf.rank_teams()
            conf.update_seas_coef(self.games_played)
        
        self.conference_rank = []
        for x in self.conferences:
            self.conference_rank.append((self.conferences[x], self.conferences[x].season_coef))
        
        sorted(self.conference_rank, key=operator.itemgetter(1), reverse=True)
    
    def set_schedule(self):
        self.schedule_of_games = []
        self.update_rank()
        self.set_out_conf()
        
        first = True
        cong_count = 0
        last_week = []
        for id,conf in self.conferences.iteritems():
            #cong_count += 1
            _temp_conf = conf.conf_game_sched()
            #print _temp_conf
            #print len(self.schedule_of_games)
            #print len(_temp_conf)
            
            
            
            
            new_week = []
            if first == True:
                for week in _temp_conf:
                    self.schedule_of_games.append(week)
                    #cong_count += len(week)
                first = False
            else:
                #cong_count += 1
                #print len(_temp_conf)
                #print _temp_conf
                count = 10
                count2 = 0
                for week2 in _temp_conf:
                    cong_count += 1
                    #print cong_count, '-----------------------'
                    count += 1
                    #print len(week2)
                    #count2 = 0
                    for game in week2:
                        #print game
                        #cong_count += 1
                        #self.schedule_of_games[count].append(game)
                        new_week.append(game)
                        if game not in last_week:
                            self.schedule_of_games[count].append(game)
                        last_week.append(game)

    def set_out_conf(self):
        conf = []
        conf2 = []
        
        for x in range(6):
            conf.append(self.conference_rank[x][0].conf_id)
            conf2.append(self.conference_rank[x+6][0].conf_id)
            
        scheduled = [[[0,1],[2,3],[4,5],[6,7],[8,9],[10,11]],
                    [[0,2],[1,5],[3,4],[6,8],[7,11],[9,10]],
                    [[0,3],[1,4],[2,5],[6,9],[7,10],[8,11]],
                    [[0,4],[1,2],[3,5],[6,10],[7,8],[9,11]],
                    [[0,5],[1,3],[2,4],[6,11],[7,9],[8,10]]]
        
        for i in range(6):
            for week in scheduled:
                for matchup in week:
                    conf_count = 0
                    while True:
                        if matchup[conf_count] == i:
                            matchup[conf_count] = conf[i]
                        elif matchup[conf_count] == i+6:
                            matchup[conf_count] = conf2[i]
                        conf_count += 1
                        if conf_count > 1:
                            break
        
        for i in range(6):
            week = []
            for y in range(6):
                week.append([conf[i], conf2[y]])
            scheduled.append(week)
            
            if i < 6:
                new_confs2 = []
                for z in range(6):
                    if z == 0:
                        new_confs2.append(conf2[5])
                    else:
                        new_confs2.append(conf2[z-1])
                confs2 = new_confs2
                
        for week in scheduled:
            game_week = []
            for matchup in week:
                for z in range(12):
                    game_week.append([self.conferences[matchup[0]].rank_order[z].club_id, self.conferences[matchup[1]].rank_order[z].club_id])
            self.schedule_of_games.append(game_week)
            
    def player_week(self, week):
        for game in week:
            Game(self.teams[game[0]], self.teams[game[1]], self)
            
    def coach_creation(self):
        while True:
            if len(self.coaches) < len(self.teams)*3:
                self.coaches[self.world_coach_id] = Coach(self.world_coach_id)
                self.world_coach_id += 1
            else:
                break
                
    def recruit_creation(self):
        self.recruits = {}
        total = 0
        for id, team in self.teams.iteritems():
            total += team.open_spots()
            
        for x in range(total*3):
            self.recruits[self.world_id] = Player(self.world_id)
            self.world_id += 1
    
    def confere_creation(self):
        for x in range(12):
            self.conferences[self.conf_id] = Conference(self.conf_id)
            self.conf_id += 1
    
    def recruit_loop(self):
        self.recruit_creation()
        while True:
        #for x in range(20):
            total = 0
            for id, team in self.teams.iteritems():
                total += team.open_spots()
            
            for id, player in self.recruits.iteritems():
                player.short_list = []
            
            if total > 0:
                for id, team in self.teams.iteritems():
                    self.coaches[team.head_coach].recruiting(team, self.recruits)
                count = 0
                for id,recruit in self.recruits.iteritems():
                    if len(recruit.short_list) > 0:
                        chosen = recruit.choose_school(self)
                        for z in range(len(chosen.roster)):
                            if chosen.roster[z] == 0:
                                recruit.recruited = True
                                chosen.roster[z] = recruit
                                self.players[recruit.player_id] = recruit
                                break
                    else:
                        count += 1
            else:
                break
    
    def coach_offer_reset(self):
        for id in self.coaches:
            self.coaches[id].job_offers = []
            
    def fire_ext_loop(self, average_salary):
        for id in self.teams:
            if self.teams[id].contract_length < 1 and self.teams[id].head_coach != 0:
                self.teams[id].fire_extend_check(self)
                if self.teams[id].contract_length > 0:
                    money = self.teams[id].coach_value(self.teams[id].head_coach)
                    #print self.teams[id].contract_length
                    choice = self.teams[id].head_coach.ext_choice(average_salary, money)
                    if choice is True:
                        self.teams[id].coach_salary = money
                        self.teams[id].ast_salary = money/4
                        self.teams[id].head_coach.contract = [money, self.teams[id].contract_length]
                    else:
                        self.teams[id].head_coach.hired = False
                        self.teams[id].head_coach = 0
            elif self.teams[id].head_coach != 0:
                self.teams[id].fire_extend_check(self, False, True)
    
    def hiring_loop(self, average_salary):
        self.fire_ext_loop(average_salary)
        while True:
        #for i in range(5):
            count = 0
            self.coach_offer_reset()
            job_offers = 0
            for id, team in self.teams.iteritems():
                #print 'id', team.club_id, 'coach', team.head_coach
                if team.head_coach == 0:
                    team.offer_coach(self)
                    count += 1
                '''else:
                    print 'dude'''
            for id, coach in self.coaches.iteritems():
                if len(coach.job_offers) > 0:
                    job_offers += len(coach.job_offers)
                    coach.coach_job_choice(average_salary, self)
                    count -= 1
            '''print job_offers'''
            #print count
            '''print '_____________'''
            if count < 1:
                break
        

        #this is the loop where the head coach selects an assistant coach
        while True:
            count = 0
            self.coach_offer_reset()
            for id, team in self.teams.iteritems():
                if team.ast_coach == 0:
                    count += 1
                    self.coaches[team.head_coach].choose_ast(self)
                
            
            for id, coach in self.coaches.iteritems():
                    if len(coach.job_offers) > 0:
                        coach.coach_job_choice(average_salary, self, True)
                        count -= 1
            #print count
            if count < 1:
                break
                
    def conference_team(self):
        timer = 0
        while True:
            count = 0
            timer += 1
            for id, team in self.teams.iteritems():
                team.conf_offers = []
                if team.conf_id == None:
                    count += 1
            #print count
            if count < 1:
                break
            #print 'new-----------------------'
            for id, conf in self.conferences.iteritems():
                '''if len(conf.teams)>0:
                    for team in conf.teams:
                        print team.club_id'''
                if len(conf.teams) < 12:
                    conf.offer_schools(self)
                
            for id, team in self.teams.iteritems():
                if len(team.conf_offers) > 0:
                    team.pick_conference(self)
                    
    def rank_teams(self):
        rpi = []
        elo = []
        win_p = []
        for id, team in self.teams.iteritems():
            rpi.append([team.club_id, team.rpi, False])
            elo.append([team.club_id, team.pse_elo, False])
            win_p.append([team.club_id, team.wins, False])
            #print team.club_id, team.rpi, team.pse_elo
        
        points_rpi = len(rpi)
        points_elo = len(elo)
        points_win_p = len(win_p)
        
        for i in rpi:
            pick = [-5000000000, 0, 0]
            count = 0
            for x in rpi:
                if x[1] > pick[0] and x[2] == False:
                    pick[0], pick[1], pick[2] = x[1], x[0], count
                count += 1

            self.teams[pick[1]].rank_pts += points_rpi
            points_rpi -= 1
            rpi[pick[2]][2] = True
            
        for i in elo:
            pick = [-5000000000, 0, 0]
            count = 0
            for x in elo:
                if x[1] > pick[0] and x[2] == False:
                    pick[0], pick[1], pick[2] = x[1], x[0], count
                count += 1

            self.teams[pick[1]].rank_pts += points_elo
            points_elo -= 1
            elo[pick[2]][2] = True
        
        for i in win_p:
            pick = [-5000000000, 0, 0]
            count = 0
            for x in win_p:
                if x[1] > pick[0] and x[2] == False:
                    pick[0], pick[1], pick[2] = x[1], x[0], count
                count += 1

            self.teams[pick[1]].rank_pts += points_win_p
            points_win_p -= 1
            win_p[pick[2]][2] = True
        
        pts = []
        for id, team in self.teams.iteritems():
            pts.append([team.club_id, team.rank_pts, False])
            
        points_pts = 64
        for i in pts:
            pick = [-5, 0, 0]
            count = 0
            for x in pts:
                if x[1] > pick[0] and x[2] == False:
                    pick[0], pick[1], pick[2] = x[1], x[0], count
                count += 1

            self.teams[pick[1]].rank += points_pts
            if points_pts > 0:
                points_pts -= 1
            pts[pick[2]][2] = True
    
    def play_tourn_rd(self, bracket, final_four=False):
        new_brack = []
        if final_four == True:
            brack = [[]]
            for region in bracket:
                brack[0].append(region[0])
                
            bracket = brack
                    
        for region in bracket:
            brack = []
            for i in range(len(region)/2):
                brack.append([0,0])
            new_brack.append(brack)
        
        count_r = 0
        count_g = 0
        count_t = 0
        length = 0
            
            
        for region in bracket:
            count_g = 0
            for game in region:
                #print count_r, count_g, count_t
                x = Game(self.teams[game[0]],self.teams[game[1]], self, True)
                #print x
                new_brack[count_r][count_g][count_t] = x
                count_t += 1
                if count_t > 1:
                    count_t = 0
                    count_g += 1
            count_r += 1
            
        return new_brack
                 
    def tournament(self):
        west = [[64,1],[60,5],[56,9],[52,13],[48,17],[44,21],[40,25],[36,29]]
        south = []
        east = []
        midwest = []
        for i in west:
            south.append([i[0]-1,i[1]+1])
            east.append([i[0]-2,i[1]+2])
            midwest.append([i[0]-3,i[1]+3])
        
        bracket = [west, south, east, midwest]
        
        for id, team in self.teams.iteritems():
            if team.rank != 0:
                count_r = 0
                for region in bracket:
                    count_g = 0
                    for game in region:
                        count = 0
                        for seed in game:
                            if team.rank == seed:
                                bracket[count_r][count_g][count] = team.club_id
                            count += 1
                        count_g += 1
                    count_r += 1
                        
        print bracket
        round32 = self.play_tourn_rd(bracket)
        print round32
        sweet16 = self.play_tourn_rd(round32)
        print sweet16
        elite8 = self.play_tourn_rd(sweet16)
        print elite8
        final4 = self.play_tourn_rd(elite8, True)
        print final4
        final = self.play_tourn_rd(final4)
        print final
        champ = Game(self.teams[final[0][0][0]], self.teams[final[0][0][1]], self, True)
        print champ
        
def lineup_stats(lineup, run):
    stats = {}
    count = 0
    for player in lineup:
        print player[0].attr
        count += 1
        player[0].g_stats['GT'] += 1
        #print player[0].exhaustion
        for key, value in player[0].attr.iteritems():
            if count < 2:
                stats[key] = 0
            if key == 'fouling':
                stats[key] += (20.0 - value)/(2.0 * player[0].exhaustion)
            elif key == 'three_conversion':
                stats[key] += value*1.0 * player[0].exhaustion * run
            elif key == 'outside_conversion':
                stats[key] += value* player[0].exhaustion * run
            elif key == 'inside_conv_mod' or key == 'outside_conv_mod':
                stats[key] += value/2.0 * player[0].exhaustion * run
            elif key == 'draw_foul':
                stats[key] += value/4.0 * player[0].exhaustion
            elif key == 'pos_create':
                poss = ((0+value)/10.0) * player[0].exhaustion
                #print value, poss
                stats[key] += poss 
            elif key == 'steal_rate':
                stats[key] += (value/5.0) * run
            elif key == 'assist_rate':
                stats[key] += (value/2.0) * run
            elif key == 'block_rate':
                stats[key] += (value/3.0) * run
            else:
                stats[key] += value * player[0].exhaustion
    #print stats
    return stats

def Game(team1, team2, league, tourn=False):
    #print league.game_count
    #league.game_count += 1
    turns_top = 12
    overall_turn = 1
    foul_out = 6
    if league.college == True:
        turns_top = 10
        foul_out = 5
    half = 1
    score1, score2 = 0, 0
    time_out1, time_out2 = 5, 5
    run1, run2 = 1.0, 1.0
    team1.games_played += 1
    team2.games_played += 1
    team1.player_g_stat_reset(league)
    team2.player_g_stat_reset(league)
    
    test_m, test_s, test_st = [0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]
    
    for i in range(10):
        team1.roster[i].tiredness, team2.roster[i].tiredness = 0,0
        team1.roster[i].set_exhaust()
        team2.roster[i].set_exhaust()
    
    while True:
    
        for player in team1.roster:
            player.rest(True)
        for player in team2.roster:
            player.rest(True)
    
        current_turn = 1
        #possessions
        team1_carry = [0]
        team2_carry = [0]
        while True:
            current_turn += 1
            overall_turn += 1
            called_time = False
            if current_turn > turns_top:
                break
            else:
                called_time = league.coaches[team1.head_coach].call_time(run2, overall_turn, time_out1, team1.roster)
                if called_time == True and time_out1 > 0:
                    time_out1 -= 1
                    run1, run2 = 1.0, 1.0
                    for player in team1.roster:
                        player.rest()
                    for player in team2.roster:
                        player.rest()
                else:
                    called_time = league.coaches[team2.head_coach].call_time(run1, overall_turn, time_out2, team2.roster)
                    if called_time == True and time_out2 > 0:
                        time_out2 -= 1
                        run1, run2 = 1.0, 1.0
                        for player in team1.roster:
                            player.rest()
                        for player in team2.roster:
                            player.rest()
                '''print time_out1, time_out2
                print run1, run2'''
                lineup1 = league.coaches[team1.head_coach].set_lineup(team1.roster, score1-score2, overall_turn, foul_out, turns_top*2)
                lineup2 = league.coaches[team2.head_coach].set_lineup(team2.roster, score2-score1, overall_turn, foul_out, turns_top*2)
                change = Game_turn(lineup1, lineup2, team1_carry, team2_carry, foul_out, run1, run2)
                run1 += change
                if run1 > 1.9:
                    run1 = 1.9
                elif run1 < 0.1:
                    run1 = 0.1
                run2 = 2.0 - run1
                
                count_o = 0
                for player in team1.roster:
                    played = False
                    for i in lineup1:
                        if player.player_id == i[0].player_id:
                            played = True
                    if played == False:
                        player.rest()
                for player in team2.roster:
                    played = False
                    for i in lineup2:
                        if player.player_id == i[0].player_id:
                            played = True
                    if played == False:
                        player.rest()
                score1, score2 = update_points(team1), update_points(team2)
                #print score1, score2
        half += 1
        if half >= 3:
            break
    if score1 == score2:
        overtime = 1
        #print "Overtime: " + str(overtime)
        while True:
            ot_turn = 3
            while True:
                if ot_turn < 1:
                    break
                else:
                    lineup1 = league.coaches[team1.head_coach].set_lineup(team1.roster, score1-score2, current_turn, foul_out, turns_top*2)
                    lineup2 = league.coaches[team2.head_coach].set_lineup(team2.roster, score2-score1, current_turn, foul_out, turns_top*2)
                    change = Game_turn(lineup1, lineup2, team1_carry, team2_carry, foul_out, test_m, test_s, test_st, run1, run2)
                    run1 += change
                    if run1 > 1.9:
                        run1 = 1.9
                    elif run1 < 0.1:
                        run1 = 0.1
                    run2 = 2.0 - run1
                    
                    for player in team1.roster:
                        played = False
                        for i in lineup1:
                            if player.player_id == i[0].player_id:
                                played = True
                        if played == False:
                                player.rest()
                    for player in team2.roster:
                        played = False
                        for i in lineup2:
                            if player.player_id == i[0].player_id:
                                played = True
                        if played == False:
                            player.rest()
                    score1, score2 = update_points(team1), update_points(team2)
                    #print score1, score2
                ot_turn -= 1
            if score1 != score2:
                break
            else:
                overtime += 1
    for player in team1.roster:
        player.post_game_update(team2.club_id)
    for player in team2.roster:
        player.post_game_update(team1.club_id)
        
    if score1 > score2:
        team1.wins += 1
    else:
        team2.wins += 1
    
    '''for player in team1.roster:
        print '----------------'
        for key, stat in player.g_stats.iteritems():
            print key, ': ', stat'''
    
    
    dude1 = team1.update_elo(score1-score2, team2.pse_elo)
    dude2 = team2.update_elo(score2-score1, team1.pse_elo)
    
    team1.current_season_game_log.append((score1, score2, team2.club_id, team1.pse_elo, dude1))
    team2.current_season_game_log.append((score2, score1, team1.club_id, team2.pse_elo, dude2))
    
        
    if tourn == True:
        if score1-score2 > 0:
            return team1.club_id
        else:
            return team2.club_id
    
#this function is for the shooting in a game turn
def shooting(stats, shots, dstats, pl_stats, dpl_stats):
    #[three, outside, inside, inside-rebound, free-throw]
    made = [0,0,0,0,0]
    block = False
    type = 0
    for x in range(4):
        if x == 0:
            type = 15 + stats['three_conversion'] - (dstats['outside_conv_mod'])
        elif x == 1:
            type = 20 + stats['outside_conversion'] - (dstats['outside_conv_mod'])
        elif x == 2 or x == 3:
            type = 27 + stats['inside_conversion'] - (dstats['inside_conv_mod']/1.5)
            block = True
        
        for y in range(shots[x]):
            stop = random.randint(1,100)
            if stop >= 8 + dstats['poss_taken'] - stats['ball_security']:
                lost_rb = 0
                foul = False
                foul_check = random.randint(1,100)
                if foul_check <= (dstats['fouling'] + stats['draw_foul'])/2:
                    foul = True
                    dpl_stats['PF'] += 1
                    lost_rb += 1
                fate = random.randint(1,100)
                if fate <= type:
                    made[x] += 1
                    if foul == True:
                        shots[4] += 1
                    elif block == True:
                        block_check = random.randint(1,100)
                        if block_check <= 10 + dstats['block_rate']:
                            made[x] -= 1
                            dpl_stats['BLK'] += 1
                else:
                    fate = random.randint(1,100)
                    if fate <= stats['assist_rate']*2.4-dstats['steal_rate']:
                        fate = random.randint(1,100)
                        pl_stats['AST'] += 1
                        if fate <= type:
                            made[x] += 1
                            if foul == True:
                                shots[4] += 1
                            elif block == True:
                                block_check = random.randint(1,100)
                                if block_check <= dstats['block_rate']:
                                    made[x] -= 1
                                    dpl_stats['BLK'] += 1
                    if x != 3 and foul == False:
                        rebounds = shots[x]- made[x] #- lost_rb
                        if rebounds < 0:
                            rebounds = 0
                        for z in range(rebounds):
                            disappear = random.randint(1,10)
                            if disappear > 1:
                                rebound_per = (float(stats['rebound'])/(float(stats['rebound']) + 2.0*float(dstats['rebound'])))*100.0
                                reb_fate = random.randint(1,100)
                                if rebound_per >= reb_fate:
                                    shots[3] += 1
                                    pl_stats['ORB'] += 1
                                    '''if block == True:
                                        shots[3] += 1'''
                                else:
                                    dpl_stats['DRB'] += 1
                    elif foul == True:
                        if x == 0:
                            shots[4] += 3
                        else:
                            shots[4] += 2
            else:
                pl_stats['TOV'] += 1
    for i in range(shots[4]):
        conv = random.randint(1,100)
        if conv <= 30 + stats['free_throw']:
            made[4] += 1
   
    return made

def stat_allocate(lineup, shots, made, pl_stats, stats, foul_out):
    shots[2] = shots[2] + shots[3]
    made[2] = made[2] + made[3]
    for x in range(5):
        key = [0,0]
        shot_type = [0,0,0]
        if x == 0:
            key[0], key[1] = 'three_conversion', 'three_rate'
            shot_type[0], shot_type[1], shot_type[2]  = '3PM', '3PA', 3
        elif x == 1:
            key[0], key[1] = 'outside_conversion', 'outside_rate'
            shot_type[0], shot_type[1], shot_type[2] = 'FGM', 'FGA', 2
        elif x == 2:
            key[0], key[1] = 'inside_conversion', 'inside_rate'
            shot_type[0], shot_type[1], shot_type[2] = 'FGM', 'FGA', 2
        elif x == 4:
            key[0], key[1] = 'free_throw', 'draw_foul'
            shot_type[0], shot_type[1], shot_type[2] = 'FTM', 'FTA', 1
            
        if x != 3:
            for z in range(made[x]):
                fate = random.randint(1,math.floor(stats[key[0]]))
                base = math.floor(stats[key[0]])
                #print fate
                passed = 0
                count = 0
                for player in lineup:
                    count += 1
                    base -= player[0].attr[key[0]]
                    if base < fate:
                        player[0].g_stats[shot_type[0]] += 1
                        player[0].g_stats[shot_type[1]] += 1
                        player[0].g_stats['PTS'] += shot_type[2]
                        shots[x] -= 1
                        break
                    else:
                        passed += player[0].attr[key[0]]
            for i in range(shots[x]):
                fate = random.randint(1,math.floor(stats[key[1]]))
                base = math.floor(stats[key[1]])
                passed = 0
                count = 0
                for player in lineup:
                    count += 1
                    base -= player[0].attr[key[0]]
                    if base < fate:
                        player[0].g_stats[shot_type[1]] += 1
                        break
                    else:
                        passed += player[0].attr[key[1]]
    for key, value in pl_stats.iteritems():
        stat = None
        if value != 0:
            if key == 'AST':
                stat = 'assist_rate'
            elif key == 'DRB' or key == 'ORB':
                stat = 'rebound'
            elif key == 'BLK':
                stat = 'block_rate'
            elif key == 'STL':
                stat = 'steal_rate'
            elif key == 'TOV':
                stat = 'ball_security'
            elif key == 'PF':
                stat = 'fouling'
        
        if stat != None:
            for i in range(value):
                z = math.floor(stats[stat])
                if z < 1:
                    z = 1.0
                fate = random.randint(1, z)
                base = math.floor(stats[stat])
                passed = 0
                count = 0
                for player in lineup:
                    count += 1
                    base -= player[0].attr[stat]
                    if base < fate:
                        player[0].g_stats[key] += 1
                        if stat == 'rebound':
                            player[0].g_stats['TRB'] += 1
                        if key == 'PF' and player[0].g_stats[key] > foul_out:
                            #this is so if a player fouls out during a period he will not be given a 7th foul and instead that foul will be placed on someone else.
                            player[0].g_stats[key] -= 1
                        else:
                            break
                    else:
                        passed += player[0].attr[stat]
    
def Game_turn(lineup1, lineup2, carry1, carry2, foul_out, run1, run2):
    stats1 = lineup_stats(lineup1, run1)
    stats2 = lineup_stats(lineup2, run2)
    pl_stats1 = {
            'PTS': 0,
            'FGM': 0,
            'FGA': 0,
            '3PM': 0,
            '3PA': 0,
            'FTM': 0,
            'FTA': 0,
            'ORB': 0,
            'DRB': 0,
            'TRB': 0,
            'AST': 0,
            'STL': 0,
            'BLK': 0,
            'TOV': 0,
            'PF': 0
        }
    pl_stats2 = {
            'PTS': 0,
            'FGM': 0,
            'FGA': 0,
            '3PM': 0,
            '3PA': 0,
            'FTM': 0,
            'FTA': 0,
            'ORB': 0,
            'DRB': 0,
            'TRB': 0,
            'AST': 0,
            'STL': 0,
            'BLK': 0,
            'TOV': 0,
            'PF': 0
        }
    
    #here is the determination of possessions this turn; while taking the carry-over from the previous turns into account
    #and setting the carry-overs to the new remainders
    poss1, poss2 = stats1['pos_create'], stats2['pos_create']
    #print 'start:', poss1, poss2
    poss1 += carry1[0]
    poss2 += carry2[0]
    carry1[0], carry2[0] = poss1%1, poss2%1
    poss1, poss2 = int(poss1), int(poss2)
    #print 'final:', poss1, poss2
    
    #here the 'true' possession total for the period is determined
    steals1, steals2 = 0, 0
    for x in range(poss1):
        fate = random.randint(1,100)
        if fate <= 3 + stats2['steal_rate']:
            steals2 += 1
    for x in range(poss2):
        fate = random.randint(1,100)
        if fate <= 3 + stats1['steal_rate']:
            steals1 += 1
    poss1 -= steals2
    poss2 -= steals1
    if poss1 < 0:
        poss1 = 0
    if poss2 < 0:
        poss2 = 0
    
    pl_stats1['STL'], pl_stats2['STL'] = steals1, steals2
    pl_stats1['TOV'], pl_stats2['TOV'] = steals2, steals1
        
    #here the total possessions are split between three, outside, and inside shots
    #[three, outside, inside, inside-rebounds, free-throw]
    shots1 = [0,0,0,0,0]
    shots2 = [0,0,0,0,0]
    for x in range(poss1):
        choice = random.randint(1,100)
        if choice <= stats1['outside_rate']:
            shots1[1] += 1
        elif choice <= stats1['three_rate'] + stats1['outside_rate']:
            shots1[0] += 1
        else:
            shots1[2] += 1
    for x in range(poss2):
        choice = random.randint(1,100)
        if choice <= stats2['outside_rate']:
            shots2[1] += 1
        elif choice <= stats2['three_rate'] + stats1['outside_rate']:
            shots2[0] += 1
        else:
            shots2[2] += 1
    
    #print shots1, shots2
    #the shooting functions
    made1 = shooting(stats1, shots1, stats2, pl_stats1, pl_stats2)
    made2 = shooting(stats2, shots2, stats1, pl_stats2, pl_stats1)
    stat_allocate(lineup1, shots1, made1, pl_stats1, stats1, foul_out)
    stat_allocate(lineup2, shots2, made2, pl_stats2, stats2, foul_out)
    for player in lineup1:
        player[0].tired_set()
        player[0].update_percents(player[0].g_stats)
    for player in lineup2:
        player[0].tired_set()
        player[0].update_percents(player[0].g_stats)
    return update_run(pl_stats1, pl_stats2)
   
def update_points(team):
    #     [3p,2p,FT]
    fgs = [0,0,0]
    for player in team.roster:
        fgs[1] += player.g_stats['FGM']
        fgs[0] += player.g_stats['3PM']
        fgs[2] += player.g_stats['FTM']
    
    return fgs[0]*3+fgs[1]*2+fgs[2]

def update_run(stats1, stats2):
    points1, points2 = 0, 0
    points1 += (2*stats1['3PM']) + stats1['FGM'] + (2*stats1['BLK']) + (2*stats1['STL'])
    points2 += (2*stats2['3PM']) + stats2['FGM'] + (2*stats2['BLK']) + (2*stats2['STL'])
    return float(points1 - points2)/10.0