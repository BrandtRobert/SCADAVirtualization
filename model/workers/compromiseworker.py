from model.workers import Worker
from typing import Dict
import time


class CompromiseWorker(Worker):
    """
        Execute the worker compromises. Get the actual reading and then modify it.
        The Compromised Worker also tracks previous readings so that you can delay the sensor readings.
        hold_back: is how many readings back a value should be delayed.
        reading: specifies an equation for how to modify the reading (if hold_back > 0)
                    then you are modifying the reading. In this equation x is the original reading value.
    """
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
        # print("Time difference at: {} waiting for: {}".format(time.time() - self.start_time, self.activate_at))
        sim_time = self.attributes['clock'].get_time()
        if sim_time > self.activate_at and self.worker.num_readings > self.conf.get('hold_back', 0):
            i = self.conf.get('hold_back', 0)
            delayed_reading = self.worker.previous_readings[-(i+1)]
            f = lambda x: eval(self.conf.get('reading', 'x'))
            new_reading = f(delayed_reading)
            print("Compromise new reading", reading, new_reading)
            return new_reading
        else:
            return reading
