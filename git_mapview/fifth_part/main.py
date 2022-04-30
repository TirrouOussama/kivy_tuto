
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
import requests
import re

class fscreen(Widget):
	my_avat = StringProperty()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.placed = False
		self.exists = False
		self.ids.main_map.zoom = 15
		self.ids.main_map.center_on(self.ids.main_map_me.lat, self.ids.main_map_me.lon)
		self.my_avat = 'avatar.png'

	def press(self):
		print(str(self.ids.main_map_me.lat) +  ' | ' + str(self.ids.main_map_me.lon))

	def place_pin(self):
		self.placed = True

	def remove_pin(self):
		if self.exists == True:
			self.ids.main_map.remove_widget(self.dist)
			self.placed = False
			self.exists = False

	def on_touch_up(self, touch):
		if touch.y > self.height*0.05:
			if self.placed == True and self.exists == False:
				self.dist = MapMarkerPopup(lat=self.ids.main_map.get_latlon_at(touch.x, touch.y)[0], lon=self.ids.main_map.get_latlon_at(touch.x, touch.y)[1], source='dist.png')
				
				self.btn = Button(text='print loc', on_press=self.press_dist)
				self.dist.add_widget(self.btn)
				self.ids.main_map.add_widget(self.dist)
				print(self.ids.main_map.get_latlon_at(touch.x, touch.y))
				self.exists = True

	def press_dist(self, instance):
		print(self.dist.lat)
		print(self.dist.lon)

		self.start_lon = self.ids.main_map_me.lon
		self.start_lat = self.ids.main_map_me.lat

		self.end_lon = self.dist.lon 
		self.end_lat = self.dist.lat
		self.body = {"coordinates":[[self.start_lon,self.start_lat],[self.end_lon,self.end_lat]]}
		self.headers = {
    		'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    		'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
    		'Content-Type': 'application/json; charset=utf-8'}
		self.call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=self.body, headers=self.headers)
		print(self.call.text)
		self.string_res = self.call.text

		print(self.string_res)

		self.tag = 'rtept'
		self.reg_str = '</' + self.tag + '>(.*?)' + '>'
		self.res = re.findall(self.reg_str, self.string_res)
		print(self.res)
		print('_____________________________________')
		self.string1 = str(self.res)
		self.tag1 = '"'
		self.reg_str1 = '"' + '(.*?)' + '"'
		self.res1 = re.findall(self.reg_str1, self.string1)
		print(self.res1)

		for i in range(0, len(self.res1)-1, 2):
			print('lat= ' + self.res1[i])
			print('lon= ' + self.res1[i+1])

			self.points_lat = self.res1[i]
			self.points_lon = self.res1[i+1]

			self.points_pop = MapMarkerPopup(lat=self.points_lat, lon=self.points_lon, source='waypoints.png')
			self.ids.main_map.add_widget(self.points_pop)


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