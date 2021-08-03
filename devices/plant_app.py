# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:02:33 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

from time import sleep
from datetime import datetime
from pprint import pprint
from labjack import ljm

# ----- globals

time_series = {}

# ----- helpers

def get_current_time():
    raw_time = datetime.now()
    current_time = raw_time.strftime("%H:%M:%S")
    return current_time

def write(handle, pin="TDAC0", v=2.0):
    return ljm.eWriteName(handle, pin, v)

def read_analog(handle, pin="AIN0"):
    return ljm.eReadName(handle,pin)

def status_print(t, pot_value, s1_value, s2_value, err):
    print("\n"*4)
    print("---- {0} ----".format(get_current_time())
              + "\n[{0}] Potentiometer value: {1}".format(t, pot_value)
              + "\n\t > Signal 1: -/+ 1  (TDAC0) = [{0}]".format(s1_value)
              + "\n\t > Signal 2: offset (TDAC1) = [{0}]".format(s2_value)
              + "\n err: {0}".format(err))


# ----- main loop

def main():
    T7_id = "ANY"
    T7_handle = ljm.openS("T7", "USB", T7_id)
    T7_pins = ["TDAC0", "TDAC1"]
    
    signal1_v = 0
    signal2_offset = 0
    
    try:
        while True:
            for e in range (1000):
                # Alternate +/- 1 from base signal
                if e % 10 == 0 and e != 0:
                    if signal1_v > signal2_offset:
                        signal1_v = 0
                    else:
                        signal1_v = 1
    
                # Change offset to 2
                # > if pot is connected, this value will not matter
                if e == 100:
                    if signal2_offset > 0:
                        signal2_offset = 0
                    else:
                        pot_input = read_analog(T7_handle)
                        if pot_input < 1.0:
                            signal2_offset = 2
                        else:
                            signal2_offset = int(pot_input)
                
                w_error_s1 = write(T7_handle, T7_pins[0], signal1_v)
                _ = write(T7_handle, T7_pins[1], signal2_offset)
                
                pot_ain = read_analog(T7_handle)
                
                # Print the registers for LJ and see if PLC replies
                status_print(e, pot_ain, signal1_v, signal2_offset, w_error_s1)
                
                time_series[get_current_time()] = (signal1_v, signal2_offset)
                
                sleep(1)
                
    except KeyboardInterrupt:
        print("Service terminated.")
    
    # process/output time series data into CSV
    print(time_series)

if __name__ == '__main__':
    
    # Plant app
    main()
    
    