from scribbles_home_build import *
import datetime, pickle, shelve

print datetime.datetime.utcnow()

one = League()
#pickle.dump(one, open("one_test.txt", 'wb'))
save = shelve.open("test.txt")
save['one'] = one
save.close()

print datetime.datetime.utcnow()

#print one.schedule_of_games

'''for id,team in one.teams.iteritems():
    print team.conf_id'''

'''for iid, team in one.teams.iteritems():
        print team.ast_coach'''

#print Game(one.teams[11], one.teams[12], one)

'''print one.teams[1].roster
print one.teams[2].roster

for team in one.teams:
    print one.teams[team].open_spots()'''
print "done"
