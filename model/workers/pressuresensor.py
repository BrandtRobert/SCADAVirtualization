from .worker import Worker
from threading import Thread, Event


class PressureSensor(Worker):

    def __init__(self, attr, response_pipe_w):
        Worker.__init__(self, attr, response_pipe_w)
        self.pressure_reading = None

    def print_pressure_reading(self):
        stopped = Event()

        def pp():
            # the first call is in `interval` secs
            while not stopped.wait(1.5):
                self.lock.acquire()
                if self.pressure_reading is not None:
                    # print("Pressure Reading \"{}\": {:.2f} psi".format(self.attributes['name'],
                    #                                              self.pressure_reading))
                    self.logger.info("Pressure Reading \"{}\": {:.2f} psi".format(self.attributes['name'],
                                                                                  self.pressure_reading))
                self.lock.release()

        Thread(target=pp, daemon=True).start()
        return stopped

    def run(self, receive_queue):
        stop_flag = self.print_pressure_reading()
        for item in iter(receive_queue.get, None):
            with self.lock:
                self.pressure_reading = item[1]
        stop_flag.set()

    def get_reading(self):
        with self.lock:
            if self.pressure_reading:
                return self.pressure_reading
            else:
                return 0
