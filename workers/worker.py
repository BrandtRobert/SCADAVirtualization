from abc import ABC
from abc import abstractmethod
from datachannels import ModbusReceiver, modbusencoder
from typing import Dict
import socket
import threading


class Worker(ABC):

    def __init__(self, attr: Dict, pipe: int):
        self.pipe = pipe
        self.attributes = attr
        self.modbus_receiver = None
        self.modbus_thread = None

    @abstractmethod
    def run(self, receive_queue):
        pass

    @abstractmethod
    def get_reading(self):
        pass

    def start_modbus_server(self, port):
        """
            Should be invoked by child class most of the time,
            port specification allows to configure ports for each worker.
            :param port: the port for the worker to listen for modbus requests
        """
        ENDIANNESS = 'BIG'

        def handle_request(request):
            request_header = request['header']
            request_body = request['body']
            print('received request:{}'.format(request_body))
            print('Sending reading:{}'.format(self.get_reading()))
            return modbusencoder.respond_read_registers(request_header, [(float(self.get_reading()), 'FLOAT32')],
                                                 endianness=ENDIANNESS)
        DEVICE_FUNCTION_CODES = [3, 4, 6, 16]
        self.modbus_receiver = ModbusReceiver(port, device_function_codes=DEVICE_FUNCTION_CODES,
                                              socket_type=socket.SOCK_DGRAM)
        self.modbus_thread = threading.Thread(target=self.modbus_receiver.start_server, args=(handle_request,),
                                              daemon=True)
        self.modbus_thread.start()
