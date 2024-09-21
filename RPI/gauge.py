from kivy.animation import Animation
from kivy.app import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import ColorProperty, NumericProperty
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

from os.path import join, dirname, abspath

from label_box import LabelBox

class GaugeWidget(Widget):
    path = dirname(abspath(__file__))
    file_gauge_outer = StringProperty(join(path, "assets/GaugeOuter.png"))
    file_gauge_inner = StringProperty(join(path, "assets/GaugeInner.png"))
    file_needle = StringProperty(join(path, "assets/Needle.png"))
    needle_sc = ObjectProperty(None)

    min_rotation = 138.5
    max_rotation = -138.5

    yellow_threshold = 11
    green_threshold = 16

    # Defaults
    gauge_outer_color = (0.08, 0.08, 0.08)
    gauge_inner_color = (0.02, 0.02, 0.02)
    needle_color = ColorProperty((0, 0.98, 0.05))
    needle_over_color = (0.98, 0.02, 0)
    needle_perf_color = (0, 0.98, 0.05)
    needle_under_color = (0.98, 0.90, 0)
    show_anim = False

    min_val = 8
    max_val = 20
    gauge_value = NumericProperty(0.0)

    def __init__( self,
            min_val=min_val,
            max_val=max_val,
            yellow_threshold=yellow_threshold,
            green_threshold=green_threshold,
            gauge_outer_color=gauge_outer_color,
            gauge_inner_color=gauge_inner_color,
            needle_over_color=needle_over_color,
            needle_perf_color=needle_perf_color,
            needle_under_color=needle_under_color,
            show_anim=show_anim,
        **kwargs):
        super().__init__(**kwargs)

        self.min_val = min_val
        self.max_val = max_val
        self.yellow_threshold = yellow_threshold
        self.green_threshold = green_threshold

        self.gauge_outer_color = gauge_outer_color
        self.gauge_inner_color = gauge_inner_color
        self.needle_over_color = needle_over_color
        self.needle_perf_color = needle_perf_color
        self.needle_under_color = needle_under_color

        self.show_anim = show_anim

        if self.show_anim:
            Clock.schedule_once(self.spin_needle, 0)

        self.label_box = LabelBox(value=self.gauge_value)
        self.add_widget(self.label_box)

    def Update(self, value):
        self.gauge_value = value
        self.rotate_needle()
        self.set_needle_color()
        self.label_box.label.text = str(round(self.gauge_value, 2))

    def rotate_needle(self):
        normalized_value = (self.gauge_value - self.min_val) / (self.max_val - self.min_val)
        rotation = (self.min_rotation + normalized_value * (self.max_rotation - self.min_rotation))
        self.set_needle_pos(rotation)

    def set_needle_color(self):
        if self.gauge_value > self.green_threshold:
            self.needle_color = self.needle_over_color
        elif self.gauge_value > self.yellow_threshold:
            self.needle_color = self.needle_perf_color
        else:
            self.needle_color = self.needle_under_color

    def set_needle_pos(self, pos):
        self.needle_sc.rotation = pos

    def spin_needle(self, dt):
        self.set_needle_pos(self.min_rotation)
        spin_anim = Animation(rotation=self.max_rotation, duration=1)

        spin_anim.start(self.needle_sc)
