import time
import yaml
import sys
from model.logger import Logger
from typing import Dict
from controller.sensorbus import SensorBus


class Experiment1:

    def __init__(self, conf: Dict):
        self.sensor_bus = SensorBus(conf)
        self.worker_info = {}
        self.logger = Logger("ActorLogs", "../model/logger/logs/actors_logs.txt")
        self._init_worker_info(conf)

    def _init_worker_info(self, conf):
        for plc, info in conf.items():
            for worker, worker_info in info['workers'].items():
                self.worker_info[plc + '.' + worker] = worker_info

    def begin_control_loop(self):
        main_power_plant_tripped = False
        while True:
            time.sleep(.5)
            sensors = self.sensor_bus.get_sensor_readings()
            sim_time = \
                int(sensors['oracle'][self.worker_info['oracle.timer']['register']])
            if sim_time > 0:
                self.sensor_bus.started = True
            main_plant_pressure = \
                sensors['main_power_plant'][self.worker_info['main_power_plant.pressure_sensor']['register']]
            main_compressor_setting = \
                sensors['main_compressor_plc'][self.worker_info['main_compressor_plc.pressure_setter']['register']]
            if sim_time >= 604800:
                break

            if main_plant_pressure == 0:
                continue
            elif (main_plant_pressure < 300 or main_plant_pressure > 800) and not main_power_plant_tripped:
                to_write = ('main_power_plant',
                            self.worker_info['main_power_plant.pressure_trip']['register'],
                            1)
                # print("Main power plant tripped: {}".format(to_write))
                self.sensor_bus.update_actuators([to_write])
                # main_power_plant_tripped = True
            else:
                # Mean of the first downstream pressures * 1.5
                pressure_update = 1.5 * (600 - main_plant_pressure)
                new_pressure_setting = int(main_compressor_setting + round(pressure_update))
                # print("Updating main compressor pressure ", new_pressure_setting)
                new_pressure_setting = min(800, max(new_pressure_setting, 400))
                to_write = ('main_compressor_plc',
                            self.worker_info['main_compressor_plc.pressure_setter']['register'],
                            new_pressure_setting)
                self.sensor_bus.update_actuators([to_write])
        print("Attempting to graph results....")
        data_collector = self.sensor_bus.get_data_collector()
        data_collector.add_to_plot('main_power_plant.pressure_sensor', 'oracle.timer')
        data_collector.add_to_plot('main_power_plant.temperature_sensor', 'oracle.timer')
        data_collector.add_to_plot('oracle.main_plant_pressure', 'oracle.timer')
        # data_collector.add_to_plot('oracle.main_plant_temperature', 'oracle.timer')
        data_collector.show_plot('Change in Pressure Over Time',
                                    ylabel='Pressure Reading (PSI)',
                                    legend_labels=['compromised plant pressure', 'real plant temperature',
                                                   'real plant pressure'])


if __name__ == "__main__":
    fpath = sys.argv[1]
    with open(fpath, 'r') as stream:
        try:
            print('Reading', fpath)
            config_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    falseActor = Experiment1(config_yaml)
    falseActor.begin_control_loop()
