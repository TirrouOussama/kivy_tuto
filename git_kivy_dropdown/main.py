from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget 
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown


class fscreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


	def select(self):
		print(self.ids.drop.text)


class theapp(App):
	def build(self):		
		self.screenm = ScreenManager() 

		self.fscreen = fscreen()
		screen = Screen(name = "fscreen")
		screen.add_widget(self.fscreen)
		self.screenm.add_widget(screen)


		return self.screenm

if __name__ == "__main__":
	theapp = theapp()										
	theapp.run() 