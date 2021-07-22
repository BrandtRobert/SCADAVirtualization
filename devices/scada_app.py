# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 13:38:26 2021

@author: Luis Rodriguez
@email: Luis.Rodriguez[at]rams.colostate.edu
@company: Colorado State University
"""

import time
from pyModbusTCP.client import ModbusClient


print("Hello World, I am the SCADA app." 
      +"\n[!] I will communicate to devices with Modbus")

# TCP auto connect on first modbus request
c = ModbusClient(host="192.168.0.241", port=502, unit_id=1)

print("Attempting connection...")
whi
conn_status = c.open()

print(conn_status)

regs = c.read_holding_registers(0,2)

print(regs)