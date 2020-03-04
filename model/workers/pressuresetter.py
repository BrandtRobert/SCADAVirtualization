from model.workers import Worker
import os
import struct


class PressureSetter(Worker):

    def __init__(self, attr, pipe):
        Worker.__init__(self, attr, pipe)
        self.new_update = False
        self.reading = 600

    def run(self, receive_queue):
        pass

    def get_reading(self):
        with self.lock:
            return self.reading

    def set_reading(self, setting):
        with self.lock:
            self.reading = setting
            psi = struct.pack(">d", int(self.reading))
            os.write(self.pipe, psi)
