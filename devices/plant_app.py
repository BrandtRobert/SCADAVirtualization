# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:02:33 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

from datetime import datetime as dt
from os.path import basename


from labjack import ljm
from LabjackSignalWorker import SignalWorker


# ----- globals

FILENAME = basename(__file__)
signal_data = {}


# ----- helpers

# - 
def debug_print(s):
    print("{0} : {1}".format(FILENAME, s))

# - 
def get_current_time():
    raw_time = dt.now()
    current_time = raw_time.strftime("%H:%M:%S")
    return current_time

# -
def create_filetag():
    t = dt.now().time()
    seconds = (t.hour*60 + t.minute)*60 + t.second
    return "{0}_{1}".format(dt.now().date(), seconds)

# -
def status_print(t, pot_value, s1_value, s2_value, err):
    print("\n"*4)
    print("---- {0} ----".format(get_current_time())
              + "\n[{0}] Potentiometer value: {1}".format(t, pot_value)
              + "\n\t > Signal 1: -/+ 1  (TDAC0) = [{0}]".format(s1_value)
              + "\n\t > Signal 2: offset (TDAC1) = [{0}]".format(s2_value)
              + "\n err: {0}".format(err))


# ----- main loop

def main():
    # T7_id = "ANY"
    T7_handle = ljm.openS("T7", "USB", "ANY")
    pins_w_info = [("TDAC0", "AIN0", 0.10, T7_handle), ("TDAC1", "AIN1", 1.00, T7_handle)]

    
    debug_print("Starting threads for signals...")

    
    jobs = []
    for i in pins_w_info:
        thread = SignalWorker(args=(i))
        jobs.append(thread)
    
    for j in jobs:
        j.start()
        
    for j in jobs:
        j.join()
    
    debug_print("Data to be saved.")
    

if __name__ == '__main__':
    
    # - plant app
    main()
    
    debug_print("Done.")
    

    
    