import networkx as nx

'''
This graph builds a graph with only 2 more edges than nodes.
That means that the graph is pretty sparse, since we have very few
connections compared to number of nodes.
'''
def buildSparseGraph(n):
    edges = n + 2
    graph = nx.gnm_random_graph(n, edges)
    return graph

