import selectors
import yaml
import socket
from datachannels import PublishQueue
from workers import PressureSensor, SimulinkTimer
import multiprocessing
import os
import struct


class SimulinkInterface:
    def __init__(self, config_path):
        self.processes = []
        self.config = self.read_config(config_path)
        self.selector = selectors.DefaultSelector()
        self.publish_queue = PublishQueue()
        self.udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def read_config(self, config_path):
        with open(config_path, 'r') as stream:
            try:
                config_yaml = yaml.safe_load(stream)['sockets']
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)
        return config_yaml

    def create_workers(self):
        for name, attr in self.config.items():
            attr['name'] = name
            # serverfd.listen(5)
            response_pipe_r = None
            response_pipe_w = None
            respond_to = None
            if attr.get('respond_to', None):
                response_pipe_r, response_pipe_w = os.pipe()
                respond_to = (attr['respond_to']['host'], attr['respond_to']['port'])
            worker = None
            if attr['type'] == "PressureSensor":
                worker = PressureSensor(attr, response_pipe_w)
            if attr['type'] == "Timer":
                worker = SimulinkTimer(attr, response_pipe_w)
            if worker:
                if response_pipe_r:
                    self.selector.register(response_pipe_r, selectors.EVENT_READ, {"connection_type": "response",
                                                                                   "respond_to": respond_to})
                channel_id = None
                if attr.get('port', None):
                    serverfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    serverfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    serverfd.bind(('', attr['port']))
                    self.selector.register(serverfd, selectors.EVENT_READ, {"connection_type": "server_socket",
                                                                            "channel": attr['port']})
                    channel_id = attr['port']
                p = multiprocessing.Process(target=worker.run, args=(self.publish_queue.register(channel_id),))
                self.processes.append(p)
            print("Initializing process: {}".format(self.config[name]))

    def _accept_connection(self, sock: socket.socket):
        conn, addr = sock.accept()
        print("New connection from {}".format(addr))
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ, {"connection_type": "client_connection",
                                                            "channel": addr[1]})

    def _read_and_publish(self, connection: socket, channel: str):
        """
        |--- 64 bit simulation time --|
        |--- 64 bit reading         --|
        """
        data = connection.recv(16)  # Should be ready
        if data:
            sim_time, reading = struct.unpack(">dd", data)
            sim_time = int(sim_time)
            self.publish_queue.publish((sim_time, reading), channel)
        else:
            print('closing', connection)
            self.selector.unregister(connection)
            connection.close()

    def _send_response(self, read_pipe, host: str, port: int):
        response_data = os.read(read_pipe, 128)
        self.udp_send_socket.sendto(response_data, (host, port))

    def service_connection(self, key):
        connection = key.fileobj
        connection_type = key.data['connection_type']
        if connection_type == 'server_socket':
        #     self._accept_connection(connection)
        # if connection_type == 'client_connection':
            channel = key.data['channel']
            self._read_and_publish(connection, channel)
        if connection_type == 'response':
            read_pipe = key.fileobj
            host, port = key.data['respond_to']
            self._send_response(read_pipe, host, port)

    def start_server(self):
        self.create_workers()
        for p in self.processes:
            p.start()

        while True:
            events = self.selector.select()
            for key, mask in events:
                self.service_connection(key)
