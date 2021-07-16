# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 09:37:10 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

import pprint as pp, time, os, sys
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
# ----- main loops

def read_loop(handle):
    input("Enter to start loop...")
    for e in range(100):
        s = read_analog(handle)
        print("[{0}] AIN0 = {1}".format(e, s))
        

def option_loop():
    T7_id = "ANY"
    T7_handle = ljm.openS("T7", "USB", T7_id)
    T7_pins = ["TDAC0", "TDAC1"]
    
    ain0 = read_analog(T7_handle)
    
    _ = write(T7_handle, T7_pins[0], 0.0)
    
    print(" ~ Communication Terminal to DAC/PLC ~ ")
    
    while True:
        try:
            pin_i = int(input("\tEnter pin index = "))
            volt_val = float(input("\tEnter voltage   = "))
            
            err = write(T7_handle, T7_pins[pin_i], volt_val)
            print("[.] Transmiting {0}v through pin {1}".format(volt_val, pin_i))
            print("\t" + str(err))
            
            ain0 = read_analog(T7_handle)
            print("[!] Analog feedback value: {0}\n".format(ain0))
    
            time.sleep(0.5)
            
        except TypeError as e:
            print("[!] TypeError: " + str(e))
            break
        except ValueError as e:
            print("[!] ValueError: " + str(e))
            break
        except IndexError as e:
            print("[!] IndexError: " + str(e))
            break
    
    
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
    
    # Double Pulse loop! (auto)
    main()
    
    # for debugging! (manual)
    #option_loop()
    
    # for debugging as well! (manual)
    #read_loop(ljm.openS("T7", "USB", "ANY"))




