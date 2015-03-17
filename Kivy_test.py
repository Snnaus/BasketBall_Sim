from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.event import EventDispatcher
from single_game_test import test_game


class MenuScreen(Screen):
    pass
    
class ScoreBoardScreen(Screen):
    pass

class TestButton(Button):
    def press_callback(self):
        test_game()
        

class Game(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ScoreBoardScreen(name='scoreboard'))
        return sm
        
        
if __name__ == '__main__':
    #test_game()
    Game().run()