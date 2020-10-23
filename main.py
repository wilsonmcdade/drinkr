# main.py
# @author Wilson McDade, mcdade@csh

import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
Config.set('graphics','fullscreen','auto')
Config.set('graphics','window_state','maximized')
Config.write()

class MainWidget(GridLayout):
    pass

class myApp(App):
    def build(self):
        return MainWidget()

if __name__ == "__main__":
    myApp().run()
