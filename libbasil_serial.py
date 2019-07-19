import struct
import csv
import time
import serial

PORT = '/dev/cu.usbmodem14201'

def convert_moisture_raw(raw):
    return 100 * raw / 500

def sample_data(ser, N):
    data = [0]
    ser.reset_input_buffer()
    for i in range(0,N):
        ser.write(b'X\n')
        res = ser.readline().strip(b'\r\n').split(b'|')
        data = [ x[0] + int(x[1]) for x in zip(data, res) ]

    retval = [ x/N for x in data]
    retval[0] = convert_moisture_raw(retval[0])
    return retval

def getMoisture():
    with serial.Serial(port=PORT, baudrate=9600,timeout=2) as ser:
        time.sleep(10)
        moisture = sample_data(ser, 5)[0]

    return moisture

def pumpPulse(time):
    with serial.Serial(port=PORT, baudrate=9600) as ser:
        ser.write(b'S')
        ser.write(struct.pack('<B',255))
        ser.write(struct.pack('<H',1000*time))
        ser.write(b'\n')

def ensureOff():
    with serial.Serial(port=PORT, baudrate=9600) as ser:
        ser.write(b'Y\n')
        res = ser.readline().strip(b'\r\n')

    return int(res)
