from mininet.net import Mininet
from mininet.node import OVSSwitch, Host, OVSController
from mininet.link import TCLink # this library makes it more realistic with metrics like bamdwidth, delay, packet loss

def convert_nx_to_mininet(nx_graph, bandwidth=10, delay='5ms', packetLoss=0, add_hosts=True):

    net = Mininet(switch=OVSSwitch, controller=OVSController, link=TCLink)

    switch_map = {}

    for node in nx_graph.nodes():
        sw = net.addSwitch(f"s{node}")
        switch_map[node] = sw

        if add_hosts:
            host = net.addHost(f"h{node}")
            net.addLink(host, sw, bw=bandwidth, delay=delay, loss=packetLoss)

    for u, v in nx_graph.edges():
        net.addLink(
            switch_map[u],
            switch_map[v],
            bw=bandwidth,
            delay=delay,
            loss=packetLoss
        )

    return net