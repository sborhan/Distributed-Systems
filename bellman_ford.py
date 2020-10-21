import math

"""
CPSC 5520, Seattle University
This is free and unencumbered software released into the public domain.

:Credit: Used GeeksForGeeks website to build my own bellman ford algorithm
:Author: Sam Borhan
:Version: SF2020

"""


class Graph:
    """
      Class to represent a graph
      This class creates a graph by using lab3 provided data
    """

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []  # graph of list of tuples((currency1,currency2),# rate)
        self.original_weights = {}  # dictionary with key as currencies and
        # value is the rate
        self.digit_currencies = {}  # dictionary with key as currency and
        # value as assigned digit number
        self.parents = [int(-1)] * self.V  # a list which indicates the parent
        # for each index as the currency and initialized with -1 with the
        # size of our graph vertices

    def add_edge(self, currency_1, currency_2, my_orig_weight):
        """
        Function to add an edge to graph
        :param currency_1: vertex 1
        :param currency_2: vertex 2
        :param my_orig_weight: weight
        """
        self.add_new_currencies(currency_1, currency_2)
        self.add_or_update_rates(currency_1, currency_2, my_orig_weight)
        self.insert_edge_to_graph(currency_1, currency_2, my_orig_weight)

    def RemoveEdge(self, currency_1, currency_2):
        """
        Function to remove edges/currencies from the graph
        :param currency_1: vertex 1
        :param currency_2: vertex2
        """
        self.delete_original_rates(currency_1, currency_2)
        self.remove_edge_from_graph(currency_1, currency_2)

    def BellmanFord(self, src, tolerance=0.001):
        """
        Function to implement Bellman-Ford shortest path algorithm to find
        negative cycle and finding potential arbitrage
        :param src: starting root in the graph
        :param tolerance: check for acceptable negative cycle
        """
        src = self.digit_currencies.get(src)
        # Initialize distances from src to all other vertices
        # as INFINITE also parent list to -1 and initialize source distance to 0
        dist = [float("Inf")] * self.V
        self.parents = [int(-1)] * self.V
        dist[src] = 0
        # Relax all edges |V| - 1 times
        dist = self.relax_all_adges(dist, tolerance)
        # check for negative-weight cycles
        self.check_for_arbitrage(dist, src)

    def print_arbitrage(self, print_cycle):
        """
        function to print all arbitrage
        :param print_cycle: list of predecessors for each vertex in the graph
        """
        result = print_cycle
        node_1 = result[0]
        profit = 100
        print('ARBITRAGE:')
        print('\tStart from 100 USD:')
        for r in range(0, len(result)):
            node_2 = result[r]
            if node_1 != node_2:
                weight = self.original_weights.get((node_1, node_2))

                begin = list(self.digit_currencies.keys())[list(
                    self.digit_currencies.values()).index(node_1)]

                end = list(self.digit_currencies.keys())[list(
                    self.digit_currencies.values()).index(node_2)]

                print('\tExchange {} for {} at {} ---> {} {}'.format(
                    begin, end, weight, end, weight * profit))
                profit = weight * profit
                node_1 = node_2
        print(' ')
        return profit

    def add_new_currencies(self, currency_1, currency_2):
        """
        This function fill out currency dictionary if new currency added to
        the graph if not will do nothing
        :param currency_1: vertex 1
        :param currency_2: vertex 2
        """
        if currency_1 not in self.digit_currencies.keys():
            self.digit_currencies[currency_1] = len(self.digit_currencies)

        if currency_2 not in self.digit_currencies.keys():
            self.digit_currencies[currency_2] = len(self.digit_currencies)

    def add_or_update_rates(self, currency_1, currency_2, my_orig_weight):
        """
        filled up or update original weights dictionary for each 2 currencies
        :param currency_1: vertex 1
        :param currency_2: vertex2
        :param my_orig_weight: rate before convert to log number
        """
        forward_digit_currencies = (self.digit_currencies[currency_1],
                                    self.digit_currencies[
                                        currency_2])
        backward_digit_currencies = (self.digit_currencies[currency_2],
                                     self.digit_currencies[
                                         currency_1])

        self.original_weights[forward_digit_currencies] = my_orig_weight
        self.original_weights[backward_digit_currencies] = 1 / my_orig_weight

    def insert_edge_to_graph(self, currency_1, currency_2, my_orig_weight):
        """
        Inserting new edge to the graph or if edge is already exist first
        remove it from the graph then add it with the provided rate to the
        graph in order to prevent duplication

        :param currency_1: vertex 1
        :param currency_2: vertex 2
        :param my_orig_weight: weight
        """
        my_log_weight = math.log(my_orig_weight, 10)
        index = -1
        first_index = -1
        second_index = -1
        for vertecies, current_log_weight in self.graph:
            if first_index != -1 and second_index != -1:
                break
            index += 1
            if vertecies == (self.digit_currencies.get(currency_2),
                             self.digit_currencies.get(currency_1)):
                first_index = index
                continue
            if vertecies == (self.digit_currencies.get(currency_1),
                             self.digit_currencies.get(currency_2)):
                second_index = index
                continue
        if first_index != -1 and second_index != -1:
            remove_1 = self.graph[first_index]
            remove_2 = self.graph[second_index]
            self.graph.remove(remove_1)
            self.graph.remove(remove_2)

        self.graph.insert(len(self.graph), [(self.digit_currencies[currency_1],
                                             self.digit_currencies[currency_2]),
                                            -my_log_weight])
        self.graph.insert(len(self.graph), [(self.digit_currencies[currency_2],
                                             self.digit_currencies[currency_1]),
                                            my_log_weight])

    def delete_original_rates(self, currency_1, currency_2):
        """
        Function to delete specified edge/rate from original weight dictionary
        :param currency_1: vertex 1
        :param currency_2: vertex 2
        """
        forward_digit_currencies = (self.digit_currencies[currency_1],
                                    self.digit_currencies[currency_2])
        backward_digit_currencies = (self.digit_currencies[currency_2],
                                     self.digit_currencies[currency_1])
        if (currency_1, currency_2) in self.original_weights.keys():
            del self.original_weights[forward_digit_currencies]
            del self.original_weights[backward_digit_currencies]

        elif (currency_2, currency_1) in self.original_weights.keys():
            del self.original_weights[forward_digit_currencies]
            del self.original_weights[backward_digit_currencies]

    def remove_edge_from_graph(self, currency_1, currency_2):
        """
        Function to remove specified bi-directional edge from specified
        currencies
        :param currency_1: vertex 1
        :param currency_2: vertex 2
        """
        index = -1
        first_index = -1
        second_index = -1
        for vertecies, current_log_weight in self.graph:

            if first_index != -1 and second_index != -1:
                break

            index += 1
            if vertecies == (self.digit_currencies.get(currency_2),
                             self.digit_currencies.get(currency_1)):
                first_index = index
                continue
            if vertecies == (self.digit_currencies.get(currency_1),
                             self.digit_currencies.get(currency_2)):
                second_index = index
                continue

        if first_index != -1 and second_index != -1:
            remove_1 = self.graph[first_index]
            remove_2 = self.graph[second_index]
            self.graph.remove(remove_1)
            self.graph.remove(remove_2)

    def relax_all_adges(self, dist, tolerance):
        """
        Function to iterate graph V-1 time to relax edges and find shortest path
        :param dist: list of distance for each vertex
        :param tolerance: acceptable tolerance as negative cycle
        :return updated distances
        """
        for _ in range(self.V - 1):
            # Update dist value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are still in
            # queue
            for u, w in self.graph:
                if dist[u[0]] != float("Inf") and dist[u[0]] + w < dist[u[1]]:
                    if dist[u[1]] - (dist[u[0]] + w) >= tolerance:
                        dist[u[1]] = dist[u[0]] + w
                        self.parents[u[1]] = u[0]
        return dist

    def check_for_arbitrage(self, dist, src):
        """
        function to iterate again through graph and see if we can find any
        negative cycle to consider as potential arbitrage
        :param dist:
        :param src:
        :return:
        """
        for u, w in self.graph:
            print_cycle = None
            if dist[u[0]] != float("Inf") and dist[u[0]] + w < dist[u[1]]:
                dist[u[1]] = dist[u[0]] + w
                if u[0] != src and u[1] != src:
                    continue
                print_cycle = [u[1], u[0]]
                my_source = u[0]
                while self.parents[my_source] not in print_cycle:
                    print_cycle.append(self.parents[my_source])
                    my_source = self.parents[my_source]
                print_cycle.append(self.parents[my_source])
                if print_cycle[0] != src:
                    print_cycle.pop(0)
                print_cycle = print_cycle[::-1]

                result = print_cycle
                if result[0] != src or result[len(result) - 1] != src:
                    continue
                else:
                    self.print_arbitrage(result)
                    break
