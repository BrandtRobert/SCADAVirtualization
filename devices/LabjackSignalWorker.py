# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 15:29:17 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

from time import sleep
from datetime import datetime as dt
from labjack import ljm
from threading import Thread, _active
from os.path import basename


# - Inherited Thread class for signals
class SignalWorker(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(SignalWorker, self).__init__(group=None, target=None, 
                                           name=None)
        self.pin = args[0]
        self.apin = args[1]
        self.delay = args[2]
        self.handle = args[3]
        self.trigger = False
        # - reset pins to 0v
        self.write_analog(v=0.0)

    # - get the current time
    def get_current_time(self):
        raw_time = dt.now()
        current_time = raw_time.strftime("%H:%M:%S")
        return current_time

    def debug_print(self, s):
        print("{0}-{1} : {2}".format(basename(__file__), self.get_id(), s))
        print("\t" + self.get_current_time())
    
    #TODO
    # - write data to CSV
    # columns = signal_data[0].keys()
    # try:
    #     with open("plant_data_{0}.csv".format(create_filetag()), "w") as csvfile:
    #         print("Writing to {0}...".format(csvfile.name))
    #         writer = csv.DictWriter(csvfile, fieldnames=columns)
    #         writer.writeheader()
    #         for d in signal_data:
    #             writer.writerow(signal_data[d])
    # except IOError as err:
    #     print("I/O error in CSV writing! ***\n\t{0}".format(err))
    
    
    # - 
    def write_analog(self, v=2.0):
        return ljm.eWriteName(self.handle, self.pin, v)

    # - 
    def read_analog(self, pin="AIN0"):
        return ljm.eReadName(self.handle,pin)
    
    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in _active.items():
            if thread is self:
                return id
    
    # - 
    def run(self):
        self.debug_print("Thread started on pin: {0} -- {1}".format(self.pin, self.get_current_time()))
        t = 0
        while t <= 60:
            if self.trigger:
                self.write_analog(0)
            else:
                self.write_analog()
            self.debug_print("\'{0}\' value: {1:2.4f}".format(self.pin, self.read_analog(self.apin)))
            self.trigger = not self.trigger
            t += self.delay
            sleep(self.delay)
        return
            
            