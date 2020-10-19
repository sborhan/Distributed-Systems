# Python3 program for Bellman-Ford's single source
# shortest path algorithm.

# Class to represent a graph
import math


class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []
        self.original_weights = {}
        self.digit_currencies = {}
        self.parents = [int(-1)] * self.V
        self.dfs_graph = dict()

    # function to add an edge to graph
    def add_edge(self, currency_1, currency_2, my_orig_weight):
        if currency_1 not in self.digit_currencies.keys():
            self.digit_currencies[currency_1] = len(self.digit_currencies)

        if currency_2 not in self.digit_currencies.keys():
            self.digit_currencies[currency_2] = len(self.digit_currencies)

        forward_digit_currencies = (self.digit_currencies[currency_1],
                                    self.digit_currencies[
                                        currency_2])
        backward_digit_currencies = (self.digit_currencies[currency_2],
                                     self.digit_currencies[
                                         currency_1])

        self.original_weights[forward_digit_currencies] = my_orig_weight
        self.original_weights[backward_digit_currencies] = 1 / my_orig_weight

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

        # print('my graph is: ')
        # for g in self.graph:
        #     print(g)

    def RemoveEdge(self, currency_1, currency_2):

        # print('my graph before remove is: ')
        # for g in self.graph:
        #     print(g)

        forward_digit_currencies = (self.digit_currencies[currency_1],
                                    self.digit_currencies[
                                        currency_2])
        backward_digit_currencies = (self.digit_currencies[currency_2],
                                     self.digit_currencies[
                                         currency_1])
        if (currency_1, currency_2) in self.original_weights.keys():
            del self.original_weights[forward_digit_currencies]
            del self.original_weights[backward_digit_currencies]

        elif (currency_2, currency_1) in self.original_weights.keys():
            del self.original_weights[forward_digit_currencies]
            del self.original_weights[backward_digit_currencies]

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

        # print('my graph after remove is: ')
        # for g in self.graph:
        #     print(g)

    # utility function used to print the solution
    def printArr(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))

        # The main function that finds shortest distances from src to

    # all other vertices using Bellman-Ford algorithm. The function
    # also detects negative weight cycle
    def BellmanFord(self, src):
        # print('my graph is now: {}'.format(self.graph))
        # print('SOURCE in bellman IS : {}'.format(src))
        src = self.digit_currencies.get(src)
        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE
        dist = [float("Inf")] * self.V
        self.parents = [int(-1)] * self.V
        dist[src] = 0

        # Step 2: Relax all edges |V| - 1 times. A simple shortest
        # path from src to any other vertex can have at-most |V| - 1
        # edges
        for _ in range(self.V - 1):
            # Update dist value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are still in
            # queue
            for u, w in self.graph:
                # print('relaxing {}--> {} : {}'.format(u, v, w))

                if dist[u[0]] != float("Inf") and dist[u[0]] + w < dist[u[1]]:
                    dist[u[1]] = dist[u[0]] + w
                    self.parents[u[1]] = u[0]

                    # print('relaxed ::: {}--> {} : {}'.format(u, v, w))

                # Step 3: check for negative-weight cycles. The above step
        # guarantees shortest distances if graph doesn't contain
        # negative weight cycle. If we get a shorter path, then there
        # is a cycle.
        check = -1
        # print(parent)
        is_done = False
        loop = []

        for p in self.parents:
            if p != -1:
                predecessor = list(self.digit_currencies.keys())[list(
                    self.digit_currencies.values()).index(p)]
                loop.append(predecessor)
            else:
                loop.append(-1)

        # print('parents are: {}'.format(loop))
        # print(self.parents)

        for u, w in self.graph:
            print_cycle = None
            if dist[u[0]] != float("Inf") and dist[u[0]] + w < dist[u[1]]:
                dist[u[1]] = dist[u[0]] + w
                # self.parents[u[1]] = u[0] removed now

                if u[0] != src and u[1] != src:
                    continue
                print_cycle = [u[1], u[0]]
                # print('going from {} to {}'.format(u[0], u[1]))
                # print('my print cycle is : {}'.format(print_cycle))
                my_source = u[0]
                # if print_cycle[u[1] != src]:
                #     print_cycle.remove(u[1])
                while self.parents[my_source] not in print_cycle:
                    # print('my parent is : {}'.format(self.parents[my_source]))
                    print_cycle.append(self.parents[my_source])
                    my_source = self.parents[my_source]

                # print('my parent is : {}'.format(self.parents[my_source]))
                print_cycle.append(self.parents[my_source])
                # print('Now my real cycle before pop is : {}'.format(
                #     print_cycle))
                if print_cycle[0] != src:
                    print_cycle.pop(0)
                print_cycle = print_cycle[::-1]
                # print('Now my real cycle is : {}'.format(print_cycle))

                begin = list(self.digit_currencies.keys())[list(
                    self.digit_currencies.values()).index(u[0])]
                end = list(self.digit_currencies.keys())[list(
                    self.digit_currencies.values()).index(u[1])]
                predecessor = list(self.digit_currencies.keys())[list(
                    self.digit_currencies.values()).index(self.parents[u[0]])]
                # # print('{} --> {} parent is {}'.format(begin,
                #                                       end,
                #                                       predecessor))
                # print('U is :{} + {} : w < {}: v'.format(u, w, v))

                # print("Graph contains negative weight cycle")
                # print('source is : {}'.format(src))
                # print(' {} -->  {} with rate of {}'.format(begin, end, w))

                # print('U is : {}'.format(u))
                if u[0] == src or u[1] == src:
                    print(' ')
                    # print('source is {}'.format(src))
                    # print('u[0] == src: {}'.format(u[0] == src))
                    # print('u[1] == src: {}'.format(u[1] == src))

                    start = None
                    if u[0] == src:
                        start = u[0]
                    else:
                        start = u[1]
                    # print('start is: {}'.format(start))
                    # result = Graph.retrace_negative_loop(self,
                    #                                      start)
                    # print('parents :{}'.format(self.parents))

                    # print('start is: {}'.format(start))
                    # result.reverse()
                    result = print_cycle
                    # if(result[0] != src):
                    #     continue
                    # print('new Result is: {}'.format(result))
                    node_1 = result[0]
                    profit = 100

                    if result[0] != src or result[len(result) - 1] != src:
                        continue
                    print('ARBITRAGE:')
                    print('\tStart from 100 USD:')
                    for r in range(0, len(result)):
                        # if node_1 != result[r]:
                        node_2 = result[r]
                        if node_1 != node_2:
                            weight = self.original_weights.get((node_1, node_2))

                            begin = list(self.digit_currencies.keys())[list(
                                self.digit_currencies.values()).index(node_1)]
                            end = list(self.digit_currencies.keys())[list(
                                self.digit_currencies.values()).index(node_2)]
                            print('\tExchange {} for {} at {} ---> {} {'
                                  '}'.format(
                                begin, end, weight, end, weight * profit))
                            profit = weight * profit
                            node_1 = node_2
                    if profit > 100:
                        is_done = True
                    print(' ')
            if is_done:
                break

        # for p in self.graph:
        #   a = list(self.currencies.keys())[list(
        #         self.currencies.values()).index(p[0][0])]
        #   b= list(self.currencies.keys())[list(
        #       self.currencies.values()).index(p[0][1])]
        #   print('{} --> {}'.format(a,b))

    def retrace_negative_loop(self, start):
        # print('I am {}'.format(list(self.currencies.keys())[list(
        #     self.currencies.values()).index(start)]))

        arbitrageLoop = [start]
        # print('loop is Sam: {}'.format(arbitrageLoop))
        next_node = start
        while True:

            next_node = self.parents[next_node]

            predecessor = list(self.digit_currencies.keys())[list(
                self.digit_currencies.values()).index(next_node)]
            # print('my parent is: {}'.format(predecessor))

            # print('next node is :{}'.format(next_node))
            if next_node not in arbitrageLoop:
                # print('loop is nasim: {}'.format(arbitrageLoop))
                arbitrageLoop.append(next_node)
            else:
                arbitrageLoop.append(next_node)
                arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
                # print('loop is : {}'.format(arbitrageLoop))
                return arbitrageLoop

    # def retrace_negative_loop(self, p, start):
    #     print(p)
    #     arbitrageLoop = [start]
    #     predecessor = list(self.currencies.keys())[list(
    #         self.currencies.values()).index(start)]
    #     print('parent is: {}'.format(predecessor))
    #     next_node = p[start]
    #     while next_node != start:
    #         arbitrageLoop.append(next_node)
    #         next_node = p[next_node]
    #
    #     return arbitrageLoop


