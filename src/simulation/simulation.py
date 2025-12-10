import threading
import time
from extractions.convert_nx_to_mininet import convert_nx_to_mininet
from failures.link_failures import random_failures
from extractions.convert_mininet_to_py import extract_mininet
from algorithms.dijkstras import dijkstras, reconstructPath
from algorithms.bellmanFord import bellmanFord
import networkx as nx

def run_simulation(nx_graph, max_reps):

    try:
        # get the mininet graph and start the mininet graph
        net = convert_nx_to_mininet(nx_graph)

        hosts = [x.name for x in net.hosts]
        print("hostnames:", hosts)
        source = ""
        target = ""
        while source not in hosts:
            source = input("Pick a starting node:")

        while target not in hosts:
            target = input("Pick a destination node:")
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

        prev_dijkstra_path = None
        prev_bellman_path = None
        dijkstra_unstable_start = None
        bellman_unstable_start = None
        dijkstra_stable_time = None
        bellman_stable_time = None

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
            # end djikstra timer
            djik_time = time.perf_counter_ns()
            # We dont need to include reconstruction time in dijkstra time
            dijkstra_path = reconstructPath(dijkstra_prev, source, target)

            now = time.perf_counter_ns()
            if dijkstra_path != prev_dijkstra_path:
                dijkstra_unstable_start = now
                dijkstra_stable_time = None
            else:
                if dijkstra_unstable_start is not None and dijkstra_stable_time is None:
                    dijkstra_stable_time = now - dijkstra_unstable_start

            prev_dijkstra_path = dijkstra_path

            # run bellman ford
            bf_dist, bf_prev, bf_negativeCycle = bellmanFord(adj, source)
            bell_time = time.perf_counter_ns()
            if bf_negativeCycle:
                bf_path = []
                bf_cost = float('inf')
                print("Negative weight cycle detected")
                # bell_time = time.perf_counter_ns()
            else:
                # Do not take resconstruction time into account for bellman ford time
                bell_time = time.perf_counter_ns()
                bf_path = reconstructPath(bf_prev, source, target)
                bf_cost = bf_dist.get(target, float('inf'))
            #end bellman ford timer    

            now = time.perf_counter_ns()
            if bf_path != prev_bellman_path:
                bellman_unstable_start = now
                bellman_stable_time = None
            else:
                if bellman_unstable_start is not None and bellman_stable_time is None:
                    bellman_stable_time = now - bellman_unstable_start

            prev_bellman_path = bf_path


            extract_times.append(extract_time - start_time)
            djik_times.append(djik_time - extract_time)
            bell_times.append(bell_time - djik_time)

            extract_ms = extract_times[-1] / 1e6
            djik_ms = djik_times[-1] / 1e6
            bell_ms = bell_times[-1] / 1e6

            print("\n==== TIMES (iteration", curr_reps, ") ====")
            print(f"Extraction time:     {extract_ms:.3f} ms")
            print(f"Dijkstra time:       {djik_ms:.3f} ms")
            print(f"Bellman-Ford time:   {bell_ms:.3f} ms")

            if dijkstra_stable_time is not None:
                print(f"Dijkstra stabilization time: {dijkstra_stable_time / 1e6:.2f} ms")

            if bellman_stable_time is not None:
                print(f"Bellman-Ford stabilization time: {bellman_stable_time / 1e6:.2f} ms")


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

