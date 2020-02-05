from simulinkinterface import SimulinkInterface
import argparse
import sys

sys.path.insert(0, '/Users/brandt/PycharmProjects/SimulinkInterface')


def parse_args():
    parser = argparse.ArgumentParser(description="A publish subscribe interface for simulink network blocks")
    parser.add_argument("-c", "--config", type=str, help="Path to config yaml file",
                        default="../resources/simulinkconf.yaml")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    interface = SimulinkInterface(args.config)
    interface.start_server()

