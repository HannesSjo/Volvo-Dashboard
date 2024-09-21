import threading
import time
import json

class DataFetcher:
    def __init__(self, data_lock, shared_data):
        self.data_lock = data_lock
        self.shared_data = shared_data
        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.is_running = True

    def start(self):
        with open('template.json', 'r') as template:
            self.data = json.load(template)
        with self.data_lock:
            self.shared_data.clear()
            self.shared_data.update(self.data)

        self.thread.start()

    def loop(self):
        while self.is_running:
            self.fetchData()

            with self.data_lock:
                self.shared_data.clear()
                self.shared_data.update(self.data)

            time.sleep(0.2)

    def fetchData(self):
        self.data['AFR'] += 0.01
        self.data['MAP'] += 10

    def stop(self):
        self.is_running = False
        self.thread.join()
