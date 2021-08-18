# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 13:38:26 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

from time import sleep
from datetime import datetime
from pprint import pprint

from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient

# ----- globals
HORZ_LINE = "---------------------------"
SERVER_IP = "10.1.106.202"
SERVER_PORT = 502

   # Connection-specific DNS Suffix  . : research.colostate.edu
   # IPv4 Address. . . . . . . . . . . : 10.1.106.86
   # Subnet Mask . . . . . . . . . . . : 255.255.254.0
   # Default Gateway . . . . . . . . . : 10.1.106.1

   # check for open IPs: "nmap -sP -PR 10.1.106.*"

# ----- helpers

def get_current_time():
    raw_time = datetime.now()
    current_time = raw_time.strftime("%H:%M:%S")
    return current_time

# --- Menu GUI
def print_options():
    print(HORZ_LINE)
    print("1: Access Holding Registers")
    # future options added here
    print("\n 0: exit SCADA system")
    print(HORZ_LINE)

def option_processing(opt, C):
    if opt == 1:
        print("[{0}] - Viewing Holding Reg data...".format(opt))
        sleep(1)
        return access_h_regs(C)
    else:
        print("[{0}] - Nothing selected, exiting...".format(opt))
        sleep(1)
        return -1

# option 1: read Holding_Registers on MB-Server
#   address range = 40001-50000 ; word(1 byte)
def access_h_regs(C=ModbusClient):
    return -1
    #
    # manipulate registers......
    #

# option 2: read Coils on MB-Server
#   address range = 0-10000 ; bit
def access_coils(C):
    coils = C.read_coils(0, 50)
    print(coils)



# ----- main loops
# adapted from doc example:
#   > https://pymodbustcp.readthedocs.io/en/latest/examples/modbus_thread.html
def main():
    print("~~~ SCADA App Starting ~~~")
    
    # make a client/master
    client = ModbusClient(host=SERVER_IP, port=SERVER_PORT, unit_id=1)
    
    while True:
        if not client.is_open():
            client.open()
            print("{0} > Connected to: {1}:{2}".format(
                get_current_time(), SERVER_IP, SERVER_PORT))
            break
    try:
        # open TCP connection
        for e in range(1000):
            client.write_single_register(40005, 50)
            reg_list = client.read_holding_registers(40001, 8)
            
            # if reg_list:
            print("\n{0} v\n{1}".format(get_current_time(), reg_list))
            # else:
            #     print("{0} > ".format(get_current_time()))
            sleep(1)
            
    except KeyboardInterrupt:
        print("Done.")


if __name__=='__main__':
    
    # SCADA app
    main()
    