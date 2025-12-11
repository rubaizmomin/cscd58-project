# Introduction
For our project we will be making and testing our own implementations of a couple of common pathfinding algorithms. In real networks they’re used to construct routing tables that determine where a received packet should be sent. We aren’t doing all that. We are just going to get information about the algorithms that would be used by the routers. 

The 2 pathfinding algorithms we will be comparing are djikstra’s algorithm and bellman-ford’s. Djikstra’s algorithm is a greedy algorithm that keeps a priority queue of untraversed edges. Upon visiting a node its edges are added to the queue. The algorithm will then check the lowest weight edge in the queue until it reaches the destination. If all of the edges are positive then it will always find the shortest path. Bellman-Ford is similar but it uses a normal queue instead of a priority queue. This will still produce a correct optimal path, but it will generally be slower. The upside is that Bellman-Ford can handle negative edges and still produce an optimal solution. 

We will be running both on the network simulation tool mininet to determine their effectiveness, optimal path, algorithm run and stabilisation time i.e., how long does the source node take to reach destination node after it failed to reach due to link failures.

# Contributions

## Vraj Shah

* Implemented multiple topologies to create networks in networkX  
* Implemented extractor that takes a networkX network and converts it into a mininet topology  
* Implemented the base of Dijkstras and Bellman Ford algorithms to run on our graphs and record stuff in our adjacency list  
* Added some metrics to record stabilization times and also times for each iteration of our algorithms

## Kevon Reid

* Added functionality to extract mininet’s network state  
* Added timing functionality  
* Added command line options  
* Ran the recorded simulations  
* Report contribution
* Video presentation


## Rubaiz Momin

* Created a daemon service that runs in the background on a thread when the simulation is running to cause the link to fail and recover, giving a real world simulation.  
* Convert miniEdit graph to adjacency list to run algorithms on the graph.  
* Created the simulation framework to run algorithms along with the link fail/recover service in the background.  
* Report contribution.
* Video presentation.

# Instructions

1 Install all networkx dependency by running **pip3 install networkx\[default\]**  
2. Go to src/simulation/simulation.py, under run\_simulation, we have link\_failure\_thread which defines our thread that will run link failures and recoveries. Change the probability based on your liking here.  
3. Go back to the src directory which contains the main.py file. The main.py contains the following parameters:
  1. Topology: Use the keywords from the following: \[dense, line, ring, sparse, star, tree\]
  2. Size of the graph: numbers representing the hosts
  3. Repetition: How many times the simulation should run
4. So to run a ring graph with 10 hosts and repeat the simulation 3 times, we do: **sudo python3 main.py ring 10 3**

# Implementation details

We used Networkx to generate the topologies then translated them to mininet, where we ran the simulations. A given topology is generated based on a few preset paradigms (e,g ring, line or tree) and a given size. With our NetworkX generated topology we import it into mininet, creating matching hosts and switches. The links connecting them are randomly given a fixed delay at creation to simulate the latency that would come with physical distances.

With our freshly created network we then run a script to regularly have each node ping its neighbours. These latencies are then added into a model of the network where we will run our algorithms to determine the shortest path between any given pair of nodes.

In real life, links fail which impacts the optimal route and sometimes also leads to isolation of the hosts. To mimic this behaviour, we run a background thread that fails or recovers a failed link based on the probabilities provided. This impacts the adjacency list on which the algorithms are run on, simulating how the graph would work on sporadic link failures.

We will be timing how long this all takes and comparing the run times of the different algorithms and topology types.

## main.py

This is the entry point of the project which parses the arguments and runs the simulation.

## simulation.py

Here we convert our networkX graph to mininet and run a thread in the background to run link failures and recoveries. We run the simulation by getting the mininet graph to an adjacency graph and run dijkstra and bellman ford on this graph. 

## link\_failures.py

This file contains a random\_failures function which is run in simulation.py in the background. We keep a record of the links that are brought down or brought up to perform link failures or link recovery. This function directly manipulates the mininet graph.

