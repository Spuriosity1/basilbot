#!/usr/bin/python3

import sys
from libbasil import *

if sys.argv[1] == 'moisture':
    print(getMoisture())
elif sys.argv[1] == 'history':
    if sys.argc >= 2:
        print(getHistory(sys.argv[2]))
    else:
        print(getHistory(12))
elif sys.argv[1] == 'dump':
    if sys.argc >= 2:
        print(getHistory(sys.argv[2]))
    else:
        print(getHistory(12))
elif sys.argv[1] == 'water':
    try:
        runtime = int(sys.argv[2])
    except ValueError:
        print('Invalid number specification')
        sys.exit(0)
    if getMoisture() >= 70:
        print('Already moist')
        sys.exit(0)
    if runtime <= 0 or runtime >= 60:
        print('FAIL')
        sys.exit(0)
    pumpPulse(runtime)
    print('Ok')
elif sys.argv[1] == 'dump':
    try:
        print(getHistory(int(sys.argv[2])))
    except ValueError:
        print('Invalid number specification')
