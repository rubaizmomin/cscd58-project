import threading
import time
from extractions.convert_nx_to_mininet import convert_nx_to_mininet
from failures.link_failures import random_failures
from extractions.convert_mininet_to_py import extract_mininet
from algorithms.dijkstras import dijkstras, reconstructPath
from algorithms.bellmanFord import bellmanFord
import networkx as nx

def run_simulation(nx_graph, max_reps):

#TODO: should source and target always be hardcoded?
    source = "h1"
    target = "h3"
    try:
        # get the mininet graph and start the mininet graph
        net = convert_nx_to_mininet(nx_graph)
        net.start()

        # start random link failures using a thread
        link_failure_thread = threading.Thread(
            target=random_failures,
            args=(net,),
            kwargs={'fail_prob':0.2, 'recover_prob':0.5, 'sleep_interval':5},
            daemon=True
        )
        curr_reps = 0
        extract_times = []
        djik_times = []
        bell_times = []
        link_failure_thread.start()

        while curr_reps < max_reps:
            time.sleep(5)

            #start timer here
            start_time = time.perf_counter_ns()

            # after running the mininet, get the current state of the graph in networkx
            adj = extract_mininet(net)
            # end exctraction timer
            extract_time = time.perf_counter_ns()
            print(adj)

            

            # run dijkstra
            dijkstra_dist, dijkstra_prev = dijkstras(adj, source)
            dijkstra_path = reconstructPath(dijkstra_prev, source, target)
            # end djikstra timer
            djik_time = time.perf_counter_ns()

            # run bellman ford
            bf_dist, bf_prev, bf_negativeCycle = bellmanFord(adj, source)
            if bf_negativeCycle:
                bf_path = []
                bf_cost = float('inf')
                print("Negative weight cycle detected")
            else:
                bf_path = reconstructPath(bf_prev, source, target)
                bf_cost = bf_dist.get(target, float('inf'))
            #end bellman ford timer    
            bell_time= time.perf_counter_ns()

            extract_times.append(extract_time - start_time)
            djik_times.append(djik_time - extract_time)
            bell_times.append(bell_time - djik_time)
            print("\n==== CURRENT TOPOLOGY =====")
            print("Dijkstra path:", dijkstra_path, "cost=", dijkstra_dist[target], "time=", djik_times[-1])
            print("Bellman-Ford path:", bf_path, "cost=", bf_cost, "time=", bell_times[-1])
            curr_reps += 1
    except KeyboardInterrupt:
        print("\nStopping the simulation and cleaning mininet")
    finally:
        net.stop()
        print("djikstra min/max/mean:", min(djik_times), max(djik_times), sum(djik_times)/len(djik_times))
        print("bellman-ford min/max/mean:", min(bell_times), max(bell_times), sum(bell_times)/len(bell_times))

