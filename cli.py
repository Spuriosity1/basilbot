#!/usr/bin/python3

SIPP='''
```
 _____ _
/  ___(_)
\ `--. _ _ __  _ __
 `--. \ | '_ \| '_ \
/\__/ / | |_) | |_) |
\____/|_| .__/| .__/
        | |   | |
        |_|   |_|
```
'''


import sys
from libbasil_I2C import *
from libbasil import getHistory, getRawHistory
import time
from serial.serialutil import SerialException

if sys.argv[1] == 'moisture':
    try:
        print(getMoisture())
    except SerialException:
        print("ERROR: Could not establish Serial connection")
elif sys.argv[1] == 'history':
    print(getHistory(12))
elif sys.argv[1] == 'raw_history':
    print(getRawHistory(12))
elif sys.argv[1] == 'water':
    try:
        runtime = int(sys.argv[2])
    except ValueError:
        print('Invalid number specification')
        sys.exit(0)
    if getMoisture() >= 70:
        print('Already over 70% moist')
        sys.exit(0)
    if runtime <= 0 or runtime > 60:
        print('FAIL')
        sys.exit(0)

    try:
        pumpPulse(runtime)
        print(SIPP)
        time.sleep(runtime+3)
        value = ensureOff()
        if value < 100:
            print('WARN: Pump pin reads %d, should be closer to 255' % value)

    except SerialException:
        print("ERROR: Could not establish Serial connection")

elif sys.argv[1] == 'dump':
    try:
        print(getHistory(int(sys.argv[2])))
    except ValueError:
        print('Invalid number specification')
