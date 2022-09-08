
import gi
gi.require_version('Gst', '1.0')
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics.texture import Texture
from kivy.graphics import *
import time
import os
import numpy as np
import time
from datetime import datetime
import random
from plyer import notification


class welcomescreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def notifyme(self):
		self.body = self.ids.inp.text

		notification.notify(title='NOTICATION TEST', message=self.body, app_icon='/home/odr/Desktop/DEV/Tutorials/kivy/notification/python.png')





class mainscreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)



class theapp(App):
	def build(self):	
		self.screenm = ScreenManager(transition=FadeTransition()) 
		self.welcomescreen = welcomescreen()
		screen = Screen(name = "welcomescreen")
		screen.add_widget(self.welcomescreen)
		self.screenm.add_widget(screen)

		self.mainscreen = mainscreen()
		screen = Screen(name = "mainscreen")
		screen.add_widget(self.mainscreen)
		self.screenm.add_widget(screen)

		return self.screenm

if __name__ == "__main__":

	theapp = theapp()										
	theapp.run()   