from math import inf
import heapq

'''
For now I have added a parameter called weight_key.
Since I have it set to None right now, it will just use integers
as weights. Later, we can make it use the value at the key specified.
For example, if set it to "delay", it can use these values instead.
'''
def dijkstras(adj, source, weightKey=None):
    dist = {node: inf for node in adj}
    prev = {node: None for node in adj}
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        distance, u = heapq.heappop(pq)
        if distance > dist[u]:
            continue
        for v, w in adj[u].items():
            if weightKey is None:
                cost = w
            else:
                cost = w[weightKey]
            newDistance = distance + cost
            if newDistance < dist[v]:
                dist[v] = newDistance
                prev[v] = u
                heapq.heappush(pq, (newDistance, v))
    return dist, prev

'''
Since our algos tell us just the distances, 
this function can show us the actual path. Must pass
in the prev dictionary that was return by the algo
'''
def reconstructPath(prev, source, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        if cur == source:
            break
        cur = prev[cur]
    path.reverse()
    if path[0] != source:
        return []
    return path