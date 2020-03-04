from typing import Dict, Callable
from model.datachannels import ModbusReceiver, modbusencoder
from socket import SOCK_STREAM, SOCK_DGRAM
from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from time import sleep
from threading import Thread
import random


class FakePLC:
    """
        Fake PLC for testing the frontend. This is a PLC that can run a modbus server as either TCP or UDP.
            - the example reading structure is just one way of specifying how you want readings to be returned,
              this module is mainly for testing and returning some set of feasible values.
    """
    example_reading_structure = {
        'pressure': {
            'binary': False,
            'mean_value': 600,
            'noise_range': 50,
            'always_positive': False
        },
        'temperature': {
            'binary': False,
            'mean_value': 60,
            'noise_range': 5,
            'always_positive': False
        },
        'on_off': {
            'binary': True,
            'mean_value': 0,
            'probability': .1
        }
    }

    def __init__(self, modbus_port: int, reading_structure: Dict, tcp: bool = False,
                 request_handler_override: Callable = None):
        """
        :param modbus_port: the port to run the modbus server
        :param reading_structure: sampling information for returning random data
        :param tcp: whether to run the server as tcp or not, false by default
        :param request_handler_override: if you would like to implement your on functionality on request pass a callable
                function that takes the parameter response: {'header': Dict, 'body': Dict}
        """
        self.modbus_port = modbus_port
        self.reading_structure = reading_structure
        self.tcp = tcp
        self.request_handler_override = request_handler_override

    def get_random_reading(self, reading_name):
        """
            Gets a random reading based on the data in the reading structure.
        """
        reading_attributes = self.reading_structure[reading_name]
        if not reading_attributes['binary']:
            mean_value = reading_attributes['mean_value']
            noise_range = reading_attributes['noise_range']
            always_positive = reading_attributes['always_positive']
            noise = random.randrange(0, noise_range) if always_positive else random.randrange(-noise_range, noise_range)
            return mean_value + noise
        else:
            default = reading_attributes['mean_value']
            prob = reading_attributes['probability']
            if random.random() < prob:
                if default == 0:
                    return 1
                else:
                    return 0
            else:
                return default

    def request_handler(self, response):
        if self.request_handler_override:
            return self.request_handler_override(response)
        req_header = response['header']
        req_body = response['body']
        print('Received request {}'.format(req_header))
        readings = []
        for reading_name in self.reading_structure.keys():
            reading = self.get_random_reading(reading_name)
            print('Returning random reading for {}...{}'.format(reading_name, reading))
            readings.append((float(reading), 'FLOAT32'))
        return modbusencoder.respond_read_registers(req_header, readings)

    def start_server(self):
        socket_type = SOCK_STREAM if self.tcp else SOCK_DGRAM
        server = ModbusReceiver(self.modbus_port, socket_type=socket_type)
        server.start_server(self.request_handler)


if __name__ == "__main__":
    example_reading_structure = {
        'pressure': {
            'binary': False,
            'mean_value': 600,
            'noise_range': 50,
            'always_positive': False
        },
        'temperature': {
            'binary': False,
            'mean_value': 60,
            'noise_range': 5,
            'always_positive': False
        },
        'on_off': {
            'binary': True,
            'mean_value': 0,
            'probability': .1
        }
    }
    fakePLC = FakePLC(8080, example_reading_structure)
    # Modbus UDP client from pymodbus package
    client = ModbusClient('localhost', port=8080)
    plcThread = Thread(target=fakePLC.start_server, daemon=True)
    plcThread.start()
    client.connect()
    while True:
        try:
            sleep(2)
            response = client.read_holding_registers(0, 3)
            print('Response registers:', response.registers)
        except KeyboardInterrupt:
            print('Quiting...')
            exit(0)
