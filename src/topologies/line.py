import networkx as nx

def buildLineGraph(n):
    graph = nx.path_graph(n)
    return graph