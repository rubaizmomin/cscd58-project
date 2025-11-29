import networkx as nx
import random

def buildTreeGraph(n):
   
    graph = nx.Graph()
    graph.add_nodes_from(range(n))

    for node in range(1, n):
        parent = random.randrange(0, node)
        graph.add_edge(parent, node)
    return graph