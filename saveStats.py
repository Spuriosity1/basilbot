#!/usr/bin/python3

import csv
import time

from libbasil_I2C import sample_data

with open("../data/history.csv",'a') as f:
    writer = csv.writer(f)
    writer.writerow([time.strftime('%Y-%m-%dT%H:%M:%S'), sample_data(15)])


# a tiny tiny script that does not a lot
