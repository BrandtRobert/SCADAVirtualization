from model.workers import Worker
import os
import struct


class DefaultActuator(Worker):

    def __init__(self, attr, pipe):
        Worker.__init__(self, attr, pipe)
        self.new_update = False
        self.setting = self.attributes.get('default', 0)

    def run(self, receive_queue):
        pass

    def get_reading(self):
        with self.lock:
            return self.setting

    def set_reading(self, setting):
        with self.lock:
            self.setting = setting
            psi = struct.pack(">d", int(self.setting))
            os.write(self.pipe, psi)
