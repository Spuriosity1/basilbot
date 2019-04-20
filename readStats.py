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

WEBHOOK = "https://discordapp.com/api/webhooks/548424706777415680/M-4DutCXJ5NJxOmK07Bwwmy1UyzWQW9R5aSTixpgCFU8CvDNfbvFw6wAzDUL-e3RiwA6"


parser = argparse.ArgumentParser(description='Listens on specified port for two-byte words')

parser.add_argument('-p',help='Port to listen on.', default='/dev/ttyACM0')
parser.add_argument('-t',help='Second delay between samples', type=float, default=1)
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


# NOTE: This needs a heuristic model of soil moisture
moisture = 100 * sample_data(args.N)[0] / 500

msg = "Soil moisture content: {:3f}%".format(moisture)
r = req.post(WEBHOOK, json={'content':msg, 'username':'Lily'})
