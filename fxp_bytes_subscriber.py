import datetime
import struct
"""
CPSC 5520, Seattle University
This is free and unencumbered software released into the public domain.

:Credit: Used GeeksForGeeks website to build my own bellman ford algorithm
:Author: Sam Borhan
:Version: SF2020
"""


"""
 Using this file as library in lab3 Class to decode UDP message from byte to 
 usable data
"""
epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)


def get_currency(byte_data):
    """
    decoding currencies from byte to string
    :param byte_data:
    :return: returning currencies sd string
    """
    return byte_data.decode("utf-8")


def get_exchange_rate(byte_data):
    """
    decoding rate from byte to float
    :param byte_data: rate in byte
    :return: rate in float
    """
    return struct.unpack('d', byte_data)[0]


def get_date(data):
    """
    decoding date from byte to UTC time
    :param data: date in byte
    :return: date in UTC time
    """
    current_date = data
    micros = int.from_bytes(current_date, byteorder='big')
    seconds = micros / 1_000_000
    date_sec_added = epoch + datetime.timedelta(0, seconds)
    return date_sec_added
