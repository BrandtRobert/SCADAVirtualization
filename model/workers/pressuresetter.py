from model.workers import Worker
import os
import struct


class PressureSetter(Worker):

    def __init__(self, attr, pipe):
        Worker.__init__(self, attr, pipe)

    def run(self, receive_queue):
        while True:
            psi = input("Enter psi")
            psi = struct.pack(">d", int(psi))
            os.write(self.pipe, psi)

    def get_reading(self):
        pass

