import csv


PORT = '/dev/cu.usbmodem14201'

def getHistory(num):
    lines = []
    with open('/home/pi/data/history.csv','r') as f:
        reader = csv.reader(f,delimiter=',')
        lines = [row for row in reader]

    msg = '+---------------------+--------------+\n|         Date        | moisture (%) |\n+---------------------+--------------+\n'
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
