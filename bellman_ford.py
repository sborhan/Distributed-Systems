# Python3 program for Bellman-Ford's single source
# shortest path algorithm.

# Class to represent a graph
import math


class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []
        self.weights = {}
        self.currencies = {}
        self.parents = [int(-1)] * self.V
        self.dfs_graph = dict()

    # function to add an edge to graph
    def addEdge(self, u, v, w):
        print('my graph is: {}'.format(self.graph))
        if u not in self.currencies:
            self.currencies[u] = len(self.currencies)

        if v not in self.currencies:
            self.currencies[v] = len(self.currencies)

        self.weights[(self.currencies[u], self.currencies[v])] = w
        self.weights[(self.currencies[v], self.currencies[u])] = 1 / w

        weight = math.log(w, 10)
        index = -1
        for g, ww in self.graph:
            # print(index)

            # print('{} == {}'.format(g, (self.currencies.get(u),
            #                             self.currencies.get(v))))
            if g == (self.currencies.get(u), self.currencies.get(v)):
                if ww == w:
                    # print('Duplicate')
                    return
                else:
                    index += 1
                    # print(index)
                    # PROBLEM IS HERE Not deleting just adding again
                    # print('updating by removing older version')
                    self.graph[index] = [
                        (self.currencies[u], self.currencies[v]), -weight]
                    index += 1
                    # print(index)

                    # print('inside else index is : {}'.format(index))

                    self.graph[index] = [
                        (self.currencies[v], self.currencies[u]), weight]
                    index = -1
                    return
        # print('added')
        self.graph.append([(self.currencies[u], self.currencies[v]), -weight])
        self.graph.append([(self.currencies[v], self.currencies[u]), weight])

    def RemoveEdge(self, u, v):
        item1 = (self.currencies[u], self.currencies[v])
        weight1 = None
        item2 = (self.currencies[v], self.currencies[u])
        weight2 = None
        for v, w in self.graph:
            if v == item1:
                weight1 = w
                break
        for v, w in self.graph:
            if v == item2:
                weight2 = w
                break
        # print('({},{} removed'.format(item1, weight1))
        self.graph.remove([item1, weight1])
        self.graph.remove([item2, weight2])


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
        print('SOURCE in bellman IS : {}'.format(src))
        src = self.currencies.get(src)
        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE
        dist = [float("Inf")] * self.V
        # self.parents = [int(-1)] * self.V
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
                predecessor = list(self.currencies.keys())[list(
                    self.currencies.values()).index(p)]
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

                begin = list(self.currencies.keys())[list(
                    self.currencies.values()).index(u[0])]
                end = list(self.currencies.keys())[list(
                    self.currencies.values()).index(u[1])]
                predecessor = list(self.currencies.keys())[list(
                    self.currencies.values()).index(self.parents[u[0]])]
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

                    if result[0] != src or result[len(result)-1] != src:
                        continue
                    print('ARBITRAGE:')
                    print('\tStart from 100 USD:')
                    for r in range(0, len(result)):
                        # if node_1 != result[r]:
                        node_2 = result[r]
                        if node_1 != node_2:
                            weight = self.weights.get((node_1, node_2))

                            begin = list(self.currencies.keys())[list(
                                self.currencies.values()).index(node_1)]
                            end = list(self.currencies.keys())[list(
                                self.currencies.values()).index(node_2)]
                            print('\tExchange from {} to {} is : {} {}'.format(
                                begin, end, weight * profit, end))
                            profit = weight * profit
                            node_1 = node_2
                    if profit > 101:
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

            predecessor = list(self.currencies.keys())[list(
                self.currencies.values()).index(next_node)]
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

g = Graph(4)
g.addEdge('AUD', 'USD', .75035)
g.addEdge('AUD', 'USD', .75035)
g.addEdge('AUD', 'USD', .75035)
g.addEdge('AUD', 'USD', 1.20)


g.addEdge('USD', 'CHF', 1.0016)
g.addEdge('USD', 'JPY', 100.04957)
g.addEdge('CHF', 'JPY', 50)

g.BellmanFord('USD')


# g = Graph(7)
# g.addEdge('AUD', 'USD', .75035)
# g.addEdge('USD', 'CHF', 1.0016)
# g.addEdge('USD', 'JPY', 100.04957)
# g.addEdge('EUR', 'USD', 1.1002)
# g.addEdge('GBP', 'USD', 1.2516)
# g.addEdge('GBP', 'USD', 1.25162)
# g.addEdge('AUD', 'USD', 0.75047)
# g.addEdge('USD', 'JPY', 100.05876)
# g.addEdge('EUR', 'USD', 1.10043)
# g.addEdge('USD', 'CHF', 1.00154)
# g.addEdge('AUD', 'CAD', 0.30038324044194714)
# g.addEdge('CAD', 'GBP', 1.2015329617677886)
#
# # g.BellmanFord('USD')
#
# g.addEdge('USD', 'JPY', 100.05945)
# g.addEdge('EUR', 'USD', 1.10029)
# g.addEdge('GBP', 'USD', 1.2518)
# g.addEdge('AUD', 'USD', 0.75057)
# g.addEdge('CHF', 'CAD', 0.40110214706340264)
# g.addEdge('CAD', 'GBP', 1.6044085882536105)
#
# # g.BellmanFord('USD')
#
#
# # g.RemoveEdge('AUD', 'CAD')
# g.RemoveEdge('USD', 'CHF')
# # g.BellmanFord('USD')
#
# print("************************HERE***********************")
# g.addEdge('USD', 'JPY', 100.08097)
# g.addEdge('AUD', 'USD', 0.75049)
# g.addEdge('USD', 'CHF', 1.0016)
# g.addEdge('GBP', 'USD', 1.25191)
# g.addEdge('EUR', 'USD', 1.10048)
# g.addEdge('AUD', 'JPY', 73.73180687323122)
#
# # Print the solution
# g.BellmanFord('USD')
#
# #
# # # Initially, Contributed by Neelam Yadav
# # # Later On, Edited by Himanshu Garg
