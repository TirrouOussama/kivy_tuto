from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivy_gradient import Gradient


class SupperButton(Button):
    gr_left = StringProperty()
    gr_middle = StringProperty()
    gr_right = StringProperty()
    border_width = NumericProperty(1)
    border_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.l_save = None
        self.r_save = None

    def pressed(self):
        self.l_save = self.gr_left
        self.r_save = self.gr_right
        self.gr_left = "#474747"
        self.gr_right = "#949191"
        Clock.schedule_interval(self.press_anim, 0.3)

    def press_anim(self, *args):
        self.gr_left = self.l_save
        self.gr_right = self.r_save
        Clock.unschedule(self.press_anim)
