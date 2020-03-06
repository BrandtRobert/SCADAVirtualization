from model.workers import Worker
from typing import Dict
import time


class CompromiseWorker(Worker):

    def __init__(self, worker: Worker, config: Dict):
        print("Creation of new compromised worker... {}".format(worker))
        super().__init__(worker.attributes, worker.pipe)
        self.activate_at = config['after']
        self.worker = worker
        self.conf = config
        self.start_time = 0

    def run(self, receive_queue):
        self.worker.run(receive_queue)

    def get_reading(self):
        # begin the compromise timer after the first reading
        if not self.worker.started:
            self.start_time = time.time()
        actual_reading = self.worker.get_reading()
        return self._compromise_reading(actual_reading)

    def _compromise_reading(self, reading):
        compromise_type = self.conf['reading']
        print("Time difference at: {} waiting for: {}".format(time.time() - self.start_time, self.activate_at))
        if time.time() - self.start_time > self.activate_at:
            print("Compromise triggered new reading: {}".format(compromise_type))
            new_reading = compromise_type
            return new_reading
        else:
            return reading
