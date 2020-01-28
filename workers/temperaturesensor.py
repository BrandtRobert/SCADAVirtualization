from .worker import Worker
from threading import Thread, Lock, Event


class TemperatureSensor(Worker):

    def __init__(self, attr, response_pipe_w):
        Worker.__init__(self, attr, response_pipe_w)
        self.lock = Lock()
        self.temperature_reading = None

    def print_temperature_reading(self):
        stopped = Event()

        def pp():
            # the first call is in `interval` secs
            while not stopped.wait(1.5):
                self.lock.acquire()
                if self.temperature_reading is not None:
                    print("Pressure Reading \"{}\": {:.2f} mPA".format(self.attributes['name'],
                                                                       self.temperature_reading / 10 ** 6))
                self.lock.release()

        Thread(target=pp, daemon=True).start()
        return stopped

    def run(self, receive_queue):
        stop_flag = self.print_temperature_reading()
        self.start_modbus_server(port=self.attributes['modbus_port'])
        for item in iter(receive_queue.get, None):
            self.lock.acquire()
            self.temperature_reading = item[1]
            self.lock.release()
            # print("PS {} received a new message {}".format(self.attributes['name'], item))
        stop_flag.set()

    def get_reading(self):
        if self.temperature_reading:
            return self.temperature_reading
        else:
            return 0
