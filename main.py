# main.py
# @author Wilson McDade, mcdade@csh

# general imports
import RPi.GPIO as GPIO
import datetime
import logging
import os
import sys

# kivy imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color
from kivy.config import Config, ConfigParser
from kivy.uix.settings import SettingsWithSidebar
from kivy.lang.builder import Builder
from kivy.core.window import Window

#global initialization
dutycycle = 0.5

# pin initialization
pumppins = {
    '1': 12,
    '2': 13,
    '3': 18,
    '4': 19
}

GPIO.setmode(GPIO.BOARD)

for pump in pumppins.values():
    GPIO.setup(pump,GPIO.OUT)

# creating pwm instances for the pumps
pumpsig = []
for pump in pumppins.values():
    pumpsig.append((GPIO.PWM,pump,0.05))

def log_setup():
    logging.basicConfig(filename='drinkr.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Beginning Log')
    return

class drinkr(App):
    def build(self):
        config = self.config
        self.settings_cls = SettingsWithSidebar

        root = Builder.load_file('drinkr.kv')
        
        labels = root.ids
        idx = 1
        for labeled, label in labels.items():
            label.text = self.config.get(str(idx),'name')
            idx += 1

        Window.clearcolor = (.85,.85,.85,1)

        return root

    def build_config(self, config):
        config.setdefaults(
                'general',{
                    'speed':2,
                    'debug':0
                    })
        config.setdefaults(
                '1',{
                    'enable':1,
                    'name':'Drink 1'
                    })
        config.setdefaults(
                '2',{
                    'enable':1,
                    'name':'Drink 2'
                    })
        config.setdefaults(
                '3',{
                    'enable':1,
                    'name':'Drink 3'
                    })
        config.setdefaults(
                '4',{
                    'enable':1,
                    'name':'Drink 4'
                    })
 
    def pump(self,num):
        if str(num) in pumppins.keys():
            pumpsig[int(num)][0](*pumpsig[int(num)][1:])
            logging.info('Pumping')
            logging.debug('Pumping pump %i', num)
        else:
            logging.info('Num not in Pumps: %i',num)
            logging.debug('Pump %i not in pumps list', num)
   
    #at some point make a settings button and call this
    def build_settings(self,settings):
        settings.add_json_panel('Settings', self.config, 'drinks.json')

    def on_config_change(self, config, section, key, value):
        if (section not in pumppins.keys()) or (section != 'general'):
            logging.info('Something went wrong.')
            logging.debug('Config section not valid: Section: %s, Key: %s, Value: %s',section,key,value)
        else :
            if section is 'general':
                if key is 'speed':
                    if int(value) > 5 or int(value) < 0:
                        logging.info('Speed invalid')
                        logging.debug('Invalid Speed: %s',value)
                    else: 
                        global dutycycle
                        dutycycle = value/5
                if key is 'debug':
                    if value is '0':
                        logging.setLevel('INFO')
                    else:
                        logging.setLevel('DEBUG')
        
    def close_settings(self, settings=None):
        super(drinkr, self).close_settings(settings)
        print(f'exec: {sys.executable} {["python"] + sys.argv}')
        os.execvp(sys.executable, ['python'] + sys.argv)



if __name__ == "__main__":
    log_setup()
    
    Config.set('graphics','fullscreen','auto')
    Config.set('graphics','window_state','maximized')
    Config.write()
    
    logging.info('Initial Configuration')
    
    logging.info('Starting App')
    drinkr().run()
