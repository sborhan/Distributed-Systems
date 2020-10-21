import datetime
import sys
import socket
import fxp_bytes_subscriber
import bellman_ford

"""
CPSC 5520, Seattle University
This is free and unencumbered software released into the public domain.

:Credit: Used GeeksForGeeks website to build my own bellman ford algorithm
:Author: Sam Borhan
:Version: SF2020

"""

MY_ADDRESS = ('127.0.0.1', 55555)  # Address to bind my localhost
MY_Byte_ADDRESS = b'\x7f\x00\x00\x01\xd9\x03'  # my hardcoded bye address
TIME_OUT = 600  # time out after 10 minutes
BUFF_SIZE = 1024  # receive buffer size
LIFETIME = 1.5  # life of currencies exchange in second in my graph
ROOT = 'USD'  # my root vertex
VERTICES_NUMBER = 50  # making a graph with 50 vertices


class Lab3(object):
    """
    Class that subscribes client to a foreign exchange provider server and
    waiting to receive currency rates as UDP message then attempting to
    organize the data and printing the arbitrage opportunities using bellman
    ford library
    """

    def __init__(self, address):

        self.provider = address  # forex provider address
        self.byte_address = MY_Byte_ADDRESS  # my local address binding
        # address in byte format
        self.listener, self.listener_address = self.start_a_server()  # socket
        # & host/port
        self.currencies = {}  # dictionary with string currency name as key and
        # an integer as value
        self.received_time = {}  # dictionary with currencies as key and
        # received time as value
        self.old_date = None  # last time receiving a data to check time order
        self.black_list = []  # list of out of order data needed to remove
        self.my_graph = bellman_ford.Graph(VERTICES_NUMBER)  # creating graph
        # using bellman ford library

    def run(self):
        """
         Subscribing to fex-provider and decoding UDP message using
         fxp_bytes_subscriber library and making the graph and proving arbitrage
         by using bellman ford library
        """
        print('Subscribing to {}\n'.format(self.provider))
        try:
            self.listener.sendto(self.byte_address, self.provider)
        except Exception as err:
            print('Error : {}'.format(err))
            return

        while True:
            print('\nWaiting {} minutes to receive all UDP '
                  'messages....\n'.format(int(TIME_OUT / 60)))
            try:
                self.listener.settimeout(TIME_OUT)
                data, server = self.listener.recvfrom(BUFF_SIZE)
            except socket.timeout:
                print(
                    'REQUEST TIMED OUT AFTER {} minutes'.format(TIME_OUT / 60))
                print('Socket Closed : No More Data Received!')
                self.listener.close()
                break

            self.check_current_data_lifetime()
            self.remove_old_data()
            # print('Receiving UDP Message from {}'.format(server))
            packet = [data[i:i + 32] for i in range(0, len(data), 32)]
            self.add_data_to_my_graph(packet)
            self.my_graph.BellmanFord(ROOT)

    def add_data_to_my_graph(self, packet):
        """
        Adding the data to Graph by decoding received UDP packet
        :param packet: received UDP message from provider
        :return: currencies and weights of each 32 bytes data
        """
        for data in packet:
            current_date, currency_1, currency_2, exchange_rate = \
                self.get_info(data)
            print('{} {} {} {}'.format(current_date, currency_1, currency_2,
                                       exchange_rate))
            if self.old_date is None:
                self.old_date = current_date
            elif current_date < self.old_date:
                print('ignoring out-of-sequence message')
                continue
            else:
                self.old_date = current_date

            self.received_time[(currency_1, currency_2)] = current_date
            self.my_graph.add_edge(currency_1, currency_2, exchange_rate)

    def check_current_data_lifetime(self):
        """
        Checking if data received in order if nor ignore the data
        """
        for (currency_1, currency_2) in self.received_time.keys():
            received_time = self.received_time.get((currency_1, currency_2))
            if (datetime.datetime.utcnow() - received_time).seconds > LIFETIME:
                self.black_list.append((currency_1, currency_2))
                self.my_graph.RemoveEdge(currency_1, currency_2)
                print('removing stale quote for ({}, {})'.format(currency_1,
                                                                 currency_2))

    def remove_old_data(self):
        """
        Deleting old data from currencies received time dictionary
        """
        while self.black_list:
            del self.received_time[self.black_list.pop()]

    def get_info(self, data):
        """
        Decoding and returning UDP message using fxp_bytes_subscriber library
        :param data: UDP received message
        :return: date , currencies and rates
        """
        current_date = fxp_bytes_subscriber.get_date(data[0:8])
        currency_1 = fxp_bytes_subscriber.get_currency(data[8:11])
        currency_2 = fxp_bytes_subscriber.get_currency(data[11:14])
        exchange_rate = fxp_bytes_subscriber.get_exchange_rate(
            data[14:22])
        if currency_1 not in self.currencies:
            self.currencies[currency_1] = len(self.currencies)
        if currency_2 not in self.currencies:
            self.currencies[currency_2] = len(self.currencies)
        return current_date, currency_1, currency_2, exchange_rate

    def print_currencies(self):
        """
        Printing currencies dictionary just for testing purposes
        """
        for key, value in self.currencies.items():
            print('{}, {}'.format(key, value))

    @staticmethod
    def start_a_server():
        """
        Making a server for ourself by creating a socket and binding to our
        local host and an available port and return that socket along with
        port and host
        :return: created socket and (host,port)
        """
        listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listener.bind(MY_ADDRESS)
        print('\nMy Socket binding with: {}'.format(MY_ADDRESS))
        return listener, listener.getsockname()


def check_input(user_input):
    """
    Checking user input
    :param user_input: system arguments
    :return: provider_host and provider_port of fxp provider
    """
    provider_port = None
    provider_host = None
    if len(user_input) == 2 or len(user_input) > 3:
        print("Usage: python3 lab3.py [Provider_HOST] [Provider_PORT] ")
        exit(1)

    elif len(user_input) == 1:
        provider_host = 'localhost'
        provider_port = 50405

    else:
        try:
            provider_port = int(user_input[2])
        except ValueError:
            print("Oops! That was no valid Port number.  Try again...")
            exit(1)

        if provider_port not in range(1025, 65536):
            print("Port needs to be between 1025-65535.")
            exit(1)
        try:
            provider_host = user_input[1]
        except Exception as err:
            print('Error: {}'.format(err))

    return provider_host, provider_port


if __name__ == '__main__':
    """
    Receiving fxp provider address or use default address and initializing 
    lab3 class and run it to make the graph and produce arbitrage by using UDP 
    message 
    sent from provider
    """
    host, port = check_input(sys.argv)
    provider_address = (host, port)
    lab3 = Lab3(provider_address)
    lab3.run()
