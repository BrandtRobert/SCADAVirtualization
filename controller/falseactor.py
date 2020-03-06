import time
import yaml
import sys
from model.logger import Logger
from typing import Dict
from pymodbus.client.sync import ModbusUdpClient as ModbusClient


class FalseActor:

    def __init__(self, conf: Dict):
        self.plcs = conf
        self.logger = Logger("ActorLogs", "../model/logger/logs/actors_logs.txt")

    @staticmethod
    def _convert_to_32_float(register1, register2) -> float:
        # Pad hex with 0's
        reg1_hex = hex(register1)[2:]
        if len(reg1_hex) < 4:
            reg1_hex = reg1_hex + ('0' * (4 - len(reg1_hex)))
        reg2_hex = hex(register2)[2:]
        if len(reg2_hex) < 4:
            reg2_hex = reg2_hex + ('0' * (4 - len(reg2_hex)))
        import struct
        hex_bytes = reg1_hex + reg2_hex
        f = struct.unpack('!f', bytes.fromhex(hex_bytes))
        return f[0]

    def parse_registers(self, registers):
        self.logger.debug("Parsing registers {}".format(registers))
        register_data = []
        for i in range(2, len(registers) + 1, 2):
            r1 = registers[i-2]
            r2 = registers[i-1]
            register_data.append(self._convert_to_32_float(r1, r2))
        self.logger.debug("Resulting data: {}".format(register_data))
        return register_data

    def begin_control_loop(self):
        plcs_of_interest = {}
        # Read pressure at PP aux and PP cherokee
        for plc_name, info in self.plcs.items():
            if "cherokee" in plc_name:
                plcs_of_interest['cherokee'] = info
                plcs_of_interest['cherokee']['client'] = ModbusClient('localhost', port=int(info['modbus_port']))
            elif "aux" in plc_name:
                plcs_of_interest['aux'] = info
                plcs_of_interest['aux']['client'] = ModbusClient('localhost', port=int(info['modbus_port']))
            elif "main_compressor_1" in plc_name:
                plcs_of_interest['main_compressor'] = info
                plcs_of_interest['main_compressor']['client'] = ModbusClient('localhost', port=int(info['modbus_port']))
        cherokee_client: ModbusClient = plcs_of_interest['cherokee']['client']
        aux_client: ModbusClient = plcs_of_interest['aux']['client']
        main_compressor_client: ModbusClient = plcs_of_interest['main_compressor']['client']
        self.logger.debug('Starting control loop...')
        while True:
            time.sleep(.200)
            # Read cherokee
            cherokee_registers = self.parse_registers(cherokee_client.read_holding_registers(0, 4).registers)
            self.logger.debug('Reading Cherokee Registers {}'.format(cherokee_registers))
            # Read aux
            aux_registers = self.parse_registers(aux_client.read_holding_registers(0, 4).registers)
            # Read main compressors
            self.logger.debug('Reading Aux Registers {}'.format(aux_registers))
            main_registers = self.parse_registers(main_compressor_client.read_holding_registers(0, 4).registers)
            self.logger.debug('Main Compressor Registers {}'.format(main_registers))
            # First register is pressure
            if 0 < cherokee_registers[0] < 500:
                pressure_setting = main_registers[-1]
                new_setting = min(int(pressure_setting + 100), 1000)
                # pressure_setting = 100
                self.logger.info('Pressure at cherokee low ({} psi) updating output at main compressor to {}'
                                 .format(cherokee_registers[0], new_setting))
                main_compressor_client.write_register(0, new_setting)
            if 0 < aux_registers[0] < 500:
                pressure_setting = main_registers[-1]
                new_setting = min(int(pressure_setting + 100), 1000)
                self.logger.info('Pressure at aux low ({} psi) updating output at main compressor to {}'
                                 .format(aux_registers[0], new_setting))
                main_compressor_client.write_register(0, new_setting)


if __name__ == "__main__":
    fpath = sys.argv[1]
    with open(fpath, 'r') as stream:
        try:
            print('Reading', fpath)
            config_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    falseActor = FalseActor(config_yaml)
    falseActor.begin_control_loop()
