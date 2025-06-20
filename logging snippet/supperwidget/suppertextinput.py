from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivy_gradient import Gradient
from kivy.lang import Builder

# Builder.load_file('supperwidget/suppertextinput.kv')


class SupperTextinput(TextInput):
    line_h = NumericProperty()
    underline_width = NumericProperty(1)  #### has to be > 0
    underline_color = ListProperty([0, 0, 0, 1])
    start_x = NumericProperty()
    end_x = NumericProperty()
    rec_x = NumericProperty()
    rec_px = NumericProperty()

    sz_x = NumericProperty(64)
    sz_y = NumericProperty(64)

    icon_offset = NumericProperty()
    icon_source = StringProperty()
    gr_left = StringProperty("#ffffff")
    gr_middle = StringProperty("#ffffff")

    gr_right = StringProperty("#ffffff")

    border_width = NumericProperty(1)
    border_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_x = 0
        self.end_x = 0
        self.rec_x = 0
        self.rec_px = 0
        self.ref_pos = None
        self.ref_size = None

    def focused_anim(self, sz, ps):
        if self.focus == True:
            self.rec_x = 0
            self.ref_pos = ps
            self.ref_size = sz
            self.start_x = ps[0] + 100
            self.end_x = ps[0] + sz[0] - 100
            self.rec_px = ps[0] + (sz[0] / 2)
            self.underline_color = [0, 0, 0, 1]
            Clock.schedule_interval(self.canvas_rec_expand, 1 / 60)
            Clock.schedule_interval(self.reset_it, 1 / 30)

    def textinput_line_anime(self, *args):
        if self.start_x < self.ref_pos[0] + (self.ref_size[0] / 2) - 100:
            self.start_x += 4  #### this speed by which the line is moving 4px
            self.end_x -= 4  #### this speed by which the line is moving 4px

        elif self.start_x >= self.ref_pos[0] + (self.ref_size[0] / 2) - 100:
            Clock.schedule_interval(self.textinput_line_anime_2, 1 / 60)
            Clock.unschedule(self.textinput_line_anime)

    def textinput_line_anime_2(self, *args):
        if self.start_x >= self.ref_pos[0] + 100:
            self.start_x -= 4  #### this speed by which the line is moving 4px
            self.end_x += 4  #### this speed by which the line is moving 4px

        elif self.start_x < self.ref_pos[0] + (self.ref_size[0] / 2) - 100:
            Clock.schedule_interval(self.textinput_line_anime, 1 / 60)
            Clock.unschedule(self.textinput_line_anime_2)

    def canvas_rec_expand(self, *args):
        if self.rec_x < self.ref_size[0]:
            self.rec_x += 16  #### this speed by which the rec is expanding
            self.rec_px -= 8  #### this speed by which the rec is expanding

        elif self.rec_x >= self.ref_size[0]:
            self.rec_x = self.ref_size[0]
            self.rec_px = self.ref_pos[0]
            Clock.unschedule(self.canvas_rec_expand)
            Clock.schedule_interval(self.textinput_line_anime, 1 / 60)
            Clock.schedule_interval(self.textinput_line_anime, 1 / 60)

    # def on_size(self, *args):
    #   Clock.unschedule(self.textinput_line_anime)
    #   Clock.unschedule(self.textinput_line_anime_2)
    #   Clock.unschedule(self.canvas_rec_expand)
    #   self.rec_x = 0
    #   self.focused_anim(self.size, self.pos)

    def reset_it(self, *args):
        if self.focus == False:
            Clock.unschedule(self.canvas_rec_expand)
            Clock.unschedule(self.textinput_line_anime)
            Clock.unschedule(self.textinput_line_anime_2)
            Clock.unschedule(self.reset_it)
            self.start_x = 0
            self.end_x = 0
            self.rec_px = self.width * 10  ##### this gets insta updated
            #### doesnt get updated
