from topologies.star import buildStarGraph
from topologies.tree import buildTreeGraph
from topologies.ring import buildRingGraph
from topologies.sparse import buildSparseGraph
from topologies.line import buildLineGraph
from topologies.dense import buildDenseGraph
from simulation.simulation import run_simulation
import sys


if __name__ == "__main__":
    # read inputs
    if len(sys.argv) != 4:
        print("Usage: main.py topo size reps")
        exit(1)
    
    size = int(sys.argv[2])
    reps = int(sys.argv[3])

    # Choose a topology
    if sys.argv[1] == "star":
        G = buildStarGraph(size)
    elif sys.argv[1] == "tree":
        G = buildTreeGraph(size)
    elif sys.argv[1] == "sparse":
        G = buildSparseGraph(size)
    elif sys.argv[1] == "ring":
        G = buildRingGraph(size)
    elif sys.argv[1] == "line":
        G = buildLineGraph(size)
    elif sys.argv[1] == "dense":
        G = buildDenseGraph(size)
    else:
        print("Valid topologies: dense line ring sparse star tree")
        exit(1)

    # Run the experiment
    run_simulation(G, reps)