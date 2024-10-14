import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty, ListProperty
from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.lang import Builder

from supperwidget.supperbutton import SupperButton
Builder.load_file("supperwidget/supperbutton.kv")



	  



class datescreen(Widget):

	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.days_list = []
		self.day_selected = 1
		self.current_month = 'January'
		self.current_year = 2024


	def confirm_date(self):
		pass

	def draw_day_buttons(self):
		for i in range(1, 32):
			btn = SupperButton()
			btn.text = str(i)
			btn.gr_left = '#ffffff'
			btn.gr_middle = '#cbcbcb'
			btn.gr_right = '#ffffff'
			btn.font_name = 'resources/fonts/1.ttf'
			btn.border_width = 1
			btn.border_color = [0, 0, 0, 1]
			btn.bind(on_press=self.day_select)
			self.ids.grid_days.add_widget(btn)
			self.days_list.append(btn)

		self.days_list[0].gr_left = "#474747"
		self.days_list[0].gr_right = "#949191"

	def on_size(self, *args):			# this is just to initiate after the size is good 
		if self.width > 100:
			self.draw_day_buttons()

	def day_select(self, instance):
		if self.day_selected is not None:
			self.days_list[int(self.day_selected) - 1].gr_left = '#ffffff'
			self.days_list[int(self.day_selected) - 1].gr_right = '#ffffff'
		
		instance.gr_left = "#474747"
		instance.gr_right = "#949191"

		self.day_selected = int(instance.text)
		self.ids.date_accept_lbl.text = str(self.day_selected) + ' ' +  str(self.current_month) + ' ' + str(self.current_year)



	def move(self, target):
		if target == 'year_left':
			self.ids.input_year.text = str(self.year_prep() - 1)


		elif target == 'year_right':
			if self.year_prep() < 2024:
				self.ids.input_year.text = str(self.year_prep() + 1)


		elif target == 'month_left':
			self.ids.month_lbl.text = self.month_minus()
		elif target == 'month_right':
			self.ids.month_lbl.text = self.month_plus()

		self.current_year = self.ids.input_year.text
		self.current_month = self.ids.month_lbl.text

		c = False
		for items in self.days_list:
			if items.gr_left == '#474747':
				c = True

		if c == False:
			self.days_list[0].gr_left = "#474747"
			self.days_list[0].gr_right = "#949191"
			self.day_selected = '1'

		self.ids.date_accept_lbl.text = str(self.day_selected) + ' ' +  str(self.current_month) + ' ' + str(self.current_year)

	def year_prep(self):
		try:
			year = int(self.ids.input_year.text)
			if 1950 <= year <= 2024:
				return year
		except ValueError:
			pass
		return 2024

	def month_minus(self):
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		months_30 = ['April', 'June', 'September', 'November']
		current_index = months.index(self.ids.month_lbl.text)

		
		if current_index > 0:
			current_index -= 1
		else:
			current_index = len(months) - 1  
		
		previous_month = months[current_index]
		self.update_days_for_month(previous_month)
		
		return previous_month

	def month_plus(self):
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		
		months_30 = ['April', 'June', 'September', 'November']
		current_index = months.index(self.ids.month_lbl.text)
		if current_index < len(months) - 1:
			current_index += 1
		else:
			current_index = 0
		
		next_month = months[current_index]
		self.update_days_for_month(next_month)
		
		return next_month

	def update_days_for_month(self, month):
		months_30 = ['April', 'June', 'September', 'November']
		if month == 'February':
			if self.is_leap_year(self.year_prep()):
				max_days = 29
			else:
				max_days = 28
		elif month in months_30:
			max_days = 30
		else:
			max_days = 31
		current_day_count = len(self.days_list)
		
		if current_day_count > max_days:
			for _ in range(current_day_count - max_days):
				btn = self.days_list.pop()
				self.ids.grid_days.remove_widget(btn)
		elif current_day_count < max_days:
			for i in range(current_day_count + 1, max_days + 1):
				btn = SupperButton()
				btn.text = str(i)
				btn.gr_left = '#ffffff'
				btn.gr_middle = '#cbcbcb'
				btn.gr_right = '#ffffff'
				btn.font_name = 'resources/fonts/1.ttf'
				btn.border_width = 1
				btn.border_color = [0, 0, 0, 1]
				btn.bind(on_press=self.day_select)
				self.ids.grid_days.add_widget(btn)
				self.days_list.append(btn)

	def is_leap_year(self, year):
		return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)



class theapp(App):
	def build(self):
		
		self.screenm = ScreenManager() #(transition=FadeTransition())

		self.datescreen= datescreen()
		screen = Screen(name = "datescreen")
		screen.add_widget(self.datescreen)
		self.screenm.add_widget(screen)

		return self.screenm

if __name__ == "__main__":
	theapp = theapp()										
	theapp.run() 