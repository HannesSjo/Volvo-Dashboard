import threading
import time
import json
import serial
import serial.tools.list_ports


class DataFetcher:
    def __init__(self, data_lock, shared_data):
        self.data_lock = data_lock
        self.shared_data = shared_data
        self.find_arduino_serial()
        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.is_running = True

    def start(self):
        with open('template.json', 'r') as template:
            self.data = json.load(template)
        # with self.data_lock:
        #     print("Updating shared_data: ", self.data)
        #     self.shared_data.clear()
        #     self.shared_data.update(self.data)
        self.thread.start()


    def loop(self):
        while self.is_running:
            self.fetchData()

            with self.data_lock:
                try:
                    self.shared_data.clear()
                    self.shared_data.update(self.data)
                    print("Good: ", self.data)
                except:
                    print("Bad: ", self.data)

            time.sleep(0.2)


    def fetchData(self):
        if self.ser.in_waiting > 0:
            try:
                json_data = self.ser.readline().decode('utf-8').strip()
                if json_data:
                    self.data = json.loads(json_data)
            except json.JSONDecodeError:
                print("Received bad JSON")

    def stop(self):
        self.is_running = False
        self.thread.join()

    def find_arduino_serial(self):
        ports = list(serial.tools.list_ports.comports())

        #for p in ports:
            #if "Arduino" in p.description or (p.manufacturer is not None and "Arduino" in p.manufacturer):
        self.ser = serial.Serial('/dev/ttyACM0', 115200)
