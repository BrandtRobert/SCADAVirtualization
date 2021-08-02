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

def scada_loop():
    print("Hello World, I am the SCADA app." 
      +"\n[!] I will communicate to devices with Modbus")

    
    # Make a client/master
    client = ModbusClient(host=SERVER_IP, port=SERVER_PORT, unit_id=1)
    
    while True:
            try:
                print("[?] Attempting connection...")
                status = client.open()
            except:
                print("[!] Disconnected from device with error!\n")
                sleep(2)
                    
        
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