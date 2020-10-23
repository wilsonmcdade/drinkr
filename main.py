# main.py
# @author Wilson McDade, mcdade@csh

# general imports
import RPi.GPIO as GPIO
import datetime
import logging

# kivy imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color
from kivy.config import Config, ConfigParser

#global initialization
dutycycle = 0.5

# pin initialization
pump1 = 12
pump2 = 13
pump3 = 18
pump4 = 19
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump1, GPIO.OUT)
GPIO.setup(pump2, GPIO.OUT)
GPIO.setup(pump3, GPIO.OUT)
GPIO.setup(pump4, GPIO.OUT)

# creating pwm instances for the pumps
pwm1 = GPIO.PWM(pump1,0.05)
pwm2 = GPIO.PWM(pump2,0.05)
pwm3 = GPIO.PWM(pump3,0.05)
pwm4 = GPIO.PWM(pump4,0.05)

def log_setup():
	logging.basicConfig(filename='drinkr.log', filemode='w", format='%(asctime)s - %(levelname)s - %(message)s')
	logging.info('Beginning Log')
	return

class MainWidget(GridLayout):
	pass

class drinkr(App):
	def build(self):
    		return MainWidget()
	
	#at some point make a settings button and call this
	def build_settings(settings):


if __name__ == "__main__":
	log_setup()

	Config.set('graphics','fullscreen','auto')
	Config.set('graphics','window_state','maximized')
	Config.write()

	logging.info('Initial Configuration')

	logging.info('Starting App')
	drinkr().run()
