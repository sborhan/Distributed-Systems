import datetime
import sys
import socket
import fxp_bytes_subscriber
import bellman_ford

MY_ADDRESS = ('127.0.0.1', 55555)
MY_Byte_ADDRESS = b'\x7f\x00\x00\x01\xd9\x03'
TIME_OUT = 600  # time out after 10 minutes
BUFF_SIZE = 1024
LIFETIME = 1.5
ROOT = 'USD'
VERTICES_NUMBER = 50


class Lab3(object):

    def __init__(self, address):

        self.provider = address
        self.byte_address = MY_Byte_ADDRESS
        self.listener, self.listener_address = self.start_a_server()  # socket
        # & host/port
        self.currencies = {}
        self.received_time = {}
        self.my_graph = None
        self.old_date = None
        self.black_list = []
        self.my_graph = bellman_ford.Graph(VERTICES_NUMBER)

    def run(self):

        self.listener.sendto(self.byte_address, self.provider)
        while True:
            print('\nWaiting {} minutes to receive all UDP '
                  'messages....\n'.format(int(TIME_OUT / 60)))
            try:
                self.listener.settimeout(TIME_OUT)
                data, server = self.listener.recvfrom(BUFF_SIZE)
            except socket.timeout:
                print('REQUEST TIMED OUT AFTER {} SECONDS'.format(TIME_OUT))
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
        for (currency_1, currency_2) in self.received_time.keys():
            received_time = self.received_time.get((currency_1, currency_2))
            if (datetime.datetime.utcnow() - received_time).seconds > LIFETIME:
                self.black_list.append((currency_1, currency_2))
                self.my_graph.RemoveEdge(currency_1, currency_2)
                print('removing stale quote for ({}, {})'.format(currency_1,
                                                                 currency_2))

    def remove_old_data(self):
        while self.black_list:
            del self.received_time[self.black_list.pop()]

    def get_info(self, data):
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
        print('My Socket binding with: {}'.format(MY_ADDRESS))
        return listener, listener.getsockname()


def check_input(input):
    port = None
    host = None

    if len(input) == 2 or len(input) > 3:
        print("Usage: python3 lab3.py [Provider_HOST] [Provider_PORT] ")

    elif len(input) == 1:
        host = 'localhost'
        port = 50405

    else:
        try:
            port = int(input[2])
        except ValueError:
            print("Oops! That was no valid Port number.  Try again...")
            exit(1)

        if port not in range(1025, 65536):
            print("Port needs to be between 1025-65535.")
            exit(1)

        host = input[1]

    return host, port


if __name__ == '__main__':
    host, port = check_input(sys.argv)
    provider_address = (host, port)
    lab3 = Lab3(provider_address)
    lab3.run()
