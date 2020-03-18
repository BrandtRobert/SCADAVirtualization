from threading import RLock


class PLCClock:
    def __init__(self):
        self.time = 0
        self.lock = RLock()

    def update_time(self, new_time):
        with self.lock:
            self.time = max(self.time, new_time)

    def get_time(self):
        with self.lock:
            return self.time

    def reset_clock(self):
        with self.lock:
            self.time = 0
