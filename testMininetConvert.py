import time
from mininet.cli import CLI
from src.topologies import buildTreeGraph, buildDenseGraph, buildLineGraph
from src.extractions import convert_nx_to_mininet

def main():
    print("Building NetworkX graph...")
    # graph = buildTreeGraph(8)      
    # graph = buildLineGraph(3)
    graph = buildDenseGraph(5, 0.6)
    # The other graphs can be tested the same way
    # Make a graph using the specified function and run it here
    print("Converting to Mininet...")
    net = convert_nx_to_mininet(graph, bandwidth=5, delay='5ms', packetLoss=0)

    print("Starting Mininet...")
    net.start()

    print("Delaying for a few seconds to stabilize the network...")
    print("Wait 60 seconds!")
    net.pingAll()
    # time.sleep(60)

    print("Network loaded! Opening CLI...")
    CLI(net)

    print("Stopping network...")
    net.stop()

if __name__ == "__main__":
    main()