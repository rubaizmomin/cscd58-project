from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch, Host, OVSController
from mininet.link import TCLink  
from src.extractions import convert_mininet_to_py, convert_nx_to_mininet
from src.topologies import buildLineGraph   


def main():
    
    graph = buildLineGraph(2)

    net = convert_nx_to_mininet(graph)


    print("Starting Mininet...")
    net.start()

    print("Extracting link weights")
    weights = convert_mininet_to_py.extract_mininet(net)
    print(weights)


    print("Stopping network...")
    net.stop()

if __name__ == "__main__":
    main()