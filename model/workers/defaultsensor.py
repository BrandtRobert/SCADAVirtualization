from .worker import Worker
from threading import Event, Thread


class DefaultSensor(Worker):

    def __init__(self, attr, response_pipe_w):
        Worker.__init__(self, attr, response_pipe_w)
        self.reading = self.attributes.get('default', None)
        self.units = self.attributes.get('units', '')

    def run(self, receive_queue):
        stop_flag = self.print_pressure_reading()
        for item in iter(receive_queue.get, None):
            self.started = True
            self.attributes['clock'].update_time(item[0])
            with self.lock:
                self.num_readings = self.num_readings + 1
                self.previous_readings.append(item[1])
                self.reading = item[1]
        stop_flag.set()

    def print_pressure_reading(self):
        stopped = Event()

        def pp():
            # the first call is in `interval` secs
            while not stopped.wait(1.5):
                self.lock.acquire()
                if self.reading is not None:
                    # print("Pressure Reading \"{}\": {:.2f} psi".format(self.attributes['name'],
                    #                                              self.pressure_reading))
                    self.logger.info("Pressure Reading \"{}\": {:.2f}".format(self.attributes['name'],
                                                                                  self.reading))
                self.lock.release()
        Thread(target=pp, daemon=True).start()
        return stopped

    def get_reading(self):
        with self.lock:
            if self.reading:
                return self.reading
            else:
                return 0
