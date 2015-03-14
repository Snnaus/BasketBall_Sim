from engine import *
import datetime, pickle, shelve, csv

save = shelve.open('test_league.txt')
one = save['one']
#print one

#one.schedule_of_games = []
#one.set_out_conf()
#one.set_schedule()
one.play_season()
#one.tournament()

count = 1
'''for i in one.teams[200].current_season_game_log:
    print i, count
    count += 1'''
'''for i, team in one.teams.iteritems():
    print team.games_played
'''

'''with open('rankings.csv', 'w') as csvfile:
    fieldnames = ['ID', 'Win%', 'Elo1', 'Elo2','Diff', 'RPI', 'PTS', 'Rank']
    export = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    for i, team in one.teams.iteritems():
        export.writerow({'ID': i,'Win%': round(float(team.wins)/float(team.games_played),3), 'Elo1': round(team.pse_elo,4), 'Elo2': round(team.pse_elo2,4), 'Diff': round(team.pse_elo-team.pse_elo2,4), 'RPI': team.rpi, 'PTS': team.rank_pts, 'Rank': team.rank})
'''
'''for i, team in one.teams.iteritems():
        print team.club_id, ': ', round((float(team.wins)/float(team.games_played)),3) , round(team.pse_elo, 4), round(team.pse_elo2, 4), team.rpi, team.rank_pts, team.rank #team.wins, team.games_played-team.wins, team.games_played
'''
#print lineup_stats(one.teams[150].roster)
average = {}
players = 0

for i,value in one.teams[150].roster[0].career_season_log[2001].iteritems():
    average[i] = 0
#print average
for i,player in one.players.iteritems():
        #print player.career_season_log[2001]
        if player.career_season_log[2001]['GT'] > 500:
                players += 1
                #print player.career_season_log[1]
                for key,value in player.career_season_log[2001].iteritems():
                        #print key, type(value)
                        average[key] += value
print '# of players: ', players
for i,value in average.iteritems():
        printer = round((float(value)/float(players))/33, 2)
        if i == 'FT%' or i == 'FG%' or i == '3P%':
                printer = value/players
        print i,': ', printer
'''for i, team in one.teams.iteritems():
    print team.roster[0]'''

#one = pickle.load(open('one_test.txt', 'rb'))

'''for i in one:
    print i'''
