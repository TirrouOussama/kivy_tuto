
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from functools import partial
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker, MapSource


class fscreen(Widget):
	my_avat = StringProperty()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.ids.main_map.zoom = 15
		self.ids.main_map.center_on(self.ids.main_map_me.lat, self.ids.main_map_me.lon)
		self.my_avat = 'avatar.png'



	def press(self):
		print(str(self.ids.main_map_me.lat) +  ' | ' + str(self.ids.main_map_me.lon))




		
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
	theapp.run() 