import socket
from threading import RLock, Event
import time
import struct


class SimulationTimeOracle:

    CURRENT_SIM_TIME = 0
    LOCK = RLock()

    def __init__(self, _receive_port, _respond_port, socket_type = socket.SOCK_DGRAM):
        self.sock_type = socket_type
        self.receive_socket = socket.socket(socket.AF_INET, socket_type)
        self.receive_socket.bind(('', _receive_port))
        self.simtime_recent = 0
        self.time_ratio = 0
        self.stopped = Event()
        self._respond_port = _respond_port

    def start(self):
        while not self.stopped.is_set():
            data = self.receive_socket.recv(16)
            sim_ts, r_ts = struct.unpack(">dd", data)
            # initial condition
            if r_ts == 0:
                r_ts2 = time.time()
                response = struct.pack(">dd", sim_ts, r_ts2)
                # send a response
                self.receive_socket.sendto(response, ('localhost', self._respond_port))
            else:
                r_ts2 = r_ts
                r_ts3 = time.time()
                # there is some sort of drift in this rtt that is ever increasing...
                rtt = r_ts3 - r_ts2
                with SimulationTimeOracle.LOCK:
                    self.time_ratio = rtt / (sim_ts - self.simtime_recent)
                    self.simtime_recent = sim_ts
                    SimulationTimeOracle.CURRENT_SIM_TIME = sim_ts
                response = struct.pack(">dd", sim_ts, r_ts3)
                # send a response
                self.receive_socket.sendto(response, ('localhost', self._respond_port))

    def stop(self):
        self.stopped.set()
        # to break out of a blocking receive call
        s = socket.socket(socket.AF_INET, self.sock_type)
        s.send(struct.pack(">dd", 0, 0))

    @staticmethod
    def get_sim_time():
        with SimulationTimeOracle.LOCK:
            return SimulationTimeOracle.CURRENT_SIM_TIME
