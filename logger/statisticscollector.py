from threading import RLock
import json


class StatisticsCollector:

    packets_received = 0
    responses_sent = 0
    error_packets_sent = 0
    socket_errors = 0
    number_of_devices = 0
    avg_response_time = 0
    number_of_terms_in_mean = 0
    lock = RLock()

    # def __init__(StatisticsCollector):
    #     StatisticsCollector.packets_received = 0
    #     StatisticsCollector.responses_sent = 0
    #     StatisticsCollector.error_packets_sent = 0
    #     StatisticsCollector.socket_errors = 0
    #     StatisticsCollector.number_of_devices = 0
    #     StatisticsCollector.avg_response_time = 0
    #     StatisticsCollector.number_of_terms_in_mean = 0
    #     StatisticsCollector.lock = RLock()
    @staticmethod
    def increment_packets_received():
        with StatisticsCollector.lock:
            StatisticsCollector.packets_received = StatisticsCollector.packets_received + 1

    @staticmethod
    def get_packets_received():
        with StatisticsCollector.lock:
            return StatisticsCollector.packets_received

    @staticmethod
    def increment_responses_sent():
        with StatisticsCollector.lock:
            StatisticsCollector.responses_sent = StatisticsCollector.responses_sent + 1

    @staticmethod
    def get_responses_sent():
        with StatisticsCollector.lock:
            return StatisticsCollector.responses_sent

    @staticmethod
    def increment_error_packets_sent():
        with StatisticsCollector.lock:
            StatisticsCollector.error_packets_sent = StatisticsCollector.error_packets_sent + 1

    @staticmethod
    def get_error_packets_sent():
        with StatisticsCollector.lock:
            return StatisticsCollector.error_packets_sent

    @staticmethod
    def increment_socket_errors():
        with StatisticsCollector.lock:
            StatisticsCollector.socket_errors = StatisticsCollector.socket_errors + 1

    @staticmethod
    def get_socket_errors():
        with StatisticsCollector.lock:
            return StatisticsCollector.socket_errors

    @staticmethod
    def increment_number_of_devices():
        with StatisticsCollector.lock:
            StatisticsCollector.number_of_devices = StatisticsCollector.number_of_devices + 1

    @staticmethod
    def get_number_devices():
        with StatisticsCollector.lock:
            return StatisticsCollector.number_of_devices

    @staticmethod
    def increment_avg_response(n):
        with StatisticsCollector.lock:
            StatisticsCollector.number_of_terms_in_mean = StatisticsCollector.number_of_terms_in_mean + 1
            if StatisticsCollector.number_of_terms_in_mean == 0:
                StatisticsCollector.avg_response_time = n
            else:
                StatisticsCollector.avg_response_time = round(StatisticsCollector.avg_response_time
                                                              + ((n - StatisticsCollector.avg_response_time) /
                                                                 StatisticsCollector.number_of_terms_in_mean), 3)

    @staticmethod
    def get_average_response_time():
        with StatisticsCollector.lock:
            return StatisticsCollector.avg_response_time

    @staticmethod
    def write_out_stats(stats_file):
        with StatisticsCollector.lock:
            data = {
                'packets_received': StatisticsCollector.packets_received,
                'responses_sent': StatisticsCollector.responses_sent,
                'error_packets_sent': StatisticsCollector.error_packets_sent,
                'socket_errors': StatisticsCollector.error_packets_sent,
                'average_response_time': StatisticsCollector.avg_response_time,
                'number_of_devices': StatisticsCollector.number_of_devices
            }
            with open(stats_file, 'w') as f:
                f.write(json.dumps(data))
                f.close()

    @ staticmethod
    def get_stats():
        with StatisticsCollector.lock:
            return {
                'packets_received': StatisticsCollector.packets_received,
                'responses_sent': StatisticsCollector.responses_sent,
                'error_packets_sent': StatisticsCollector.error_packets_sent,
                'socket_errors': StatisticsCollector.error_packets_sent,
                'average_response_time': StatisticsCollector.avg_response_time,
                'number_of_devices': StatisticsCollector.number_of_devices
            }
