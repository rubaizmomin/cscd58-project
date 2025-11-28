import networkx as nx

def buildRingGraph(n):
    graph = nx.cycle_graph(n)
    return graph