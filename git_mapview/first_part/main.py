from kivy.uix.button import Button
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarkerPopup, MapMarker, MapSource
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget 



class fscreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.ids.main_map.zoom = 15
		self.ids.main_map.center_on(36.5924, 2.9898)

		self.pin = MapMarkerPopup(lat=36.59248 ,lon=2.9898 ,source='me_32.png')
		self.btn = Button(size= (self.width*0.2, self.height*0.05), pos=(self.pin.pos[0], self.pin.pos[1]), on_press=self.show)
		self.pin.add_widget(self.btn)

		self.ids.main_map.add_widget(self.pin)



	def show(self, instance):
		print(str(self.pin.lat)+ ' | '+ str(self.pin.lon))


		pass
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
