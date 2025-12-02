from topologies.star import buildStarGraph
from simulation.simulation import run_simulation

if __name__ == "__main__":
    # Choose a topology
    G = buildStarGraph(5)

    # Run the experiment
    run_simulation(G)