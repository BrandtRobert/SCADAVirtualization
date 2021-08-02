# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 13:38:26 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

from time import sleep
from pprint import pprint

from pyModbusTCP.client import ModbusClient

# globals
SERVER_IP = "10.1.106.200"
SERVER_PORT = 502

   # Connection-specific DNS Suffix  . : research.colostate.edu
   # IPv4 Address. . . . . . . . . . . : 10.1.106.86
   # Subnet Mask . . . . . . . . . . . : 255.255.254.0
   # Default Gateway . . . . . . . . . : 10.1.106.1

HORZ_LINE = "---------------------------"



# MENU GUI
def print_options():
    print(HORZ_LINE)
    print("1: Access Holding Registers")
    
    print("\n 0: exit SCADA system")
    print(HORZ_LINE)

def option_processing(opt, C):
    if opt == 1:
        print("[{0}] - Viewing Holding Reg data...".format(opt))
        sleep(1)
        access_h_regs(C)
    else:
        print("[{0}] - Nothing selected, exiting...".format(opt))
        sleep(1)
        return -1
    

# option 1: read Holding_Registers on MB-Server
#   address range = 40001-50000 ; word(1 byte)
def access_h_regs(C=ModbusClient):
    regs = C.read_holding_registers(40001, 100)
    print(regs)
    #
    # manipulate registers......
    #
    
    

# option 2: read Coils on MB-Server
#   address range = 0-10000 ; bit
def access_coils(C=ModbusClient):
    coils = C.read_coils(0, 50)
    print(coils)
    

def scada_loop():
    print("~~~ SCADA App Starting ~~~")
    
    # Make a client/master
    client = ModbusClient(host=SERVER_IP, port=SERVER_PORT, unit_id=1)
    while not client.is_open():
            try:
                print("[?] Attempting connection...")
                if client.open():
                    print("\t Connected to server!")
            except:
                print("[!] Disconnected from device with error!\n")
                sleep(2)
    
    while client.is_open():
        print_options()
        option = input("Select an option:")
        
        status = option_processing(option, client)
        
        if status < 0:
            break
        
    print("[.] Done.")

if __name__=='__main__':
    scada_loop()
    # server = ModbusServer(SERVER_IP, SERVER_PORT, no_block=True)
    
    # try:
    #     print("[?] Starting server...")
    #     server.start()
    #     print("[!] Server is online")
    #     state = [0]
        
    #     while True:
    #         DataBank.set_words(0, [int(uniform(0,100))])
    #         if state != DataBank.get_words(1):
    #             state = DataBank.get_words(1)
    #             print(state)
    #             sleep(0)
        
    # except:
    #     print("[!] Server shutting down...")
    #     server.stop()