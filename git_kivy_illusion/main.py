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
from functools import partial
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ReferenceListProperty

import time
import math
import numpy as np
import random

class fscreen(Widget):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.init = False

		self.tch = ''
		self.d = 0
		self.p = 0

		self.xpt1 = 0
		self.ypt1 = 0
		self.ypt3 = 0
		self.xpt3 = 0
		self.ypt2 = 0
		self.xpt2 = 0
		self.cnt = 0

		self.obj_bzlist = []

		self.list_bz_minus = []
		self.list_bz_plus = []
		self.string_par_minus = []
		self.string_par_plus = []
		self.curvingy= 0.7
		self.curvingx= 0.6

		self.converge_end = self.y*0.5
		self.converge_y = self.y*0.5		##### bezier initial curving
		self.converge_x = self.y*0.5
		self.converge_endx = self.x*0.5
		self.b =self.x*0.35	
		self.a = self.b				#### Eclipse formula
		self.k =self.y*0.5
		self.h = self.x*0.5


		self.bz1 = Line(bezier=(0, 0, 0, 0, 0, 0),width = 0)
		self.bz2 = Line(bezier=(0, 0, 0, 0, 0, 0),width = 0)


		Clock.schedule_interval(self.converge_update, 1/60)
		Clock.schedule_interval(self.convergex_update, 1/60)
		Clock.schedule_interval(self.curv, 2)





	def on_touch_down(self, touch):
		if self.init == False:	
			self.x = self.width
			self.y = self.height
			       ########## dist between point and point 2 in object

			self.x_obj_end = self.x*0.5
			self.y_obj_end = self.y*0.23					#####initial object
			self.converge_obj_x = self.x*0.5
			self.converge_obj_y = self.y*0.23

			########################
			self.converge_end = self.y*0.5
			self.converge_y = self.y*0.5		##### bezier initial curving
			self.converge_x = self.y*0.5
			self.converge_endx = self.x*0.5

			################
			self.b = self.x*0.35
			self.a = self.y*0.4					#### Eclipse formula
			self.k =self.y*0.5
			self.h = self.x*0.5
			################
			
				
			for self.i in np.arange(self.y*0.1, self.y*0.91, self.y*0.025):
				print(str(self.i))
				self.x_bez_start_minus = (-(self.b*math.sqrt(-(self.i*self.i) + (2*self.k*self.i)-(self.k*self.k)+(self.a*self.a)))/self.a)+self.h
				self.x_bez_start_plus = ((self.b*math.sqrt(-(self.i*self.i) + (2*self.k*self.i)-(self.k*self.k)+(self.a*self.a)))/self.a)+self.h
	
				with self.canvas:
					Color(random.uniform(0, 1), random.uniform(0,1), random.uniform(0, 1))
					self.linebz_minus = Line(bezier=(self.x_bez_start_minus, self.i, self.x*0.5, self.converge_y  , self.x/2, self.converge_end),width = 1)
					self.linebz_plus = Line(bezier=(self.x_bez_start_plus, self.i, self.x*0.5, self.converge_y  , self.x/2, self.converge_end),width = 1)					
						
					self.list_bz_minus.append(self.linebz_minus)
					self.string_par_minus.append(str(self.x_bez_start_minus)+','+str(self.i)+','+str(self.x*0.5)+','+str(self.converge_y)+','+str(self.x/2)+','+str(self.converge_end))
						
					self.list_bz_plus.append(self.linebz_plus)
					self.string_par_plus.append(str(self.x_bez_start_plus)+','+str(self.i)+','+str(self.x*0.5)+','+str(self.converge_y)+','+str(self.x/2)+','+str(self.converge_end))
					self.cnt = self.cnt+1
			
			
			

			print('this is   ' +str(self.d))
		self.init = True	


	def convergex_update(self, *args):
			if self.converge_endx < self.x*self.curvingx:

				self.converge_endx = self.converge_endx + self.x*0.008
				self.x_obj_end = self.converge_endx

				#self.object_bz1 = Line(bezier=(self.x_object_1, self.y_object_2, self.converge_obj_x, self.converge_obj_y  , self.x_obj_end, self.y_obj_end ),width = 1)
				
				#self.object_bz2 = Line(bezier=(self.x_object_2, self.y_object_2, self.converge_obj_x, self.converge_obj_y , self.x_obj_end, self.y_obj_end ),width = 1)
			

				for self.ind in range(0, self.cnt, 1):
					
					self.list_bz_plus[self.ind].bezier = [float(self.string_par_plus[self.ind].split(',')[0]),float(self.string_par_plus[self.ind].split(',')[1]),float(self.string_par_plus[self.ind].split(',')[2]),float(self.string_par_plus[self.ind].split(',')[3]), self.converge_endx,self.converge_end]
					
					#self.object_bz1 = Line(bezier=(self.x_object_1, self.y_object_2, self.converge_obj_x, self.converge_obj_y  , self.x_obj_end, self.y_obj_end ),width = 1)	
					#self.object_bz2 = Line(bezier=(self.x_object_2, self.y_object_2, self.converge_obj_x, self.converge_obj_y , self.x_obj_end, self.y_obj_end ),width = 1)
					
					self.list_bz_minus[self.ind].bezier = [float(self.string_par_minus[self.ind].split(',')[0]),float(self.string_par_minus[self.ind].split(',')[1]),float(self.string_par_minus[self.ind].split(',')[2]),float(self.string_par_minus[self.ind].split(',')[3]), self.converge_endx,self.converge_end]

			if self.converge_endx >= self.x*self.curvingx:

				self.converge_endx = self.converge_endx - self.x*0.008
				self.x_obj_end = self.converge_endx
				
				for self.ind in range(0, self.cnt, 1):
					self.list_bz_plus[self.ind].bezier = [float(self.string_par_plus[self.ind].split(',')[0]),float(self.string_par_plus[self.ind].split(',')[1]),float(self.string_par_plus[self.ind].split(',')[2]),float(self.string_par_plus[self.ind].split(',')[3]), self.converge_endx,self.converge_end]
					self.list_bz_minus[self.ind].bezier = [float(self.string_par_minus[self.ind].split(',')[0]),float(self.string_par_minus[self.ind].split(',')[1]),float(self.string_par_minus[self.ind].split(',')[2]),float(self.string_par_minus[self.ind].split(',')[3]), self.converge_endx,self.converge_end]



	def converge_update(self, *args):

			if self.converge_end < self.y*self.curvingy:   
				self.converge_end = self.converge_end + self.y*0.008   
				self.y_obj_end = self.converge_end

			if self.converge_end >= self.y*self.curvingy:
				self.converge_end = self.converge_end - self.y*0.008		
				self.y_obj_end = self.converge_end

	def curv(self, *args):
		if self.curvingx > 0.5:
			self.curvingx = random.uniform(-0.1,-0.2)
		elif self.curvingx < 0.5:
			self.curvingx = random.uniform(1.1, 1.2)

			if self.curvingy > 0.5:
				self.curvingy = random.uniform(-0.1, -0.2)
			elif self.curvingy < 0.5:
				self.curvingy = random.uniform(1.2, 1.3)





	def generate(self, *args):
		pass



	def move_generated(self, *args):
		pass



class secscreen(Widget):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)






class thscreen(Widget):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		pass


class theapp(App):
	def build(self):
		self.screenm = ScreenManager(transition=FadeTransition())

		self.fscreen = fscreen()
		screen = Screen(name = "first screen")
		screen.add_widget(self.fscreen)
		self.screenm.add_widget(screen)

		self.secscreen = secscreen()
		screen  = Screen(name = "secondscreen")
		screen.add_widget(self.secscreen)
		self.screenm.add_widget(screen)

		self.thscreen = thscreen()
		screen  = Screen(name = "thirdscreen")
		screen.add_widget(self.thscreen)
		self.screenm.add_widget(screen)

		return self.screenm


if __name__ == "__main__":
	theapp = theapp()
	theapp.run()
