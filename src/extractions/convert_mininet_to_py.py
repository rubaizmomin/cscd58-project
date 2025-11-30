from mininet.net import Mininet
from mininet.node import OVSSwitch, Host, OVSController, Node
from mininet.link import TCLink, Intf # this library makes it more realistic with metrics like bamdwidth, delay, packet loss

# TODO: finish this
def parsePing(s: str) -> float:
    print(s)
    return 0

# 
def extractLinkWeight(h1: Host, h2: Host):
    assert h1 is not h2
    assert len(h1.connectionsTo(h2)) > 0
    pingStr = h1.cmd("ping -c 1 " + h2.name)
    return parsePing(pingStr)


# gets takes all the links in net and passes a ping through 
def convert_mininet_to_py(net: Mininet):
    weights = {}
    for h1 in net.hosts:
        for h2 in net.hosts:
            if h1 is not h2 and len(h1.connectionsTo(h2)) > 0:
                extractLinkWeight(h1, h2)

    return weights