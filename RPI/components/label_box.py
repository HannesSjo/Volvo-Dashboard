from os.path import abspath, dirname, join
from kivy.app import StringProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

from utils import constants


class LabelBox(RelativeLayout):
    path = dirname(abspath(__file__))
    file_label_box = StringProperty(join(path, "assets/LabelBox2.png"))

    # TODO: fix colors

    # Defaults
    value = 0
    bg_color = (0.1, 0.1, 0.1, 1)
    font_size = 100
    font_color = (1, 0.8, 0, 1)

    def __init__(self, value=value, bg_color=bg_color, font_size=font_size, font_color=font_color, **kw):
        super().__init__(**kw)

        self.pos = (self.center_x - self.width / 2, self.center_y - self.height / 2 - 250)
        self.size = (800, 800)
        self.value = value
        self.bg_color = bg_color
        self.font_size = font_size
        self.font_color = font_color

        self.label = Label(text=str(value), font_name=constants.Constants.font(), font_size=self.font_size, color=self.font_color)

        self.canvas.add(Color(0.1, 0.1, 0.1))
        self.canvas.add(Rectangle(size=(300,150), pos=(250,325)))
        self.add_widget(self.label)
