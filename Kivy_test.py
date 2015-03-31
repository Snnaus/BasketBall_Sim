from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
#from single_game_test import *
from user_game import *
from engine import *
import shelve

dude = shelve.open("test_league_3_27_2015.txt")
one = dude['one']

class MenuScreen(Screen):
    pass
    
class ScoreBoardScreen(Screen):
    def __init__(self, **kwargs):
        super(ScoreBoardScreen, self).__init__()
    pass

class TestButton(Button):
    def press_callback(self):
        test_game()


class GameSM(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManager, self).__init__()
    bball_game = ObjectProperty(UserGame())
    universal_text = StringProperty('Start')
    score1, score2 = NumericProperty(0), NumericProperty(0)
        
    def uni_button_call(self):
        if self.bball_game.game_started == False:
            self.bball_game.game_start(one.teams[150], one.teams[102], one)
            self.universal_text = 'Next Turn'
        else:
            self.bball_game.play_turn()
            self.score1, self.score2 = bball_game.score1, bball_game.score2
            if self.bball_game.game_fin == True:
                self.universal_text = 'Start Again?'
    

class Game(App):

    def build(self):
        sm = GameSM()
        #sm.add_widget(MenuScreen(name='menu'))
        #sm.add_widget(ScoreBoardScreen(name='scoreboard'))
        return sm
        
        
if __name__ == '__main__':
    #test_game()
    Game().run()