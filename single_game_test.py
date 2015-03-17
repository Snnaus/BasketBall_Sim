from engine import *
import datetime, pickle, shelve

save = shelve.open('test_league.txt')
one = save['one']

def test_game():
    one.coaches[one.teams[150].head_coach].user = True
    print Game(one.teams[150], one.teams[102], one, True)



'''for player in one.teams[150].roster:
    print player.posi['OF'] + player.posi['DE']

print '__________________________'

for player in one.teams[164].roster:
    print player.posi['OF'] + player.posi['DE']'''