# g = Graph(7)
# g.addEdge(0, 1, .75035)
# g.addEdge(0, 6, .3003)
# g.addEdge(1, 3, 100.049)
# g.addEdge(1, 2, 1.0016)
# g.addEdge(1, 4, .9089)
# g.addEdge(1, 5, .7989)
# g.addEdge(5, 6, .8322)
# g.addEdge(2, 6, .401102)

# g = Graph(5)
# g.add_edge('AUD', 'USD', .75035)
# g.add_edge('USD', 'AUD', .75035)
# g.add_edge('GPB', 'AUD', .75035)
# g.RemoveEdge('USD', 'AUD')
#
# g.add_edge('AUD', 'USD', .85035)
# g.add_edge('AUD', 'USD', .95035)
# g.add_edge('AUD', 'USD', 1.20)
#
# g.add_edge('USD', 'CHF', 1.0016)
# g.add_edge('USD', 'JPY', 100.04957)
# g.add_edge('CHF', 'JPY', 50)
# g.add_edge('AUD', 'USD', .9999)
# g.add_edge('USD', 'AUD', .98)
#
# g.BellmanFord('USD')

'''
g = Graph(7)
g.add_edge('AUD', 'USD', .75035)
g.add_edge('USD', 'CHF', 1.0016)
g.add_edge('USD', 'JPY', 100.04957)
g.add_edge('EUR', 'USD', 1.1002)
g.add_edge('GBP', 'USD', 1.2516)
g.add_edge('GBP', 'USD', 1.25162)
g.add_edge('AUD', 'USD', 0.75047)
g.add_edge('USD', 'JPY', 100.05876)
g.add_edge('EUR', 'USD', 1.10043)
g.add_edge('USD', 'CHF', 1.00154)
g.add_edge('AUD', 'CAD', 0.30038324044194714)
g.add_edge('CAD', 'GBP', 1.2015329617677886)

g.BellmanFord('USD')

g.add_edge('USD', 'JPY', 100.05945)
g.add_edge('EUR', 'USD', 1.10029)
g.add_edge('GBP', 'USD', 1.2518)
g.add_edge('AUD', 'USD', 0.75057)
g.add_edge('CHF', 'CAD', 0.40110214706340264)
g.add_edge('CAD', 'GBP', 1.6044085882536105)

g.BellmanFord('USD')


# g.RemoveEdge('AUD', 'CAD')
g.RemoveEdge('USD', 'CHF')
# g.BellmanFord('USD')

g.add_edge('USD', 'JPY', 100.08097)
g.add_edge('AUD', 'USD', 0.75049)
g.add_edge('USD', 'CHF', 1.0016)
g.add_edge('GBP', 'USD', 1.25191)
g.add_edge('EUR', 'USD', 1.10048)
g.add_edge('AUD', 'JPY', 73.73180687323122)

# Print the solution
g.BellmanFord('USD')

#
# # Initially, Contributed by Neelam Yadav
# # Later On, Edited by Himanshu Garg
'''
