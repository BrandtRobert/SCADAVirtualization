import socket
# from pyModbusTCP.client import ModbusClient

class DeviceInterface:
    """
        DeviceInterface connects to a Pi associated with a physical PLC device
    :return:
    """

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.open_connection(host, port)

    def open_connection(self, host, port):
        server = (host, port)
        self.client_socket.connect(server)

    def close_connection(self):
        self.client_socket.close()

    def request_data_test(self):
        self.client_socket.sendall("gib data plz".encode())
        while True:
            try:
                data = self.client_socket.recv(16).decode()
                print('PLC "data" : ', data)
                return data
            except Exception as e:
                print("Could not receive data, trying again")

    def send_request(self):
        r = input()
        if len(r) < 1:
            print("[!] invalid request")
            print("\tsyntax : [w/r,addr,value/size]")
        elif r.upper() is "EXIT":
            print("[!] disconnecting from server...")
        else:
            self.client_socket.sendall(r.encode())
            try:
                data = self.client_socket.recv(16).decode()
                print('PLC response : ', data)
            except socket.error as e:
                print("[!] could not receive data, try new request")

    # def read_regs(self, start_addr, size):
    #     print("Reading {1} addresses starting at {0}".format(start_addr, size))
    #     return 0
    #
    # def write_regs(self, addr, value):
    #     print("Writing value {1} to address {0}".format(addr, value))
    #     return 0



if __name__ == '__main__':
    obj = DeviceInterface('192.168.0.133', 10001)
    while True:
        obj.send_request()


    #c = ModbusClient()
    # d = obj.request_data_test()
    # print(d)

    # obj.close_connection()
