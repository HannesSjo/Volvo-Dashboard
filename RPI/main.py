from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
#from dataFetcher import DataFetcher
from label_box import LabelBox
from gauge import GaugeWidget
from dataFetcherDemo import DataFetcher
import threading
import random

class Dashboard(App):
    size = (800, 800)
    fps = 24
    gauge_max_val = 20
    gauge_min_val = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_lock = threading.Lock()
        self.shared_data = {}
        self.label = None
        self.data_fetcher = DataFetcher(self.data_lock, self.shared_data)

    def build(self):
        self.data_fetcher.start()
        Window.size = self.size

        box = BoxLayout(orientation='horizontal', padding=5)

        self.label = Label()
        self.gauge = GaugeWidget(
            min_val=self.gauge_min_val, 
            max_val=self.gauge_max_val,
            yellow_threshold=11,
            green_threshold=15,
            show_anim=False,
        )


        box.add_widget(self.gauge)

        Clock.schedule_interval(self.update_display, (1/self.fps))
        self.gauge.gauge_value = 14.7

        return box

    def on_stop(self):
        self.data_fetcher.stop()

    def update_display(self, dt):
        if self.shared_data == {}:
            return

        with self.data_lock:
            AFR = str(self.shared_data['AFR'])
            self.gauge.gauge_value = AFR

if __name__ == '__main__':
    Dashboard().run()
