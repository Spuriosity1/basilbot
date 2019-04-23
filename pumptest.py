import serial
import argparse
import time
import requests as req
import struct

REQ = b'\x05'
ACK = b'\x80'

SIZE = 2

NPRINT=1000
data=[]

WEBHOOK = "https://discordapp.com/api/webhooks/569672015653371948/4dQlTM9QMBq3yXwtRKIxWhivrtVMUGQrmAAxCDcSgG3yNtp0asDJv6VFZIhmB--PdA6R"


parser = argparse.ArgumentParser(description='Listens on specified port for two-byte words')

parser.add_argument('-p',help='Port to listen on.', default='/dev/ttyACM0')
parser.add_argument('-t',help='Seconds to run for', type=float, default=1)
parser.add_argument('-N',help='Number of samples', type=int, default=3)
args=parser.parse_args()

ser = serial.Serial(port=args.p, dsrdtr=True, baudrate=9600)




def sample_data(N):
    data = [0]
    for i in range(0,N):
        ser.write(b'X\n')
        res = ser.readline().strip(b'\r\n').split(b'|')
        data = [ x[0] + int(x[1]) for x in zip(data, res) ]

    return [ x/N for x in data]

def pumpPulse(speed, power):
    ser.write(b'S')
    ser.write(struct.pack('<B',speed))
    ser.write(struct.pack('<H',power))
    ser.write(b'\n')


pumpPulse(255,int(args.t*1000))
print(ser.readline())
