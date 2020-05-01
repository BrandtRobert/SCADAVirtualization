import time
import yaml
import sys
from model.logger import Logger
from typing import Dict
from controller.sensorbus import SensorBus


class ColoradoGasModel:

    def __init__(self, conf: Dict):
        self.sensor_bus = SensorBus(conf)
        self.worker_info = {}
        self.logger = Logger("ActorLogs", "../model/logger/logs/actors_logs.txt")
        self._init_worker_info(conf)

    def _init_worker_info(self, conf):
        for plc, info in conf.items():
            for worker, worker_info in info['workers'].items():
                self.worker_info[plc + '.' + worker] = worker_info

    def _check_and_trip_plant(self, reading, low, high, plc_name, sensor_name):
        if reading < low or reading > high:
            to_write = (plc_name,
                        self.worker_info[plc_name + '.' + sensor_name]['register'],
                        1)
            return to_write
        else:
            return False

    def begin_control_loop(self):
        power_plant_1_tripped = False
        while True:
            time.sleep(.5)
            sensors = self.sensor_bus.get_sensor_readings()
            sim_time = \
                int(sensors['oracle'][self.worker_info['oracle.timer']['register']])

            if sim_time == 0:
                # Sim not started yet
                continue
            else:
                self.sensor_bus.started = True
            if sim_time >= 604800:
                # Simulation has ended
                break

            # power_plant = sensors['pp_fort_collins'][self.worker_info['pp_fort_collins.pressure_sensor']['register']]
            # power_plant_1_pressure = \
            #     sensors['power_plant_1'][self.worker_info['power_plant_1.pressure_sensor']['register']]
            # power_plant_2_pressure = \
            #     sensors['power_plant_2'][self.worker_info['power_plant_2.pressure_sensor']['register']]
            # main_compressor_setting = \
            #     sensors['main_compressor_plc'][self.worker_info['main_compressor_plc.pressure_setter']['register']]
            #
            # actuator_updates = []
            # plant_1_trip = self._check_and_trip_plant(power_plant_1_pressure, 300, 800,
            #                                           'power_plant_1', 'pressure_trip')
            # plant_2_trip = self._check_and_trip_plant(power_plant_2_pressure, 300, 800,
            #                                           'power_plant_2', 'pressure_trip')
            # if plant_1_trip is not False:
            #     actuator_updates.append(plant_1_trip)
            # if plant_2_trip is not False:
            #     actuator_updates.append(plant_2_trip)
            #
            # # Mean of the first downstream pressures * 1.5
            # pressure_update = 1.5 * ((600 - power_plant_1_pressure) + (600 - power_plant_2_pressure))
            # new_pressure_setting = int(main_compressor_setting + round(pressure_update))
            # new_pressure_setting = min(800, max(new_pressure_setting, 400))
            # # print("Updating main compressor pressure ", new_pressure_setting)
            # pressure_setting_update = ('main_compressor_plc',
            #                            self.worker_info['main_compressor_plc.pressure_setter']['register'],
            #                            new_pressure_setting)
            # actuator_updates.append(pressure_setting_update)
            # self.sensor_bus.update_actuators(actuator_updates)

        print("Attempting to graph results....")
        data_collector = self.sensor_bus.get_data_collector()
        data_collector.add_to_plot('pp_fort_collins.pressure_sensor', 'oracle.timer')
        data_collector.add_to_plot('pp_denver.temperature_sensor', 'oracle.timer')
        data_collector.add_to_plot('pp_colorado_springs.pressure_sensor', 'oracle.timer')
        data_collector.add_to_plot('pp_cheyenne_wells.pressure_sensor', 'oracle.timer')
        # data_collector.add_to_plot('oracle.main_plant_pressure', 'oracle.timer')
        # data_collector.add_to_plot('oracle.main_plant_temperature', 'oracle.timer')
        data_collector.show_plot('Sensor Reading Over Time',
                                 save_as='coloradoGasModelPressure.png',
                                 ylabel='Pressure Reading (PSI)',
                                 legend_labels=['Plant 1 Pressure', 'Plant 1 Temperature',
                                                'Plant 2 Pressure', 'Plant 2 Temperature'])


if __name__ == "__main__":
    fpath = sys.argv[1]
    with open(fpath, 'r') as stream:
        try:
            print('Reading', fpath)
            config_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    falseActor = ColoradoGasModel(config_yaml)
    falseActor.begin_control_loop()
