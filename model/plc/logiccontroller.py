from typing import Dict
from model.workers import WorkerFactory
from model.datachannels import modbusencoder, ModbusReceiver, FunctionCodes
from model.logger import Logger
from .plcclock import PLCClock
import threading
import selectors
import socket


class LogicController:
    def __init__(self, name: str, conf: Dict):
        self.plc_name = name
        self.conf = conf
        self.modbus_port = conf['modbus_port']
        self.worker_processes = {}
        self.setup_complete = False
        self.logger = Logger("PLCLogger", "../logger/logs/plc_log.txt", prefix="[{}]".format(self.plc_name))
        self.clock = PLCClock()

    def __str__(self):
        return "{}:\n{}".format(self.plc_name, self.conf)

    def start_plc(self, modbus_port=None):
        if self.setup_complete:
            self.start_workers()
            self.start_modbus_server(modbus_port)
        else:
            self.logger.warning("PLC has not been initialized, rejecting start up")

    def register_workers(self, selector, publish_queue):
        workers_conf = self.conf['workers']
        for worker_name, attr in workers_conf.items():
            # Invoke the factory to create a new worker
            attr['name'] = worker_name
            worker, response_pipe_r = WorkerFactory.create_new_worker(attr)
            if worker is None:
                continue
            # Add the clock to the workers attributes
            attr['clock'] = self.clock
            # If this worker intends to respond to simulink then
            # Link up it's pipe to the main selector
            if response_pipe_r:
                respond_to = (attr['respond_to']['host'], attr['respond_to']['port'])
                selector.register(response_pipe_r, selectors.EVENT_READ,
                                  {"connection_type": "response", "respond_to": respond_to})
            # If this worker intends to listen from simulink data then it should give a port
            # A server socket will be set up for this port in the main selector
            # Data destined to this port will be parsed, packaged, and then sent to listening worker processes
            # using the publish_queue
            if attr.get('port', None):
                serverfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                serverfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                serverfd.bind(('', attr['port']))
                selector.register(serverfd, selectors.EVENT_READ,
                                  {"connection_type": "server_socket", "channel": attr['port']})
            # Unsure whether creation of thread or starting a thread attaches it to the parent ps
            # If there are performance issues in the simulink interface you can investigate this
            p = threading.Thread(target=worker.run, args=(publish_queue.register(attr['port']),))
            self.worker_processes[worker_name] = {
                "process": p,
                "attributes": attr,
                "worker": worker,
            }
            self.logger.info("Setting up worker '{}'".format(worker_name))
        self.setup_complete = True

    def start_workers(self):
        for worker_name, info in self.worker_processes.items():
            self.logger.info("Starting up worker '{}'".format(worker_name))
            info['process'].start()

    def start_modbus_server(self, port=None):
        if port is None:
            port = self.conf['modbus_port']

        ENDIANNESS = 'BIG'

        def handle_request(request):
            #@TODO Based on the request body respond with the appropriate worker information
            request_header = request['header']
            request_body = request['body']
            self.logger.debug("Servicing modbus request {}".format(request_header))
            if request_header['function_code'] == FunctionCodes.WRITE_SINGLE_HOLDING_REGISTER:
                setting = request_body['value']
                # We will have to change this to select worker based on the register
                #    (we need some mapping config file though)
                for worker_name, info in self.worker_processes.items():
                    if "setter" in worker_name:
                        self.logger.info("Setting new pressure reading to {} at {}".format(setting, worker_name))
                        info['worker'].set_reading(setting)
                return modbusencoder.respond_write_registers(request_header, 0, 1, endianness=ENDIANNESS)
            else:
                readings = []
                for worker_name, info in self.worker_processes.items():
                    worker = info['worker']
                    self.logger.info('Retrieving data from {}'.format(worker_name))
                    readings.append((worker.get_reading(), 'FLOAT32'))
                self.logger.info("Responding to request with {}".format(readings))
                return modbusencoder.respond_read_registers(request_header, readings, endianness=ENDIANNESS)

        DEVICE_FUNCTION_CODES = [3, 4, 6, 16]
        modbus_receiver = ModbusReceiver(port, device_function_codes=DEVICE_FUNCTION_CODES,
                                         socket_type=socket.SOCK_DGRAM)
        self.logger.info("Starting modbus server for PLC on {}".format(self.modbus_port))
        modbus_receiver.start_server(handle_request)
