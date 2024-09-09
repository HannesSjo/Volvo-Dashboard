from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
#from dataFetcher import DataFetcher
from dataFetcherDemo import DataFetcher
import threading

class Dashboard(App):
    size = 800
    fps = 24

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_lock = threading.Lock()
        self.shared_data = {}
        self.label = None
        self.data_fetcher = DataFetcher(self.data_lock, self.shared_data)

    def build(self):
        self.data_fetcher.start()
        Window.size = (self.size, self.size)

        self.label = Label()


        Clock.schedule_interval(self.update_display, (1/self.fps))
        return self.label

    def on_stop(self):
        self.data_fetcher.stop()

    def update_display(self, dt):
        if self.shared_data == {}:
            return
        
        with self.data_lock:
            AFR = str(self.shared_data['AFR'])
            self.label.text = AFR

if __name__ == '__main__':
    Dashboard().run()