from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from utils import constants

class LabelBox(Widget):
    # Defaults
    value = 0
    bg_color = (0.1, 0.1, 0.1, 1)
    font_size = 100
    font_color = (1, 0.8, 0, 1)
    pos = (100, 100)

    def __init__(self,
                 layout,
                 value=value,
                 bg_color=bg_color,
                 font_size=font_size,
                 font_color=font_color,
                 pos=pos,
                 **kw):
        super().__init__(**kw)
        adjusted_position = (pos[0] - self.size[0] / 2, pos[1])

        self.layout = RelativeLayout(pos=adjusted_position)
        self.value = value
        self.bg_color = bg_color
        self.font_size = font_size
        self.font_color = font_color

        self.label = Label(text=str(value), font_name=constants.Constants.font(), font_size=self.font_size, color=self.font_color)
        self.label.size_hint = (None, None)
        self.label.size = (300, 150)
        self.label.pos = self.pos

        self.layout.canvas.add(Color(*bg_color))
        self.layout.canvas.add(Rectangle(size=self.label.size, pos=self.pos))

        self.pos = pos
        self.layout.add_widget(self.label)

        layout.add_widget(self.layout)
