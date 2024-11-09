from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
#from dataFetcher import DataFetcher
from components.colored_image_box import ColoredImageBox
from components.image_box import ImageBox
from gauge import GaugeWidget
from dataFetcher import DataFetcher
from components.miniGauge import MiniGauge
import threading

class Dashboard(App):
    size = (800, 800)
    fps = 24

    bottom_left = (10, 160)
    bottom_right = (400, 160)
    top_left = (10, 320)
    top_right = (400, 320)

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
            10.0, 0.0, 300.0,
            300,
            "kPa"
        )

        self.iatLabel = ImageBox(layout, "iat.png", self.bottom_left)
        self.otLabel = ImageBox(layout, "ot.png", self.bottom_right, align_left=False)
        self.opLabel = ImageBox(layout, "op.png", self.top_left)
        self.egtLabel = ColoredImageBox(layout, "ot.png", self.top_right, align_left=False)

        Clock.schedule_interval(self.update_display, (1/self.fps))

        return layout

    def on_stop(self):
        self.data_fetcher.stop()

    def update_display(self, dt): 
        if self.shared_data == {}:
            return

        with self.data_lock:
            try:
                MAP = self.shared_data['MAP']
                AFR = self.shared_data['AFR']
                IAT = self.shared_data['IAT']
                OT = self.shared_data['OT']
                OP = self.shared_data['OP']
                EGT = self.shared_data['EGT']

                self.mapGauge.Update(MAP)
                self.afrGauge.Update(AFR)
                self.iatLabel.Update(IAT)
                self.otLabel.Update(OT)
                self.opLabel.Update(OP)
                self.egtLabel.Update(EGT)
            except KeyError:
                print("Invalid shared_data: ", self.shared_data)


if __name__ == '__main__':
    Dashboard().run()
