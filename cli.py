#!/usr/bin/python3

import sys
from libbasil import *

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
