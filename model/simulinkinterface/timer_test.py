from model.simulinkinterface import SimulationTimeOracle
import threading
import time

if __name__ == "__main__":
    oracle = SimulationTimeOracle(6068, 6065)
    p = threading.Thread(target=oracle.start)
    p.start()
    while True:
        time.sleep(2)
        print('Current sim time', SimulationTimeOracle.get_sim_time())
        print('Other way to check', SimulationTimeOracle.CURRENT_SIM_TIME)
