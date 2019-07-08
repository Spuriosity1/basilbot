import serial
import argparse
import time
import requests as req
import csv

# DEPRECEATED

REQ = b'\x05'
ACK = b'\x80'

SIZE = 2

NPRINT=1000
data=[]

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

    return [time.strftime('%Y-%m-%dT%H:%M:%S')] + [ x/N for x in data]


with open("../data/history.csv",'a') as f:
    writer = csv.writer(f)
    writer.writerow(sample_data(args.N))
