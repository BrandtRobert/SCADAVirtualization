import struct
import time
from model.workers import Worker
from collections import deque
from typing import Dict
import os


class SimulinkTimer(Worker):

    def __init__(self, attr: Dict, pipe: int):
        Worker.__init__(self, attr, pipe)
        self.rtts = deque(maxlen=100)
        self.simtime_recent = 0
        self.time_ratio = 0

    def run(self, receive_queue):
        for item in iter(receive_queue.get, None):
            sim_ts, r_ts = item[0], float(item[1])
            self.attributes['clock'].update_time(sim_ts)
            # initial condition
            if r_ts == 0:
                r_ts2 = time.time()
                response = struct.pack(">dd", sim_ts, r_ts2)
                # send a response
                os.write(self.pipe, response)
            else:
                r_ts2 = r_ts
                r_ts3 = time.time()
                # there is some sort of drift in this rtt that is ever increasing...
                rtt = r_ts3 - r_ts2
                self.lock.acquire()
                self.time_ratio = rtt / (sim_ts - self.simtime_recent)
                self.simtime_recent = sim_ts
                self.rtts.append(rtt)
                self.lock.release()
                response = struct.pack(">dd", sim_ts, r_ts3)
                # send a response
                os.write(self.pipe, response)

    def get_reading(self):
        with self.lock:
            return self.simtime_recent
