from os.path import abspath, dirname, join
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from utils import constants

class LabelBox(Widget):
    # Defaults
    # value = 0
    bg_color = (0.1, 0.1, 0.1, 1)
    font_size = 100
    font_color = (1, 0.8, 0, 1)
    pos = (100, 100)
    image = None

    def __init__(self,
                 layout,
                 # value=value,
                 image=image,
                 bg_color=bg_color,
                 font_size=font_size,
                 font_color=font_color,
                 pos=pos,
                 **kw):
        super().__init__(**kw)
        adjusted_position = (pos[0] - self.size[0] / 2, pos[1])

        self.layout = RelativeLayout(pos=adjusted_position)
        # self.value = value
        self.bg_color = bg_color
        self.font_size = font_size
        self.font_color = font_color
        self.pos = pos

        self.label = Label(text="", font_name=constants.Constants.font(), font_size=self.font_size, color=self.font_color)
        self.label.size_hint = (None, None)
        self.label.size = (300, 150)
        self.label.pos = self.pos


        if image:
            self.calculated_bg_size = self.calculate_bg_size()
            adjusted_image_position = (pos[0] - 50, pos[1] + 20)
            path = dirname(abspath(image))
            file = str(join(path, "assets/{}".format(image)))
            self.image = Image(source=file, pos=adjusted_image_position, size_hint=(0.15, 0.15))

            self.label.pos = (self.pos[0] + self.image.width, self.pos[1])

            self.layout.add_widget(self.image)

        with self.layout.canvas.before:
            Color(*bg_color)
            Rectangle(size=self.calculate_bg_size(), pos=self.calculate_bg_pos())

        self.layout.add_widget(self.label)

        layout.add_widget(self.layout)

        self.label.bind(text=self.update_rect)

    def calculate_bg_size(self):
        total_width = self.label.width
        if self.image:
            total_width += self.image.width
        return (total_width, self.label.height)

    def calculate_bg_pos(self):
        if self.image:
            return (self.pos[0] - self.image.width, self.pos[1])
        return self.pos

    def update_rect(self, *args):
        pass

    def Update(self, value):
        # self.value = value
        self.label.text = str(value)
