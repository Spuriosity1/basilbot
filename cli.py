#!/usr/bin/python3
import sys
from libbasil_I2C import *
from libbasil_history import *

SIPP='''
```
 _____ _
/  ___(_)
\\ `--. _ _ __  _ __
 `--. \\ | '_ \\| '_ \\
/\\__/ / | |_) | |_) |
\\____/|_| .__/| .__/
        | |   | |
        |_|   |_|
```
'''

MAX_MOISTURE = 80


if sys.argv[1] == 'moisture':
    try:
        print(getMoisture())
    except OSError:
        print("ERROR: Could not establish I2C connection")
elif sys.argv[1] == 'history':
    if len(sys.argv) < 3:
        print(getHistory(12))
    else:
        print(getHistory(int(sys.argv[2])))
elif sys.argv[1] == 'raw_history':
    if len(sys.argv) < 3:
        print(getRawHistory(12))
    else:
        print(getRawHistory(int(sys.argv[2])))
elif sys.argv[1] == 'water':
    try:
        runtime = int(sys.argv[2])
    except ValueError:
        print('Invalid number specification')
        sys.exit(0)
    if runtime <= 0 or runtime > 60:
        print('ERROR: time out of range [0, 60]')
        sys.exit(0)
    if getMoisture() >= MAX_MOISTURE:
        print('Already over {}% moist'.format(MAX_MOISTURE))
        print('Also, <@167249375775555584>: Please get your airbags checked.')
        sys.exit(0)
    try:
        pumpPulse(runtime)
        print('OK')
    except OSError:
        print("ERROR: Could not establish I2C connection")

elif sys.argv[1] == 'dump':
    try:
        print(getHistory(int(sys.argv[2])))
    except ValueError:
        print('Invalid number specification')
