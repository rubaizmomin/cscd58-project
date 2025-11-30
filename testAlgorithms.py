from src.algorithms.bellmanFord import bellmanFord
from src.algorithms.dijkstras import dijkstras, reconstructPath

'''
To test my code, I will create a simple graph and run both algos on it.
'''
def main():
    # adj = {
    # "s0": {"s1": 1, "s2": 1, "s3": 1},
    # "s1": {"s3": 1},
    # "s2": {"s3": 1},
    # "s3": {}        
    # }
    adj = {
        "s0": {"s1": 1, "s2": 4, "s3": 2},
        "s1": {"s3": 6, "s2": 2},
        "s2": {"s3": 3},
        "s3": {}
    }

    print("\n=== TEST GRAPH ===")
    for u in adj:
        print(u, "->", adj[u])

    source = "s0"
    target = "s2"

    print("\n=== Running Dijkstra ===")
    dist_dij, prev_dij = dijkstras(adj, source)
    print("Distances:", dist_dij)
    print("Shortest path:", reconstructPath(prev_dij, source, target))

    print("\n=== Running Bellman-Ford ===")
    dist_bf, prev_bf, neg = bellmanFord(adj, source)
    print("Distances:", dist_bf)
    print("Shortest path:", reconstructPath(prev_bf, source, target))
    print("Negative cycle detected?", neg)


if __name__ == "__main__":
    main()


