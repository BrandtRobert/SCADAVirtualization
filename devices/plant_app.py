# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:02:33 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

import time
from labjack import ljm


# ----- helpers

def write(handle, pin="TDAC0", v=2.0):
    return ljm.eWriteName(handle, pin, v)

def read_analog(handle, pin="AIN0"):
    return ljm.eReadName(handle,pin)

def status_print(t, a, s1, s2, err):
    print("\n"*16)
    print("----------------------------------"
              + "\n[{0}] Potentiometer value: {1}".format(t, a)
              + "\n\t > Signal 1: -/+ 1  (TDAC0) = [{0}]".format(s1)
              + "\n\t > Signal 2: offset (TDAC1) = [{0}]".format(s2)
              + "\n err: {0}".format(err))


# ----- main loop

def main():
    T7_id = "ANY"
    T7_handle = ljm.openS("T7", "USB", T7_id)
    T7_pins = ["TDAC0", "TDAC1"]
    
    signal1_v = 0
    signal2_offset = 0
    
    
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
            
            ain0 = read_analog(T7_handle)
            
            # Print the registers for LJ and see if PLC replies
            # > occurs every 10 seconds
            # if e % 10 == 0:
            #     status_print(e, ain0, signal1_v, signal2_offset, w_error_s1)
            # else:
            #     print("\r\n[{0}]".format(e))
            
            status_print(e, ain0, signal1_v, signal2_offset, w_error_s1)
            time.sleep(1)

if __name__ == '__main__':
    
    # Plant app
    main()
    