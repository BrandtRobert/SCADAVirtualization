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
            time.sleep(1)
            sensors = self.sensor_bus.get_sensor_readings()
            aux_pressure = sensors['pp_aux_plc'][0]
            watkins_pressure = sensors['pp_watkins_plc'][0]
            cherokee_pressure = sensors['pp_cherokee_plc'][0]
            main_compressor_1_setting = sensors['main_compressor_1_plc'][1]
            main_compressor_2_setting = sensors['main_compressor_2_plc'][1]
            main_compressor_2_p = sensors['main_compressor_2_plc'][0]
            # main_compressor_1 = sum(differences(600, x_i)

            if (main_compressor_2_p + cherokee_pressure + watkins_pressure) == 0:
                continue

            # Mean of the first downstream pressures * 1.5
            pressure_update = \
                1.5 * (((600 - main_compressor_2_p) + (600 - cherokee_pressure) + (600 - watkins_pressure)) / 3)
            new_pressure_setting = int(main_compressor_1_setting + round(pressure_update))
            # print("Updating main compressor pressure ", new_pressure_setting)
            new_pressure_setting = min(800, max(new_pressure_setting, 400))
            self.sensor_bus.update_actuators([('main_compressor_1_plc', new_pressure_setting)])

            # if 0 < aux_pressure < 550 or 0 < cherokee_pressure < 550:
            #     new_pressure_setting = int(min(main_compressor_setting + 25, 800))
            # elif aux_pressure > 625 or cherokee_pressure > 625:
            #     new_pressure_setting = int(max(main_compressor_setting - 25, 400))
            # else: # pressure is normal (550 - 650)
            #     continue
            # print('Pressure out of normal range updating too', new_pressure_setting)


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
