from abc import ABC
from abc import abstractmethod
from model.datachannels import ModbusReceiver
from model.datachannels import modbusencoder
from typing import Dict
from model.logger import Logger
from threading import RLock


class Worker(ABC):

    def __init__(self, attr: Dict, pipe: int):
        self.pipe = pipe
        self.lock = RLock()
        self.attributes = attr
        self.modbus_receiver = None
        self.modbus_thread = None
        self.logger = Logger('WorkerLogger-{}'.format(attr['port']), '../logger/logs/worker_log.txt',
                             prefix='Worker Server {}'.format(attr['port']))

    @abstractmethod
    def run(self, receive_queue):
        pass

    @abstractmethod
    def get_reading(self):
        pass

    def __str__(self):
        return "{}".format(self.attributes)
