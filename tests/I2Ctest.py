import sys
import time
# include ../
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from libbasil_I2C import *

water(255, 15)
time.sleep(5)

print(getMoisture())
