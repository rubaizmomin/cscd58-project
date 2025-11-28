import networkx as nx

'''
This function builds a dense graph based on the number of nodes and a density index.
A density index can only be between 0 and 1. We can use it this way to make graphs more and less 
dense. For example, a denseIndex of 0.9 is VERY dense (uses 90% of max possible edges),
while a denseIndex of 0.1 is NOT dense (uses only 10% of max possible edges).
By default, the denseIndex is set to 0.5.
'''
def buildDenseGraph(n, denseIndex=0.5):
    maxEdges = n * (n - 1) // 2
    edges = int(maxEdges * denseIndex)
    graph = nx.gnm_random_graph(n, edges)
    return graph