# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 13:38:26 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

from time import sleep
from random import uniform
from pprint import pprint

from pyModbusTCP.client import ModbusClient

# globals
SERVER_IP = "169.254.153.60"
SERVER_PORT = 502


def scada_loop():
    print("Hello World, I am the SCADA app." 
      +"\n[!] I will communicate to devices with Modbus")

    
    # TCP connect on first modbus request
    client = ModbusClient(host=SERVER_IP, port=SERVER_PORT, unit_id=1)
    
    t = 0
    
    try:
        print("Attempting connection...")    
        if not client.is_open():
            client.open()
            
        while client.is_open():
            client.write_single_register(0, t)
            regs = client.read_holding_registers(0,8)
            t += 1
            pprint(regs)
            
            sleep(1)
            if t >= 100:
                t = 0
            
    except:
        print("Disconnected from device!\n")
        sleep(2)
        
    print("Done.")

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