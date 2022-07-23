import socket 

import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics.texture import Texture
import time
import threading


cnt = 0

def some_func():
	global cnt
	while True:
		time.sleep(1)
		cnt += 1

thread_1 = threading.Thread(target = some_func)

class fscreen(Widget):
	def __init__(self, **kwargs):
		global cnt
		super().__init__(**kwargs)

		Clock.schedule_interval(self.get_fromthread, 1)

	def get_fromthread(self, *args):

		self.ids.lbl.text = 'the count from the outer thread is ' + str(cnt)



class theapp(App):
	def build(self):
		self.screenm = ScreenManager() 

		self.fscreen = fscreen()
		screen = Screen(name = "first screen")
		screen.add_widget(self.fscreen)
		self.screenm.add_widget(screen)

		return self.screenm

if __name__ == "__main__":
	theapp = theapp()			
	
	thread_1.start()
	threading.Thread(target = theapp.run())