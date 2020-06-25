from typing import Dict
from model.workers import WorkerFactory
from model.datachannels import modbusencoder, ModbusReceiver, FunctionCodes
from model.logger import Logger
from .plcclock import PLCClock
import threading
import selectors
import socket


"""
    WARNING: a fatal flaw has been discovered in the design of the virtual PLCs and their
        interactions with the simulink interface. Spawning processes which already have thread
        objects can lead to undefined behavior. This will lead to a unique error where the 
        system will fail to run in windows. The reason the system works on unix based systems is
        the difference between forking and spawning a process. Unix systems will fork processes in 
        the python multi-processing module. This means that all the state of the current running process
        is inherited by the new forked process (it is a clone). The state of thread objects is 'unpicklable'
        so when spawning a process (the behavior in windows) the process will fail as it is not able to transfer
        the data pertaining to threads contained in the virtual plc.
        
    SOLUTIONS?: likely solutions could include:
        - instead of creating threads for each worker, have a single PLC process handle all the workers in 1 thread
            or spawn new threads as needed after the PLC process has been created
        - alternatively you could find a way to spin up threads after the PLC has been created
            * one possibility is a nested publish subscribe situation
            * each virtual plc takes data from the select server for each work contained in it
                the virtual plc then dispatches new data to its respective workers based on the port (data channel)
                new info is received on. This would require a thread to thread communication mechanism in the 
                virtual PLC.
"""

class LogicController:
    def __init__(self, name: str, conf: Dict):
        self.plc_name = name
        self.conf = conf
        self.modbus_port = conf['modbus_port']
        self.worker_processes = {}
        self.setup_complete = False
        self.logger = Logger("PLCLogger", "../logger/logs/plc_log.txt", prefix="[{}]".format(self.plc_name))
        self.clock = PLCClock()
        self.register_map = {}

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
            port = 0
            if attr.get('port', None):
                port = attr['port']
                serverfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                serverfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                serverfd.bind(('', attr['port']))
                selector.register(serverfd, selectors.EVENT_READ,
                                  {"connection_type": "server_socket", "channel": attr['port']})
                # Unsure whether creation of thread or starting a thread attaches it to the parent ps
                # If there are performance issues in the simulink interface you can investigate this
            channel = attr.get('channel', port)
            p = threading.Thread(target=worker.run, args=(publish_queue.register(channel),))
            self.worker_processes[worker_name] = {
                "process": p,
                "attributes": attr,
                "worker": worker,
            }
            self.register_map[int(attr['register'])] = worker
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
            request_header = request['header']
            request_body = request['body']
            self.logger.debug("Servicing modbus request {}".format(request_header))
            start_register = request_body['address']
            if request_header['function_code'] == FunctionCodes.WRITE_SINGLE_HOLDING_REGISTER:
                setting = request_body['value']
                worker = self.register_map.get(start_register, None)
                if worker:
                    if hasattr(worker, 'set_reading'):
                        worker.set_reading(setting)
                        self.logger.info("Setting new pressure reading to {} at {}"
                                 .format(setting, worker.attributes['name']))
                return modbusencoder.respond_write_registers(request_header, 0, 1, endianness=ENDIANNESS)
            else:
                readings = []
                register_count = request_body['count']
                for current_reg in range(start_register, register_count, 2):
                    worker = self.register_map.get(current_reg, None)
                    if worker:
                        self.logger.info('Retrieving data from {}'.format(worker.attributes['name']))
                        readings.append((worker.get_reading(), 'FLOAT32'))
                self.logger.info("Responding to request with {}".format(readings))
                return modbusencoder.respond_read_registers(request_header, readings, endianness=ENDIANNESS)

        DEVICE_FUNCTION_CODES = [3, 4, 6, 16]
        modbus_receiver = ModbusReceiver(port, device_function_codes=DEVICE_FUNCTION_CODES,
                                         socket_type=socket.SOCK_DGRAM)
        self.logger.info("Starting modbus server for PLC on {}".format(self.modbus_port))
        modbus_receiver.start_server(handle_request)
