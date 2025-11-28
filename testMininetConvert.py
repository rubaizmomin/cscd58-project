from mininet.cli import CLI
from src.topologies import buildTreeGraph   
from src.extractions import convert_nx_to_mininet

def main():
    print("Building NetworkX graph...")
    graph = buildTreeGraph(8)      
    # The other graphs can be tested the same way
    # Make a graph using the specified function and run it here
    print("Converting to Mininet...")
    net = convert_nx_to_mininet(graph, bandwidth=5, delay='10ms', packetLoss=1)

    print("Starting Mininet...")
    net.start()

    print("Network loaded! Opening CLI...")
    CLI(net)

    print("Stopping network...")
    net.stop()

if __name__ == "__main__":
    main()