from os.path import abspath, dirname, join
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.relativelayout import RelativeLayout

from utils.constants import Constants

class ImageBox(RelativeLayout):
    # Defaults
    font_size = 50
    font_color = (1, 0.8, 0, 1)
    bg_color = (0.1, 0.1, 0.1, 1)
    pos = (100, 100)

    def __init__(self, layout, img_src, pos=pos, align_left=True, font_color=font_color, bg_color=bg_color, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.align_left = align_left
        self.font_color = font_color
        self.bg_color = bg_color

        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rect, size=self.update_rect)

            self.create_image(img_src=img_src)
            self.create_label()

        layout.add_widget(self)

    def create_label(self):
        adjusted_label_position = (self.pos[0] + 135, self.pos[1] + 20) if self.align_left else (self.pos[0] + 50, self.pos[1] + 20)
        self.label = Label(text="0", size_hint=(None, None), font_name=Constants.font(), font_size=self.font_size, color=self.font_color, pos=adjusted_label_position)
        self.label.bind(texture_size=self.update_rect)
        self.add_widget(self.label)
        self.old_label_size = self.label.texture_size[0]

    def create_image(self, img_src):
        path = dirname(abspath(img_src))
        file = str(join(path, "assets/{}".format(img_src)))

        if self.align_left:
            self.image = Image(source=file, pos=(self.pos[0] + 20, self.pos[1]), size_hint=(None, None), size=(100, 100))
        else:
            self.image = Image(source=file, pos=(self.pos[0] + 70, self.pos[1]), size_hint=(None, None), size=(100, 100))
            
        self.add_widget(self.image)

    def update_rect(self, *args):
        self.rect.size = (155 + self.label.texture_size[0], self.image.height)

        if self.align_left:
            self.rect.pos = self.pos
        else:
            self.rect.pos = self.pos[0] - self.label.texture_size[0] + 30, self.pos[1]
            self.label.pos = self.label.pos[0] - self.label.texture_size[0] + self.old_label_size, self.label.pos[1]
            self.old_label_size = self.label.texture_size[0]

    def update_label_size(self, *args):
        self.label.size = self.label.texture_size

    def Update(self, new_val, format="{:.0f}"):
        self.label.text = str(format.format(new_val))
        self.label.texture_update()
        self.update_label_size()
