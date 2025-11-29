from mininet.cli import CLI
from src.topologies import buildTreeGraph   
from src.extractions import convert_nx_to_mininet
import random

# Turn a given link off by making its drop rate 100%
def killLink(l):
    l.config(loss=100)


# takes a given node and turns off all its links
def killNode(n):
    pass

# Given a mininet graph tries to find one with the most links
def idKeyNode():
    pass    

# Starts up a mininet instance, kills a link at random and then
# closes mininet
# TODO: finish this group of functions
if __name__ == "__main__":
    print("Building NetworkX graph...")
    graph = buildTreeGraph(8)      
    # The other graphs can be tested the same way
    # Make a graph using the specified function and run it here
    print("Converting to Mininet...")
    net = convert_nx_to_mininet(graph, bandwidth=5, delay='10ms', packetLoss=1)

    print("Starting Mininet...")
    net.start()

    # set the graph traversal to run and update every

    # wait a couple seconds

    # Simulate a random link failure by setting its drop rate to 100
    failLink = random.choice(net.links)
    killLink(failLink)

    


    # let the pathfinder restabilize for a few more seconds

    print("Stopping network...")
    net.stop()