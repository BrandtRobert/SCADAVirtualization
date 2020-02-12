from .worker import Worker
from threading import Thread, Lock, Event


class PressureSensor(Worker):

    def __init__(self, attr, response_pipe_w):
        Worker.__init__(self, attr, response_pipe_w)
        self.lock = Lock()
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
        self.start_modbus_server(port=self.attributes['modbus_port'])
        for item in iter(receive_queue.get, None):
            self.lock.acquire()
            self.pressure_reading = item[1]
            self.lock.release()
            # print("PS {} received a new message {}".format(self.attributes['name'], item))
        stop_flag.set()

    def get_reading(self):
        with self.lock:
            if self.pressure_reading:
                return self.pressure_reading
            else:
                return 0
