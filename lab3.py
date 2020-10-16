import math
import sys
import socket
import fxp_bytes_subscriber
import bellman_ford

MY_ADDRESS = ('127.0.0.1', 55555)
MY_Byte_ADDRESS = b'\x7f\x00\x00\x01\xd9\x03'
TIME_OUT = 3
BUFF_SIZE = 1024


class Lab3(object):

    def __init__(self, address):

        self.provider = address
        self.byte_address = MY_Byte_ADDRESS
        self.listener, self.listener_address = self.start_a_server()  # socket
        # & host/port
        self.currencies = {}
        self.my_graph = None

    def get_udp_message(self):
        self.listener.settimeout(TIME_OUT)
        self.listener.sendto(self.byte_address, self.provider)
        try:
            my_graph = bellman_ford.Graph(100)
            while True:
                data, server = self.listener.recvfrom(BUFF_SIZE)
                print('Receiving UDP Message from {}'.format(server))
                packet = [data[i:i + 32] for i in range(0, len(data), 32)]
                # my_graph = bellman_ford.Graph(len(packet))
                print('my packet has {} info'.format(len(packet)))
                for data in packet:
                    current_date = fxp_bytes_subscriber.get_date(data[0:8])
                    currency_1 = fxp_bytes_subscriber.get_currency(data[8:11])
                    currency_2 = fxp_bytes_subscriber.get_currency(data[11:14])
                    exchange_rate = fxp_bytes_subscriber.get_exchange_rate(
                        data[14:22])
                    # print('my dict has {} data in it now'.format(len(
                    #     self.currencies)))
                    if currency_1 not in self.currencies:
                        self.currencies[currency_1] = len(self.currencies)
                    # print('my dict has {} data in it now'.format(len(
                    #     self.currencies)))
                    if currency_2 not in self.currencies:
                        self.currencies[currency_2] = len(self.currencies)
                    # print('my dict has {} data in it now'.format(len(
                    #     self.currencies)))

                    # my_graph.addEdge(self.currencies[currency_1],
                    #                  self.currencies[currency_2],
                    #                  exchange_rate)
                    my_graph.addEdge(currency_1,
                                     currency_2,
                                     exchange_rate)

                    print('{} {} {} {}'.format(current_date,
                                               currency_1,
                                               currency_2,
                                               exchange_rate))
                    # for key, value in self.currencies.items():
                    #     print('{}, {}'.format(key, value))
                # print('source in lab3 file is : {}'.format(
                # self.currencies.get( 'USD'))) my_graph.BellmanFord(
                # self.currencies.get('USD'))

                my_graph.BellmanFord('USD')


        except socket.timeout:
            print('REQUEST TIMED OUT AFTER {} SECONDS'.format(TIME_OUT))

        print('Socket Closed : No More Data Received!')
        self.listener.close()

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


if __name__ == '__main__':

    if len(sys.argv) == 2 or len(sys.argv) > 3:
        print("Usage: python3 lab3.py [Provider_HOST] [Provider_PORT] ")
        exit(1)

    elif len(sys.argv) == 1:
        host = 'localhost'
        port = 50405

    else:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Oops! That was no valid Port number.  Try again...")
            exit(1)
        host = sys.argv[1]

    if port not in range(1025, 65536):
        print("Port needs to be between 1025-65535.")
        exit(1)

    provider_address = (host, port)
    lab3 = Lab3(provider_address)
    lab3.get_udp_message()
