from model.workers import *


class WorkerFactory:

    @staticmethod
    def create_new_worker(attr, response_pipe_w):
        if attr['type'] == 'Timer':
            return SimulinkTimer(attr, response_pipe_w)
        elif attr['type'] == 'PressureSensor':
            return PressureSensor(attr, response_pipe_w)
        elif attr['type'] == 'TemperatureSensor':
            return TemperatureSensor(attr, response_pipe_w)
        elif attr['type'] == 'SimulationStopper':
            return SimulationStopper(attr, response_pipe_w)
        elif attr['type'] == 'PressureSetter':
            return PressureSetter(attr, response_pipe_w)
        else:
            return None
