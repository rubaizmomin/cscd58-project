from src.topologies import  (buildDenseGraph, buildLineGraph, buildRingGraph, buildStarGraph, buildTreeGraph, buildSparseGraph)

'''
To test the topologies and their outputs, simply run this file.
Make sure the edges that get printed are correct.
'''
def printInfo(graph, name):
    print(f"\n=== {name} ===")
    print("Nodes:", len(graph.nodes()))
    print("Edges:", len(graph.edges()))
    print("Edge List:", list(graph.edges())[:])


def createGraphs():
    printInfo(buildSparseGraph(10), "Sparse Graph (n=10)")
    printInfo(buildDenseGraph(10), "Dense Graph (n=10)")
    printInfo(buildRingGraph(6), "Ring Graph (n=6)")
    printInfo(buildLineGraph(6), "Line Graph (n=6)")
    printInfo(buildTreeGraph(10), "Tree Graph (n=10)")
    printInfo(buildStarGraph(8), "Star Graph (n=8)")

if __name__ == "__main__":
    createGraphs()