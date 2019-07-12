import smbus2
import struct
import time


CHANNEL = 0x08


def convert_moisture_raw(raw):
    # very scientific
    # 4 is for the left shifts employed in plantI2C.ino
    return 4 * 100 * raw / 500

# Bus number is 1
bus = smbus2.SMBus(1)


def water(speed, time):
    req_str  = struct.pack('<B',speed)
    req_str += struct.pack('<H',1024*time)
    bus.write_i2c_block_data(CHANNEL, ord('W'), req_str)

def moisture_read():
    req_str  = struct.pack('<B',255)
    req_str += struct.pack('<H',128)
    bus.write_i2c_block_data(CHANNEL, ord('M'), req_str)
    time.sleep(0.5)
    # Hacky workaround for read_i2c_block_data being broken
    bus.write_byte(CHANNEL, ord('R'), 0x00)
    return bus.read_byte(CHANNEL)


def sample_data(N):
    data = []
    for i in range(0,N):
        res = moisture_read()
        data.append(res)

    return convert_moisture_raw(sum(data)/N)

def getMoisture():
    return sample_data(15);
