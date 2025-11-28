import networkx as nx

'''
This function builds a start graph. Note that the 
first node is the center and all others are leaves, which
is why we use n-1 in the nx.star_graph method
'''
def buildStarGraph(n):
    graph = nx.star_graph(n - 1)
    return graph