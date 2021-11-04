# import matplotlib.pyplot as plt
import pprint as pp, csv, math, time, datetime, os
# import numpy as np
from labjack import ljm

from UliEngineering.SignalProcessing.Simulation import sine_wave


def get_current_time():
    now_time = datetime.datetime.now()
    current_time = now_time.strftime("%H:%M:%S")
    return current_time, now_time


# ~ adapted from https://techoverflow.net/2018/12/31/easily-generate-sine-cosine-waveform-data-in-python-using-uliengineering/
# ~ Default: Generates 1 second of data with amplitude = 1.0 (swing from -1.0 ... 1.0)
#signal_values = sine_wave(frequency=10.0, samplerate=10e2, amplitude=1.0)



# Open first found LabJack
# openS: open a device based on String parameters
T7_id = "ANY"
T7_handle = ljm.openS("T7", "USB", T7_id)
T7_pin_W = "TDAC0"
T7_pin_R = "AIN0"

print("Attempting connection to LJt7...")


volt_over_time = []

print("\ntest1: Alter voltage on  ----- pin: %s" % (T7_pin_W))
time.sleep(2)


e = 0.0
while True:
    err = ljm.eWriteName(T7_handle, T7_pin_W, e)
    if e > 0.0:
        e = 0.0
    else:
        e = 1.0

# with open("labjack_data.csv", "w", newline="") as F:
#     writer_labjack = csv.writer(F, delimiter=",")
#     current_time, _ = get_current_time()
#     print("[!] Starting data transfer... {}".format(current_time))

#     # relative time
#     T = 0
#     # 10 samples per sec
#     delta_t = 0.01
#     while T <= 10:
#         e = math.sin(T)
#         print(e)
#         #set_volt(T7_handle, "DAC0", e)
#         err = ljm.eWriteName(T7_handle, T7_pin_W, e)
#         #test_change_voltage(T7_handle, T7_pin)
#         # save time, value as CSV file
#         output_volt = ljm.eReadName(T7_handle, T7_pin_R)
#         #print("\t" + str(val))
#         real_T, int_T = get_current_time()
#         writer_labjack.writerow([real_T, T, e, output_volt])

#         time.sleep(delta_t)
#         T += delta_t

# reset TDAC0 register
err = ljm.eWriteName(T7_handle, T7_pin_W, 0.0)
print("[!] Data transferred... {}".format(get_current_time()[0]))


