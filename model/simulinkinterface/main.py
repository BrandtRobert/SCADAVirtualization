from model.simulinkinterface import SimulinkInterface
import argparse
import sys

sys.path.insert(0, '/Users/brandt/PycharmProjects/SimulinkInterface')


def parse_args():
    parser = argparse.ArgumentParser(description="A publish subscribe interface for simulink network blocks")
    parser.add_argument("-c", "--config", type=str, help="Path to config yaml file",
                        default="../resources/example_conf_plc.yaml")
    parser.add_argument("-p", "--port", type=int, help="UDP send port for the interface to simulink",
                        default=5000)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print('Initializing simulink interface...')
    interface = SimulinkInterface(args.config, args.port)
    print('Starting simulink interface...')
    interface.start_server()
