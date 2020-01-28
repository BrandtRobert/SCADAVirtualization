"""
    Example from SO:
        https://stackoverflow.com/questions/31267366/how-can-i-implement-a-pub-sub-pattern-using-multiprocessing
    author: https://stackoverflow.com/users/2073595/dano
"""
import os
import multiprocessing
import socket
import selectors
from functools import wraps


def ensure_parent(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if os.getpid() != self._creator_pid:
            raise RuntimeError("{} can only be called in the "
                               "parent.".format(func.__name__))
        return func(self, *args, **kwargs)
    return inner


class PublishQueue(object):
    def __init__(self):
        self._channels = {}
        self._creator_pid = os.getpid()

    def __getstate__(self):
        self_dict = self.__dict__
        self_dict['_queues'] = []
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)


    @ensure_parent
    def register(self, channel: str):
        send_q = multiprocessing.Queue()
        channel_data = self._channels.get(channel, None)
        if channel_data is None:
            channel_data = {
                "publish_queues": [],
            }
            self._channels[channel] = channel_data
        channel_data["publish_queues"].append(send_q)
        return send_q

    @ensure_parent
    def publish(self, val, channel=None):
        for key, data in self._channels.items():
            for listener_queue in data["publish_queues"]:
                if channel is not None:
                    if key == channel:
                        listener_queue.put(val)
                # If publishing to a None channel send to all queues
                else:
                    listener_queue.put(val)
