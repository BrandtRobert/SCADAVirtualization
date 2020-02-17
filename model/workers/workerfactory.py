from model.workers import *
import os


class WorkerFactory:

    @staticmethod
    def create_new_worker(attr):
        response_pipe_r = None
        response_pipe_w = None
        if attr.get('respond_to', None):
            response_pipe_r, response_pipe_w = os.pipe()

        if attr['type'] == 'Timer':
            return SimulinkTimer(attr, response_pipe_w), response_pipe_r
        elif attr['type'] == 'PressureSensor':
            return PressureSensor(attr, response_pipe_w), response_pipe_r
        elif attr['type'] == 'TemperatureSensor':
            return TemperatureSensor(attr, response_pipe_w), response_pipe_r
        elif attr['type'] == 'SimulationStopper':
            return SimulationStopper(attr, response_pipe_w), response_pipe_r
        elif attr['type'] == 'PressureSetter':
            return PressureSetter(attr, response_pipe_w), response_pipe_r
        else:
            return None
