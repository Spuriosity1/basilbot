import smbus
import struct
import time

reg_write_dac = 0x40
channel = 0x03


# Bus number is 1
bus = smbus.SMBus(1)


def water(speed, time):
    req_str  = struct.pack('<B',speed)
    req_str += struct.pack('<H',1000*time)
    bus.write_i2c_block_data(CHANNEL, 'S', req_str)

def moisture_read():
    # read a block of 4 bytes (offset 0)
    res = bus.read_i2c_block_data(address, 0, 4)
    return struct.unpack('<HBB',res)


def sample_data(N):
    data = []
    for i in range(0,N):
        res = moisture_read()[0]
        data.append(res)

    return convert_moisture_raw(sum(data)/N)

def getMoisture():
    return sample_data(15);
