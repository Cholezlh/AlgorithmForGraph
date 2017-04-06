# -*- coding: utf-8 -*-
import sys

#########################################################################
# Graph
#########################################################################
# Description: A basic graph structure built out of lists and dictionaries.
#########################################################################
# Source: http://www.python-course.eu/graphs_python.php
#########################################################################
class Graph(object):
    # constructor
    # Takes in graph_dict dictionary parameter
    def __init__(self, graph_dict={}):
        # Initializes graph object
        # this.privateGraphDict = publicGraphDict
        self.__graph_dict = graph_dict

    # getVertices()
    def vertices(self):
        # returns the vertices of a graph
        return tuple(self.__graph_dict.keys())

    # getEdges()
    def edges(self):
        # returns the edges of a graph
        return tuple(self.__generate_edges())

    # addVertex(vertex)
    def add_vertex(self, vertex):
        # If the vertex "vertex" is not in
        #    self.__graph_dict, a key "vertex" with an empty
        #    list as a value is added to the dictionary.
        #    Otherwise nothing has to be done.
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    # addEdge(edge)
    def add_edge(self, edge):
        # Assumes that edge is of type set, tuple or list;
        #    between two vertices can be multiple edges!
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    # private generateEdges()
    def __generate_edges(self):
        # A static method generating the edges of the
        #    graph "graph". Edges are represented as sets
        #    with one (a loop back to the vertex) or two
        #    vertices
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return tuple(edges)



def tarjan(graph):
    # Declare globals
    index = {}          # Dictionary of vertices and connections
    lowlink = {}        # Dictionary of smallest indices of any node reachable from v
    stack = []          # S - stack (List)
    result = []         # List to store SCCs
    counter = [0]       # Must be list type for dictionary iteration - marks number of visits

    # Inner function; Python encapsulation convention
    # Depth-first search
    def strong_connect(v):

        # Empty graph object/list
        if not graph:
            raise ValueError("Graph is empty.")

        index[v] = counter[0]   # Depth index v = smallest unused index
        lowlink[v] = counter[0] # Computed during depth-first search from v
        counter[0] += 1         # counter++; Keep track of visits (used by stack)
        stack.append(v)         # Add vertex to stack = S.push(v)

        # Consider successors (edges) of v
        edges = graph[v]
        # for each (v, w) in E do (iterate on graph[v])
        for w in edges:
            # If (w[index] undefined], successor hasn't been visited yet
            if w not in stack:
                # Visit and add as successor
                strong_connect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            # If w already in stack
            elif w in stack:
                # Successor is a lowlink (smallest index reachable from v)
                lowlink[v] = min(lowlink[v], index[w])

        # If v is a root node, pop the stack and generate an SCC
        # If current vertex = root vertex
        if lowlink[v] == index[v]:
            # Start a new SCC list
            scc = []

            # Repeat while successor < current scc
            # True: lowlink[v] == index[v]
            # v must be left on the stack if v.lowlink < v.index
            while True:
                w = stack.pop()
                # Add w to SCC list
                scc.append(w)
                # If already visited (and are same), break
                # v must be removed as the root of a strongly connected component if v.lowlink == v.index
                if w == v:
                    break
            # Output the current strongly connected component
            # Store in tuple, immutable
            result.append(tuple(scc))

    vertices = graph
    for v in vertices:
        # If v is unvisited, make it a SCC
        if v not in lowlink:
            strong_connect(v)

    # Return list of edges (tuples)
    return result


# main - Outside of class Graph(obj)
if __name__ == "__main__":
    # A dictionary whose keys are the nodes of the graph.
#    g1 = {'A': ['F'],
#          'B': ['D', 'C'],
#          'C': ['D', 'B'],
#          'D': ['B', 'C', 'G'],
#          'E': [],
#          'F': ['A'],
#          'G': []}
#    graph1 = Graph(g1)
#    print("Edges of plain graph:")
#    print(graph1.edges())
#    print("Vertices of plain graph:")
#    print(graph1.vertices())


    g2 = {1: [2,3],
          2: [4],
          3: [4,5],
          4: [1,6],
          5: [6],
          6: []}

    graph2 = Graph(g2)

    # Create Tarjan graph object that passes in graph
    tarjan_graph = tarjan(g2)

    print("Tarjan Strongly Connected Components:")
    print(tarjan_graph)