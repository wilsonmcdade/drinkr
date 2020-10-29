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
DUTY = 5

# pin initialization
pumppins = {
    '1': 32,
    '2': 33,
    '3': 35,
    '4': 18
}

GPIO.setmode(GPIO.BOARD)

for pump in pumppins.values():
    GPIO.setup(pump,GPIO.OUT)

# creating pwm instances for the pumps
pumpsig = []
for pump in pumppins.values():
    pumpsig.append((GPIO.PWM,pump,0.05))

# Configure logging modes, format
def log_setup():
    logging.basicConfig(filename='drinkr.log', filemode='w', format='%(asctime)s\
     - %(levelname)s - %(message)s')
    logging.info('Beginning Log')
    return

# Kivy app
class drinkr(App):

    '''
        Kivy build function
        Initiates config and settings, loads the drinkr.kv file, names buttons based on the config file,
            and sets the background color.
        returns a widget structure.
    '''
    def build(self):
        config = self.config
        self.settings_cls = SettingsWithSidebar

        root = Builder.load_file('drinkr.kv')
        
        labels = root.ids
        idx = 0
        for labeled, label in labels.items():
            label.text = self.config.get(str(idx),'name')
            if str(idx) not in config.sections():
                logging.info("Index %i not in config sections",idx)
            idx += 1


        global DUTY
        DUTY = int(self.config.get('general','speed'))

        Window.clearcolor = (.85,.85,.85,1)

        return root

    '''
        build_config
        Basically just sets the default values, to be inserted into the 
		drinkr.ini. These get overwritten whenever the settings are
		changed so they're not entirely important
    '''
    def build_config(self, config):
        config.setdefaults(
                'general',{
                    'speed':5,
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
 
    '''
        Custom pump function, pumps from a specific pump
        Checks if the pump number is valid, calls pumpsig function to change the
		pumps duty cycle, starting pump
    '''
    def pump(self,num,mode):
        if str(num) in pumppins.keys():
            if mode is 1:
                pump = pumpsig[int(num)-1][0](*pumpsig[int(num)-1][1:])
                pump.start(DUTY)
                pump.ChangeDutyCycle(15*DUTY)
                logging.info('Pump: Pumping %i', int(num))
            else:
                pump = pumpsig[int(num)-1][0](*pumpsig[int(num)-1][1:])
                pump.ChangeDutyCycle(0)
                pump.stop()
                logging.info('Pump: Stopping pump %i', int(num))

        else:
            logging.info('Pump: Num not in Pumps: %i',int(num))
   
    '''
        builds settings panels
    '''
    def build_settings(self,settings):
        settings.add_json_panel('Settings', self.config, '/home/pi/drinkr/drinks.json')

    '''
        on_config_change changes the config file
        Sees a config change, checks if it's valid, and makes changes to the config file.
    '''
    def on_config_change(self, config, section, key, value):
        if (section not in pumppins.keys()) and (section != 'general'):
            logging.info('Something went wrong.')
            logging.debug('Config: section not valid: Section: %s, Key: %s, Value: %s',section,key,value)
        else :
            logging.debug('Config: Section; %s, Key: %s, Value: %s',section,key,value)
            if section is 'general':
                if key is 'speed':
                    if int(value) > 5 and int(value) < 0:
                        self.popup = Popup(title="Error", content=Label(text='Please keep the speed between 0 and 5.'))
                        popup.open()
                        logging.info('Config: Speed invalid')
                        logging.debug('Config: Invalid Speed: %s',value)
                    else: 
                        global DUTY
                        DUTY = int(value)/5
                        logging.info('Config: Duty cycle is now %i',int(value)/5)
                elif key is 'debug':
                    if value is '0':
                        logging.setLevel('INFO')
                    else:
                        logging.setLevel('DEBUG')
                else:
                    logging.info('Config: Key not found: %s',key)
            else:
                if section is '1':
                    if key is 'enable':
                        if value is '0':
                            #disable pump
                            print(self)
                 
    def close_settings(self, settings=None):
        logging.info('Settings: Closing settings')
        super(drinkr, self).close_settings(settings)
        os.system('python3 /home/pi/drinkr/main.py')
	#print(f'exec: {sys.executable} {["python3"] + sys.argv}')
        #os.execvp(sys.executable, ['python3'] + sys.argv)



if __name__ == "__main__":
    log_setup()
    
    Config.set('graphics','fullscreen','auto')
    Config.set('graphics','window_state','maximized')
    Config.write()
    
    logging.info('Initial Configuration')
    
    logging.info('Starting App')
    drinkr().run()
