import threading
# import time
import json
import serial

ser = serial.Serial('/dev/ttyACM0', 115200)

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
            print("Updating shared_data: ", self.data)
            self.shared_data.clear()
            self.shared_data.update(self.data)
        
        self.thread.start()

    def loop(self):
        while self.is_running:
            self.fetchData()

            with self.data_lock:
                self.shared_data.clear()
                self.shared_data.update(self.data)

    def fetchData(self):
        if ser.in_waiting > 0:
            try:
                json_data = ser.readline().decode('utf-8').strip()
                if json_data:
                    self.data = json.loads(json_data)
            except json.JSONDecodeError:
                print("Received bad JSON")

    def stop(self):
        self.is_running = False
        self.thread.join()
