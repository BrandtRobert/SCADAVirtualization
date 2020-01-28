import struct
import time
from workers import Worker
from threading import Thread, Event, Lock
from collections import deque
from typing import Dict
import os
import numpy as np


class SimulinkTimer(Worker):

    def __init__(self, attr: Dict, pipe: int):
        Worker.__init__(self, attr, pipe)
        self.rtts = deque(maxlen=100)
        self.dl = Lock()

    def run(self, receive_queue):
        stop_flag = self.print_data()
        for item in iter(receive_queue.get, None):
            sim_ts, r_ts = item[0], int(item[1])
            # initial condition
            if r_ts == 0:
                r_ts2 = time.time()
                response = struct.pack(">dd", sim_ts, r_ts2)
                # send a response
                os.write(self.pipe, response)
            else:
                r_ts2 = r_ts
                r_ts3 = time.time()
                rtt = r_ts3 - r_ts2
                self.dl.acquire()
                self.rtts.append(rtt)
                self.dl.release()
                response = struct.pack(">dd", sim_ts, r_ts3)
                # send a response
                os.write(self.pipe, response)
        stop_flag.set()

    def print_data(self):
        stopped = Event()

        def pp():
            # the first call is in `interval` secs
            while not stopped.wait(1):
                self.dl.acquire()
                if len(self.rtts) > 2:
                    # print(np.random.choice(self.rtts, (50, )))
                    avg_rtt = sum(self.rtts)/len(self.rtts) * (10**2)
                    print("Mean RTT: {:2f}ms".format(avg_rtt))
                self.dl.release()
        Thread(target=pp, daemon=True).start()
        return stopped.set

    def get_reading(self):
        return 0