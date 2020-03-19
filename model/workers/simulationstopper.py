from model.workers import Worker
from threading import RLock
import struct
import os


class SimulationStopper(Worker):

    def __init__(self, attr, pipe):
        Worker.__init__(self, attr, pipe)
        self.is_tripped = 1

    def run(self, receive_queue):
        for item in iter(receive_queue.get, None):
            self.attributes['clock'].update_time(item[0])
            with self.lock:
                # Stop firing events after initial trip
                if item[1] == 0 and self.is_tripped == 1:
                    self.logger.warning("ITEM [{}] tripped off... Stopping simulation".format(self.attributes['name']))
                    response = struct.pack(">d", 1)
                    os.write(self.pipe, response)
                    self.is_tripped = 0

    def get_reading(self):
        with self.lock:
            return self.is_tripped

