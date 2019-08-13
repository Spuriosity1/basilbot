import csv
from time import strftime

PORT = '/dev/cu.usbmodem14201'

def getHistory(num):
    lines = []
    with open('/home/pi/data/history.csv','r') as f:
        reader = csv.reader(f,delimiter=',')
        lines = [row for row in reader]

    msg =  '+---------------------+--------------+\n'
    msg += '|         Date        | moisture (%) |\n'
    msg += '+---------------------+--------------+\n'
    for row in lines[-num:]:
        msg += '| {} |     {:.1f}     |\n'.format(row[0].replace('T',' '), float(row[1]))
    msg += '+---------------------+--------------+'
    return msg

def getRawHistory(num):
    msg = ''
    with open('/home/pi/data/history.csv','r') as f:
        reader = csv.reader(f,delimiter=',')
        lines = [row for row in reader]
    for row in lines[-num:]:
        msg += '{},{:.1f}\n'.format(row[0].replace('T',' '), float(row[1]))
    return msg

def setHistory(moisture):
    with open("/home/pi/data/history.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow([strftime('%Y-%m-%dT%H:%M:%S'), "%.2f" % moisture])

def getRawWatering(num):
    msg = ''
    with open('/home/pi/data/history.csv','r') as f:
        reader = csv.reader(f,delimiter=',')
        lines = [row for row in reader]
    for row in lines[-num:]:
        msg += '{},{:d},{:d}\n'.format(row[0].replace('T',' '), int(row[1]), int(row[2]))
    return msg

def setWatering(power, time):
    with open("/home/pi/data/water.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow([strftime('%Y-%m-%dT%H:%M:%S'), "%d" % power, "%d" % time])
