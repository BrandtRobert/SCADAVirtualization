from abc import ABC
from abc import abstractmethod
from typing import Dict
from model.logger import Logger
from threading import RLock
import collections


class Worker(ABC):

    def __init__(self, attr: Dict, pipe: int):
        self.pipe = pipe
        self.lock = RLock()
        self.attributes = attr
        self.started = False
        self.modbus_receiver = None
        self.modbus_thread = None
        self.logger = Logger('WorkerLogger-{}'.format(attr.get('port', 0)), '../logger/logs/worker_log.txt',
                             prefix='Worker Server {}'.format(attr.get('port', 0)))
        self.previous_readings = collections.deque(maxlen=1000)
        self.num_readings = 0

    @abstractmethod
    def run(self, receive_queue):
        pass

    @abstractmethod
    def get_reading(self):
        pass

    def __str__(self):
        return "{}".format(self.attributes)