## lock.py

This is a simple lock for when we are interacting with the mininet command line so that two threads do not collide accessing the mininet command line.

## convert\_mininet\_to\_py.py

Since we weigh the edges in the networkx graph based on how long the ping takes from one node to another, we use the mininet graph to get the edge weights and convert the nodes and edges into an adjacency graph which is later used to run the algorithms.

## convert\_nx\_to\_mininet.py

This conversion is done in the beginning to convert the user’s networkX graph to a mininet graph to find edge weights, link failures and recovery.

## bellmanFord.py

Runs the bellman ford algorithm based on the adjacency list and we have also made sure (like the algorithm is made for) to detect negative cycles.

## dijkstras.py

Runs the dijkstra algorithm based on the adjacency list. This file also has a function which helps us construct the actual path that we need from a start and end node. 

# Project Analysis and Result

| topology | process | 5 hosts | 10  | 15 | 20 | 25 | 30 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| star | djikstra | 40μs | 85μs | 110μs | 113μs | 161μs | 132μs |
|  | bellman-ford | 17μs | 40μs | 45μs | 46μs | 96μs | 75μs |
| line | djikstra | 54μs | 66μs | 70μs | 100μs | 107μs | 154μs |
|  | bellman-ford | 24μs | 35μs | 33μs | 51μs | 50μs | 78μs |
| ring | djikstra | 102μs | 86μs | 94μs | 99μs | 128μs | 133μs |
|  | bellman-ford | 40μs | 40μs | 53μs | 97μs | 58μs | 96μs |
| dense | djikstra | 50μs | 74μs | 129μs | 154μs | 202μs | 250μs |
|  | bellman-ford | 24μs | 37μs | 84μs | 105μs | 127μs | 235μs |
| sparse | djikstra | 67μs | 80μs | 94μs | 121μs | 131μs | 233μs |
|  | bellman-ford | 32μs | 44μs | 55μs | 87μs | 83μs | 136μs |
| tree | djikstra | 51μs | 57μs | 84μs | 108μs | 133μs | 123μs |
|  | bellman-ford | 25μs | 25μs | 41μs | 63μs | 85μs | 78μs |

According to our results bellman-ford always performed better. This is directly contrary to the  common wisdom that djikstra’s is both faster and uses less memory. There are several possible causes. 

Inefficiencies in our implementation could’ve caused this.  Since we used python, memory is handled for us by the interpreter. Since djikstra’s uses a less space efficient algorithm it would seem reasonable that the worse space complexity makes it require more python management, leading to a slower program overall. Another problem with our interpretation is that the python’s builtin priority queue module is about twice as slow as its heap queue module. Since djikstra’s relies heavily on the priority queue, using an inefficient module could also be a major source of the discrepancy. To test this hypothesis it would require redoing the experiment in a lower level language like C, so that the memory can be managed directly rather than relying on the interpreter. 

Another possibility is that the network sizes we chose are too small to show the superiority of djikstra’s. With the hardware available to us we could barely run 30 host networks. On denser topologies especially it would almost crash the machine. If djikstra’s algorithm scales better, it’s possible that some higher network size would cause it to overtake Bellman-Ford in speed. A repeat trial could use more powerful computers to run the trials, maybe renting compute on a server.

# Conclusion

This project has really been a great opportunity for us to understand real life networks and the challenges faced. We pushed ourselves to be as creative as possible to depict a real life network by using threads and adding concurrency to operations. We also used creativity to add new metrics to add comparisons between the algorithms like the stabilisation time.  
Some of the improvements we could have made is using C instead of Python as we saw how certain operations due the algorithm’s data structure affect the time.   
Reference  
Waleed, S., Faizan, M., Iqbal, M., & Anis, M. I. (2017). Demonstration of single link failure recovery using Bellman Ford and Dijikstra algorithm in SDN. *2017 International Conference on Innovations in Electrical Engineering and Computational Technologies (ICIEECT)*, 1–4. https://doi.org/10.1109/ICIEECT.2017.7916533

