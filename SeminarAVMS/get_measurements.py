import serial
import random


def get_ECG_data():

    return random.randint(-5, 5)



def get_oximeter_data():
    SpO2 = random.randint(80, 99)
    BPM = random.randint(40, 100)

    SpO2_valid = True
    BPM_valid = True

    if SpO2 < 85:
        SpO2_valid = False

    if BPM < 50 or BPM > 80:
        BPM_valid = False

    return (SpO2, SpO2_valid, BPM, BPM_valid)






# serialInst = serial.Serial()

# serialInst.baudrate = 300
# serialInst.port = 'COM3'
# serialInst.open()

# while True:
# 	if serialInst.in_waiting:
# 		packet = serialInst.readline()
# 		print(packet.decode('utf').rstrip())
