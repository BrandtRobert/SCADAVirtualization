from model.workers import *
import os
from model.workers.compromiseworker import CompromiseWorker


class WorkerFactory:

    @staticmethod
    def create_new_worker(attr):
        response_pipe_r = None
        response_pipe_w = None
        worker = None
        if attr.get('respond_to', None):
            response_pipe_r, response_pipe_w = os.pipe()
        if attr['type'] == 'Timer':
            worker = SimulinkTimer(attr, response_pipe_w)
        elif attr['type'] == 'PressureSensor':
            worker = PressureSensor(attr, response_pipe_w)
        elif attr['type'] == 'TemperatureSensor':
            worker = TemperatureSensor(attr, response_pipe_w)
        elif attr['type'] == 'SimulationStopper':
            worker = SimulationStopper(attr, response_pipe_w)
        elif attr['type'] == 'PressureSetter':
            worker = PressureSetter(attr, response_pipe_w)
        else:
            return None
        # wrap compromised workers in a compromise worker class
        if attr.get('compromised', None):
            return CompromiseWorker(worker, attr['compromised']), response_pipe_r
        else:
            return worker, response_pipe_r
