#!/usr/bin/python3

import sys
from libbasil import *

print("You'd better add the other dank responses back or Luke i swear to god")

if sys.argv[1] == 'moisture':
    print(getMoisture())
elif sys.argv[1] == 'history':
    print(getHistory(12))
elif sys.argv[1] == 'water':
    runtime = int(sys.argv[2])
    if getMoisture() >= 70:
        print('Already moist')
        sys.exit(0)
    if runtime <= 0 or runtime >= 60:
        print('FAIL')
        sys.exit(0)
    pumpPulse(runtime)
    print('Ok')
