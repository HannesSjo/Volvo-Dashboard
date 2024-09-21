from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
#from dataFetcher import DataFetcher
from gauge import GaugeWidget
from dataFetcherDemo import DataFetcher
from components.miniGauge import MiniGauge
import threading

class Dashboard(App):
    size = (800, 800)
    fps = 24

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_lock = threading.Lock()
        self.shared_data = {}
        self.data_fetcher = DataFetcher(self.data_lock, self.shared_data)

    def build(self):
        self.data_fetcher.start()
        layout = RelativeLayout()
        Window.size = self.size

        self.afrGauge = GaugeWidget(
            min_val=9.4,
            max_val=20.0,
            yellow_threshold=12.0,
            green_threshold=17.4,
            show_anim=False,
        )
        layout.add_widget(self.afrGauge)


        self.mapGauge = MiniGauge(
            layout,
            (400,420),
            10, 0, 300,
            300,
            "kPa"
        )

        Clock.schedule_interval(self.update_display, (1/self.fps))

        return layout
    def on_stop(self):
        self.data_fetcher.stop()

    def update_display(self, dt): 
        if self.shared_data == {}:
            return

        with self.data_lock:
            MAP = self.shared_data['MAP']
            AFR = self.shared_data['AFR']

        self.mapGauge.Update(MAP)
        self.afrGauge.Update(AFR)

if __name__ == '__main__':
    Dashboard().run()
