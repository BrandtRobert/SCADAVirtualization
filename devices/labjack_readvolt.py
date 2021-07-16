import time
from labjack import ljm

def sinewave_old():
    # --- IMPORTED FROM : https://stackoverflow.com/questions/22566692/python-how-to-plot-graph-sine-wave
    # sin value generation test
    F = 5          # No. of cycles per second, F = 5 Hz
    T = 10         # Time period, T = 10 s
    Fs = 5        # No. of samples per second, Fs = 50 Hz
    Ts = 1./Fs        # Sampling interval, Ts = 20 us
    N = int(T/Ts)     # No. of samples for 2 ms, N = 500
    
    t = np.linspace(0, T, N)
    signal_values = np.sin(2*np.pi*F*t)
    # ---
    pprint.pprint(signal_values)
    print(len(signal_values))

def set_volt(handle, name, value=0.0):
    ljm.eWriteName(handle, name, value)
    v = ljm.eReadName(handle, name)
    return "\t%s = %f" % (name, v)


def test_change_voltage(handle, pin):
    for i in range(3):
        print(set_volt(handle, pin, i))
        time.sleep(1)
    print(set_volt(handle, pin, 3.3333333))
    print(set_volt(handle, pin, 0.0))


# Open first found LabJack
# openS: open a device based on String parameters
T7_id = "ANY"
T7_handle = ljm.openS("T7", "USB", T7_id)

# Call eReadName to read the serial number from the LabJack.
serial = "SERIAL_NUMBER"

result = ljm.eReadName(T7_handle, serial)

print("--- LabJack T7 tests --- \n- device id: scarlet \n- eReadName results: ")
print("\t%s = %f" % (serial, result))

print("\ntest1: Alter voltage on pin = 'DAC1'")
pin_dac1 = "DAC1"
test_change_voltage(T7_handle, pin_dac1)

print("\nAttempting to send voltage to S7-1200...")
print("look for LED2")
time.sleep(5)
set_volt(T7_handle, "DAC0", 2.4)
print("\tVolt sent! Sleeping for 5 seconds... (check TIA portal for values!)")


time.sleep(5)
set_volt(T7_handle, "DAC0", 0.00)
