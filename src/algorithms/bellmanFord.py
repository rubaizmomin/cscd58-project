from math import inf

def bellmanFord(adj, source, weightKey=None):
    dist = {node: inf for node in adj}
    prev = {node: None for node in adj}
    dist[source] = 0
    edges = []
    for u in adj:
        for v, w in adj[u].items():
            if weightKey is None:
                cost = w
            else:
                cost = w[weightKey]
            edges.append((u, v, cost))

    # Relaxations
    for _ in range(len(adj) - 1):
        updated = False
        for u, v, cost in edges:
            if dist[u] != inf and dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                prev[v] = u
                updated = True
        if not updated:
            break

    # We must check for negative weight cycles
    negativeCycle = False
    for u, v, cost in edges:
        if dist[u] != inf and dist[u] + cost < dist[v]:
            negativeCycle = True
            break

    return dist, prev, negativeCycle