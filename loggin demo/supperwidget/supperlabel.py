from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivy_gradient import Gradient


#### when modifying the text.property do


class SupperLabel(Label):
    gr_left = StringProperty()
    gr_middle = StringProperty()
    gr_right = StringProperty()
    border_width = NumericProperty(1)
    border_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_saved = None
        self.letters_list = []
        self.cnt_anim = 0
        self.first_capture = False

    def animate_text(self, *args):
        if self.cnt_anim < len(self.letters_list):
            self.text = self.text[:-1]
            self.text = self.text + self.letters_list[self.cnt_anim]
            self.cnt_anim += 1
            self.text = self.text + "_"

        elif self.cnt_anim >= len(self.letters_list):
            self.text = self.text[:-1]
            Clock.unschedule(self.animate_text)

    def on_size(self, *args):
        if self.width > 100:
            if self.first_capture == False:
                self.first_capture = True
                self.text_saved = self.text

            Clock.unschedule(self.animate_text)
            self.text = ""
            self.letters_list = list(self.text_saved)
            self.cnt_anim = 0
            Clock.schedule_interval(self.animate_text, self.type_speed)
