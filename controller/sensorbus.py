import asyncio
from pymodbus.client.asynchronous import schedulers
from typing import Dict, List
from pymodbus.client.asynchronous.udp \
    import AsyncModbusUDPClient as ModbusClient
from controller.datacollector import DataCollector


class SensorBus:

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

    @staticmethod
    def _parse_registers(registers):
        register_data = []
        for i in range(2, len(registers) + 1, 2):
            r1 = registers[i-2]
            r2 = registers[i-1]
            register_data.append(SensorBus._convert_to_32_float(r1, r2))
        return register_data

    def __init__(self, conf: Dict):
        self.clients = {}
        self.sensors = {}
        self.client_info = {}
        self.register_to_name = {}
        self.data_collector = DataCollector()
        self.started = False
        self._init_sensor_clients(conf)

    def _init_sensor_clients(self, conf: Dict):
        for plc_name, plc_info in conf.items():
            modbus_port = plc_info['modbus_port']
            self.clients[plc_name] = ModbusClient(schedulers.ASYNC_IO, host='localhost', port=modbus_port)[-1].protocol
            self.client_info[plc_name] = plc_info
            self.sensors[plc_name] = {}
            for name, worker in plc_info['workers'].items():
                self.register_to_name[plc_name + "." + str(worker['register'])] = plc_name + '.' + name

    async def _read_sensor(self, name: str, client: ModbusClient):
        num_registers = len(self.client_info[name]['workers'].keys()) * 2
        result = await client.read_holding_registers(0, num_registers)
        registers = SensorBus._parse_registers(result.registers)
        i = 0
        for register in registers:
            self.sensors[name][i] = register
            if self.started:
                sensor_name = self.register_to_name[name + "." + str(i)]
                self.data_collector.collect_data_item(sensor_name, register)
            i = i+2

    async def _update_sensors(self):
        tasks = []
        for plc_name, client in self.clients.items():
            tasks.append(self._read_sensor(plc_name, client))
        await asyncio.gather(*tasks)

    def get_sensor_readings(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._update_sensors())
        return self.sensors

    async def _write_actuator(self, register: int, value: float, client: ModbusClient):
        await client.write_register(register, value)

    async def _write_actuators(self, plc_val: List):
        tasks = []
        for plc_name, register, value in plc_val:
            tasks.append(self._write_actuator(register, value, self.clients[plc_name]))
        await asyncio.gather(*tasks)

    def update_actuators(self, plc_val: List):
        # (plc_name, register, value) --> list of tuples
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._write_actuators(plc_val))

    def get_data_collector(self):
        return self.data_collector
