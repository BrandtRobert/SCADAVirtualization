import time
import yaml
import sys
from model.logger import Logger
from typing import Dict
from controller.sensorbus import SensorBus


class FalseActor:

    def __init__(self, conf: Dict):
        self.sensor_bus = SensorBus(conf)
        self.logger = Logger("ActorLogs", "../model/logger/logs/actors_logs.txt")

    def begin_control_loop(self):
        while True:
            time.sleep(.1)
            sensors = self.sensor_bus.get_sensor_readings()
            aux_pressure = sensors['pp_aux_plc'][0]
            cherokee_pressure = sensors['pp_cherokee_plc'][0]
            main_compressor_setting = sensors['main_compressor_1_plc'][0]
            if 0 < aux_pressure < 550 or 0 < cherokee_pressure < 550:
                new_pressure_setting = int(min(main_compressor_setting + 25, 800))
            elif aux_pressure > 625 or cherokee_pressure > 625:
                new_pressure_setting = int(max(main_compressor_setting - 25, 400))
            else: # pressure is normal (550 - 650)
                continue
            # print('Pressure out of normal range updating too', new_pressure_setting)
            self.sensor_bus.update_actuators([('main_compressor_1_plc', new_pressure_setting)])

        # if 0 < cherokee_registers[0] < 500:
            #     pressure_setting = main_registers[-1]
            #     new_setting = min(int(pressure_setting + 100), 1000)
            #     # pressure_setting = 100
            #     self.logger.info('Pressure at cherokee low ({} psi) updating output at main compressor to {}'
            #                      .format(cherokee_registers[0], new_setting))
            #     main_compressor_client.write_register(0, new_setting)
            # if 0 < aux_registers[0] < 500:
            #     pressure_setting = main_registers[-1]
            #     new_setting = min(int(pressure_setting + 100), 1000)
            #     self.logger.info('Pressure at aux low ({} psi) updating output at main compressor to {}'
            #                      .format(aux_registers[0], new_setting))
            #     main_compressor_client.write_register(0, new_setting)


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
