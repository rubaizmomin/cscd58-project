from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch, Host, OVSController
from mininet.link import TCLink  
from mininet.log import setLogLevel, info
from src.extractions import convert_mininet_to_py, convert_nx_to_mininet
from src.topologies import buildLineGraph
from src.topologies.ring import buildRingGraph   
import time


def main():
    
    # graph = buildLineGraph(2)
    graph = buildRingGraph(4)

    net = convert_nx_to_mininet(graph)


    print("Starting Mininet...")
    net.start()
    net.pingAll()
    setLogLevel('error')
    net.pingAll()
    setLogLevel('info')

    print("Waiting 5 seconds")
    time.sleep(5)

    print("Testing Connectivity (Ping All)...")
    net.pingAll()

    print("Extracting link weights")
    weights = convert_mininet_to_py.extract_mininet(net)
    print(weights)

    print("Stopping network...")
    net.stop()

if __name__ == "__main__":
    main()