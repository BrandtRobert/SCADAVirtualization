from workers import Worker
from threading import Lock
import struct
import os


class SimulationStopper(Worker):

    def __init__(self, attr, pipe):
        Worker.__init__(self, attr, pipe)
        self.is_tripped = 0
        self.stop_lock = Lock()

    def run(self, receive_queue):
        for item in iter(receive_queue.get, None):
            print("Item {} received data".format(self.attributes['name']))
            with Lock:
                self.is_tripped = item[1]
                if self.is_tripped:
                    print("Item {} tripped off".format(self.attributes['name']))
                    response = struct.pack(">d", 1)
                    os.write(self.pipe, response)

    def get_reading(self):
        with Lock:
            return self.is_tripped

