import networkx as nx

def buildTreeGraph(n):
    if n < 2:
        return nx.Graph()

    graph = nx.complete_graph(n)

    spanningTree = nx.random_spanning_tree(graph)
    return nx.Graph(spanningTree)