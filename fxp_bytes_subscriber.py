import datetime
import struct

epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)


def get_currency(byte_data):
    return byte_data.decode("utf-8")


def get_exchange_rate(byte_data):
    return struct.unpack('d', byte_data)[0]


def get_date(data):
    current_date = data
    micros = int.from_bytes(current_date, byteorder='big')
    seconds = micros // 1_000_000
    millis = micros % 1_000_000
    date_sec_added = epoch + datetime.timedelta(0, seconds)
    current_date = date_sec_added + datetime.timedelta(
        milliseconds=millis)
    return current_date
