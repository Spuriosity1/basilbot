#!/usr/bin/python3
import sys
from libbasil_I2C import *
from libbasil_history import *
import config

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
    mm = config.config['man_measure']
    try:
        moisture = sample_data(mm['num_samples'])
        print(moisture)
        if moisture < mm['low_moisture']:
            print(mm['messages']['low_moisture'])
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
    mw = config.config['man_water']
    try:
        runtime = int(sys.argv[2])
    except ValueError:
        print('Invalid number specification')
        sys.exit(0)
    if runtime <= 0 or runtime > mw['max_runtime']:
        print('ERROR: time out of range [0, %d]' % mw['max_runtime'])
        sys.exit(0)
    if sample_data(mw['num_samples']) >= mw['max_moisture']:
        print('Soil is over {}% moist'.format(mw['max_moisture']))
        print(mw['messages']['max_moisture'])
        sys.exit(0)
    try:
        pumpPulse(runtime)
        print('OK')
    except OSError:
        print("ERROR: Could not establish I2C connection")
elif sys.argv[1] == 'auto':
    aw = config.config['auto_water']
    setting = False
    if len(sys.argv) == 2:
        setting = not aw['active']
    elif sys.argv[2].lower()[0] in ['y','t','s']:
        setting = True
    aw['active'] = setting
    print(("A" if setting else "Dea")+"ctivating automatic watering")
    config.save()
elif sys.argv[1] == 'config':
    print(config.traverse())
