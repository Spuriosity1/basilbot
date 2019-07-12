import csv

from libbasil_I2C import sample_data

with open("../data/history.csv",'a') as f:
    writer = csv.writer(f)
    writer.writerow(sample_data(args.N))


# a tiny tiny script that does not a lot
